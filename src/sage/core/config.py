"""
SAGE Configuration Management.

Unified configuration system supporting:
- YAML configuration files (sage.yaml)
- Environment variable overrides
- Default values
- Validation

Version: 0.1.0

Configuration Priority (highest to lowest):
1. Environment variables (SAGE_*)
2. YAML configuration file
3. Default values
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from sage.core.exceptions import ConfigNotFoundError, ConfigParseError

# =============================================================================
# Default Configuration Values
# =============================================================================

DEFAULT_CONFIG: dict[str, Any] = {
    "version": "0.1.0",
    "knowledge_base": {
        "path": ".",
        "index_file": "index.md",
        "content_dir": "content",
    },
    "loading": {
        "always": ["index.md"],
        "triggers": {},
    },
    "timeouts": {
        "t1_instant": 100,
        "t2_fast": 500,
        "t3_layer": 3000,
        "t4_comprehensive": 10000,
        "t5_background": 60000,
    },
    "cache": {
        "enabled": True,
        "max_size": 100,
        "ttl_seconds": 300,
    },
    "logging": {
        "level": "INFO",
        "format": "json",
        "include_timestamps": True,
    },
    "plugins": {
        "enabled": True,
        "directory": "plugins",
        "autoload": True,
    },
    "memory": {
        "enabled": True,
        "persistence_dir": None,  # Uses platformdirs default
        "auto_save": True,
        "auto_save_interval": 60,
    },
    "mcp": {
        "name": "sage-kb",
        "description": "SAGE Knowledge Base - Production-grade knowledge management",
    },
}


# =============================================================================
# Configuration Data Classes
# =============================================================================


@dataclass
class TimeoutConfig:
    """Timeout configuration."""

    t1_instant: int = 100
    t2_fast: int = 500
    t3_layer: int = 3000
    t4_comprehensive: int = 10000
    t5_background: int = 60000


@dataclass
class CacheConfig:
    """Cache configuration."""

    enabled: bool = True
    max_size: int = 100
    ttl_seconds: int = 300


@dataclass
class LoggingConfig:
    """Logging configuration."""

    level: str = "INFO"
    format: str = "json"
    include_timestamps: bool = True


@dataclass
class PluginConfig:
    """Plugin configuration."""

    enabled: bool = True
    directory: str = "plugins"
    autoload: bool = True


@dataclass
class MemoryConfig:
    """Memory persistence configuration."""

    enabled: bool = True
    persistence_dir: str | None = None
    auto_save: bool = True
    auto_save_interval: int = 60


@dataclass
class MCPConfig:
    """MCP server configuration."""

    name: str = "sage-kb"
    description: str = "SAGE Knowledge Base - Production-grade knowledge management"


@dataclass
class KnowledgeBaseConfig:
    """Knowledge base configuration."""

    path: str = "."
    index_file: str = "index.md"
    content_dir: str = "content"


@dataclass
class SAGEConfig:
    """
    Complete SAGE configuration.

    Combines all configuration sections into a single object.
    """

    version: str = "0.1.0"
    knowledge_base: KnowledgeBaseConfig = field(default_factory=KnowledgeBaseConfig)
    timeouts: TimeoutConfig = field(default_factory=TimeoutConfig)
    cache: CacheConfig = field(default_factory=CacheConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    plugins: PluginConfig = field(default_factory=PluginConfig)
    memory: MemoryConfig = field(default_factory=MemoryConfig)
    mcp: MCPConfig = field(default_factory=MCPConfig)
    loading: dict[str, Any] = field(
        default_factory=lambda: {"always": [], "triggers": {}}
    )


# =============================================================================
# Configuration Loading
# =============================================================================


def find_config_file(start_path: Path | None = None) -> Path | None:
    """
    Find sage.yaml configuration file.

    Searches in order:
    1. Current directory
    2. Parent directories (up to root)
    3. User config directory

    Args:
        start_path: Starting directory for search

    Returns:
        Path to config file if found, None otherwise
    """
    search_paths = []

    # Start from given path or current directory
    current = Path(start_path) if start_path else Path.cwd()

    # Search up the directory tree
    while current != current.parent:
        search_paths.append(current / "sage.yaml")
        current = current.parent

    # Also check root
    search_paths.append(current / "sage.yaml")

    for path in search_paths:
        if path.exists():
            return path

    return None


def load_yaml_config(path: Path) -> dict[str, Any]:
    """
    Load configuration from YAML file.

    Args:
        path: Path to YAML file

    Returns:
        Configuration dictionary

    Raises:
        ConfigNotFoundError: If file doesn't exist
        ConfigParseError: If YAML parsing fails
    """
    if not path.exists():
        raise ConfigNotFoundError(str(path))

    try:
        with open(path, encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        return config
    except yaml.YAMLError as e:
        raise ConfigParseError(str(path), parse_error=str(e)) from e


def get_env_overrides() -> dict[str, Any]:
    """
    Get configuration overrides from environment variables.

    Environment variables are prefixed with SAGE_ and use double underscore
    for nested keys. For example:
    - SAGE_LOGGING__LEVEL=DEBUG
    - SAGE_CACHE__ENABLED=false
    - SAGE_TIMEOUTS__T1_INSTANT=200

    Returns:
        Dictionary of configuration overrides
    """
    overrides: dict[str, Any] = {}
    prefix = "SAGE_"

    for key, value in os.environ.items():
        if not key.startswith(prefix):
            continue

        # Remove prefix and convert to lowercase
        config_key = key[len(prefix) :].lower()

        # Split by double underscore for nested keys
        parts = config_key.split("__")

        # Convert value to appropriate type
        converted_value = _convert_env_value(value)

        # Build nested dict
        current = overrides
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = converted_value

    return overrides


def _convert_env_value(value: str) -> Any:
    """Convert environment variable string to appropriate type."""
    # Boolean
    if value.lower() in ("true", "yes", "1"):
        return True
    if value.lower() in ("false", "no", "0"):
        return False

    # Integer
    try:
        return int(value)
    except ValueError:
        pass

    # Float
    try:
        return float(value)
    except ValueError:
        pass

    # String
    return value


def merge_configs(*configs: dict[str, Any]) -> dict[str, Any]:
    """
    Deep merge multiple configuration dictionaries.

    Later configs override earlier ones.

    Args:
        *configs: Configuration dictionaries to merge

    Returns:
        Merged configuration dictionary
    """
    result: dict[str, Any] = {}

    for config in configs:
        for key, value in config.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = merge_configs(result[key], value)
            else:
                result[key] = value

    return result


def load_config(config_path: Path | None = None) -> dict[str, Any]:
    """
    Load complete configuration with all sources merged.

    Priority (highest to lowest):
    1. Environment variables
    2. YAML config file
    3. Default values

    Args:
        config_path: Optional explicit path to config file

    Returns:
        Complete merged configuration dictionary
    """
    configs = [DEFAULT_CONFIG.copy()]

    # Load YAML config if available
    yaml_path = config_path or find_config_file()
    if yaml_path:
        try:
            yaml_config = load_yaml_config(yaml_path)
            configs.append(yaml_config)
        except (ConfigNotFoundError, ConfigParseError):
            pass  # Use defaults if config file has issues

    # Apply environment overrides
    env_overrides = get_env_overrides()
    if env_overrides:
        configs.append(env_overrides)

    return merge_configs(*configs)


def config_to_dataclass(config: dict[str, Any]) -> SAGEConfig:
    """
    Convert configuration dictionary to SAGEConfig dataclass.

    Args:
        config: Configuration dictionary

    Returns:
        SAGEConfig instance
    """
    return SAGEConfig(
        version=config.get("version", "0.1.0"),
        knowledge_base=KnowledgeBaseConfig(**config.get("knowledge_base", {})),
        timeouts=TimeoutConfig(**config.get("timeouts", {})),
        cache=CacheConfig(**config.get("cache", {})),
        logging=LoggingConfig(**config.get("logging", {})),
        plugins=PluginConfig(**config.get("plugins", {})),
        memory=MemoryConfig(**config.get("memory", {})),
        mcp=MCPConfig(**config.get("mcp", {})),
        loading=config.get("loading", {"always": [], "triggers": {}}),
    )


# =============================================================================
# Global Configuration Instance
# =============================================================================

_config: SAGEConfig | None = None


def get_config(reload: bool = False) -> SAGEConfig:
    """
    Get the global configuration instance.

    Args:
        reload: Force reload configuration from sources

    Returns:
        SAGEConfig instance
    """
    global _config

    if _config is None or reload:
        config_dict = load_config()
        _config = config_to_dataclass(config_dict)

    return _config


def reset_config() -> None:
    """Reset the global configuration (mainly for testing)."""
    global _config
    _config = None
