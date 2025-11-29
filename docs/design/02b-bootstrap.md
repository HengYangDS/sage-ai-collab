---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~900
---

# Application Bootstrap & Configuration

> Declarative initialization and configuration management for SAGE

---

## Table of Contents

- [1. Bootstrap Process](#1-bootstrap-process)
- [2. Entry Point](#2-entry-point)
- [3. Configuration Settings](#3-configuration-settings)

---

## 1. Bootstrap Process

### 1.1 Overview

The bootstrap process handles declarative application initialization:

- Configuration loading
- DI container setup
- EventBus initialization (S.A.G.E. aligned pub/sub)
- Service registration

### 1.2 Implementation

```python
# src/sage/core/bootstrap.py
"""
Application Bootstrap - Declarative initialization.
"""
from pathlib import Path
from typing import Dict, Any, Optional
import yaml

from sage.core.di import DIContainer, get_container, Lifetime
from sage.core.events import EventBus, get_event_bus
from sage.core.logging import configure_logging, get_logger
from sage.core.protocols import SourceProtocol, AnalyzeProtocol, GenerateProtocol, EvolveProtocol

logger = get_logger(__name__)


async def bootstrap(
    config_path: Optional[Path] = None,
    config_override: Optional[Dict[str, Any]] = None
) -> DIContainer:
    """
    Bootstrap the SAGE application.
    
    Args:
        config_path: Path to sage.yaml (default: ./sage.yaml)
        config_override: Override config values
        
    Returns:
        Configured DI container
    """
    # Load configuration
    config = _load_config(config_path or Path("sage.yaml"))
    if config_override:
        config = _merge_config(config, config_override)

    # Configure logging
    log_config = config.get("logging", {})
    configure_logging(
        level=log_config.get("level", "INFO"),
        format=log_config.get("format", "console"),
    )

    logger.info("bootstrapping application", config_path=str(config_path))

    # Setup DI container
    container = get_container()
    container.configure(config)

    # Register core services
    _register_core_services(container, config)

    # Setup EventBus subscriptions (S.A.G.E. aligned channels)
    event_bus = get_event_bus()
    _setup_event_subscriptions(event_bus, config)

    logger.info("bootstrap complete", services=len(container._registrations))
    return container


def _load_config(path: Path) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    if not path.exists():
        logger.warning("config file not found, using defaults", path=str(path))
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _merge_config(base: Dict, override: Dict) -> Dict:
    """Deep merge configuration dictionaries."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _merge_config(result[key], value)
        else:
            result[key] = value
    return result


def _register_core_services(container: DIContainer, config: Dict) -> None:
    """Register core protocol implementations."""
    from sage.core.loader import TimeoutLoader
    from sage.core.knowledge import KnowledgeService
    from sage.core.output import MultiChannelOutput
    from sage.core.metrics import MetricsCollector

    container.register(SourceProtocol, TimeoutLoader, Lifetime.SINGLETON)
    container.register(AnalyzeProtocol, KnowledgeService, Lifetime.TRANSIENT)
    container.register(GenerateProtocol, MultiChannelOutput, Lifetime.SCOPED)
    container.register(EvolveProtocol, MetricsCollector, Lifetime.SINGLETON)
```

---

## 2. Entry Point

### 2.1 Unified Entry Point

```python
# src/sage/__main__.py
"""
Unified Entry Point.

Usage:
    python -m sage serve [--service cli|mcp|api|all]
    python -m sage --version
"""
import asyncio
import sys
import argparse

from sage import __version__
from sage.core.bootstrap import bootstrap


async def main():
    parser = argparse.ArgumentParser(prog="sage")
    parser.add_argument("--version", action="store_true")

    subparsers = parser.add_subparsers(dest="command")

    # serve command
    serve_parser = subparsers.add_parser("serve", help="Start services")
    serve_parser.add_argument(
        "--service",
        choices=["cli", "mcp", "api", "all"],
        default="all",
        help="Service to start"
    )
    serve_parser.add_argument("--host", default="localhost")
    serve_parser.add_argument("--port", type=int)

    args = parser.parse_args()

    if args.version:
        print(f"sage {__version__}")
        return 0

    if args.command == "serve":
        # Bootstrap application
        container = await bootstrap()

        # Start requested service(s)
        if args.service in ("mcp", "all"):
            from sage.services.mcp_server import start_mcp_server
            await start_mcp_server(host=args.host, port=args.port or 8000)

        if args.service in ("api", "all"):
            from sage.services.http_server import start_api_server
            start_api_server(host=args.host, port=args.port or 8080)

        if args.service == "cli":
            from sage.services.cli import app
            app()

        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
```

---

## 3. Configuration Settings

### 3.1 SageSettings Class

```python
# src/sage/core/config.py
"""
Configuration Management with pydantic-settings.

Supports:
- Environment variables (SAGE_*)
- User config file
- Project config file
- Package defaults
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path
from typing import Literal, Optional


class SageSettings(BaseSettings):
    """Zero-coupling configuration with multiple sources."""

    model_config = SettingsConfigDict(
        env_prefix="SAGE_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Version
    version: str = Field(default="0.1.0")
    debug: bool = Field(default=False)

    # Timeout settings
    timeout_global_max_ms: int = Field(default=10000)
    timeout_default_ms: int = Field(default=5000)

    # Loading settings
    loading_max_tokens: int = Field(default=4000)
    loading_cache_enabled: bool = Field(default=True)
    loading_cache_ttl_seconds: int = Field(default=300)

    # Logging settings
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(default="INFO")
    log_format: Literal["console", "json"] = Field(default="console")

    # CORS settings (for API)
    cors_origins: list[str] = Field(default_factory=list)

    # Paths
    config_path: Optional[Path] = Field(default=None)
    content_root: Path = Field(default=Path("content"))

    @classmethod
    def load(cls, project_config: Optional[Path] = None) -> "SageSettings":
        """Load settings from all sources with proper precedence."""
        if project_config and project_config.exists():
            import yaml
            with open(project_config) as f:
                yaml_config = yaml.safe_load(f) or {}
            return cls(**yaml_config)
        return cls()


def get_settings() -> SageSettings:
    """Get application settings."""
    return SageSettings.load(Path("sage.yaml"))
```

### 3.2 Configuration Priority

| Priority | Source                    | Example                     |
|----------|---------------------------|-----------------------------|
| 1 (High) | Environment variables     | `SAGE_TIMEOUT_DEFAULT_MS`   |
| 2        | User config               | `~/.config/sage/config.yaml`|
| 3        | Project config            | `./sage.yaml`               |
| 4 (Low)  | Package defaults          | Built-in values             |

### 3.3 Key Settings

| Setting                  | Default | Description              |
|--------------------------|---------|--------------------------|
| `timeout_global_max_ms`  | 10000   | Global max timeout       |
| `timeout_default_ms`     | 5000    | Default operation timeout|
| `loading_max_tokens`     | 4000    | Max tokens per request   |
| `loading_cache_enabled`  | true    | Enable response caching  |
| `log_level`              | INFO    | Logging level            |
| `log_format`             | console | Output format            |

---

## Related

- `docs/design/02-sage-protocol.md` — Protocol overview
- `docs/design/02a-di-eventbus.md` — DI Container and EventBus
- `docs/design/01b-configuration.md` — Configuration hierarchy details
- `config/sage.yaml` — Main configuration file

---

*Part of SAGE Knowledge Base*
