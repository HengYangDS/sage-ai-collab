# Plugin System Configuration

> Configuration reference for the SAGE plugin system

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Plugin Discovery](#2-plugin-discovery)
- [3. Plugin Configuration](#3-plugin-configuration)
- [4. Bundled Plugins](#4-bundled-plugins)
- [5. Custom Plugins](#5-custom-plugins)
- [6. Security](#6-security)

---

## 1. Overview

### 1.1 Plugin Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Plugin Manager                           │
├─────────────────────────────────────────────────────────────┤
│  Discovery  │  Loading  │  Lifecycle  │  Configuration     │
└──────┬──────┴─────┬─────┴──────┬──────┴────────┬───────────┘
       │            │            │               │
       ▼            ▼            ▼               ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────────────┐
│ Bundled  │ │ External │ │  Custom  │ │ Per-Plugin Config │
│ Plugins  │ │ Packages │ │  Local   │ │    Settings       │
└──────────┘ └──────────┘ └──────────┘ └───────────────────┘
```

### 1.2 Plugin Types

| Type         | Location                    | Use Case           |
|--------------|-----------------------------|--------------------|
| **Bundled**  | `src/sage/plugins/bundled/` | Core functionality |
| **External** | PyPI packages               | Community plugins  |
| **Custom**   | User directory              | Project-specific   |

---

## 2. Plugin Discovery

### 2.1 Discovery Configuration

```yaml
# config/sage.yaml
plugins:
  discovery:
    # Enable/disable discovery sources
    sources:
      bundled: true
      external: true
      custom: true
    
    # Search paths for custom plugins
    paths:
      - plugins/
      - ~/.sage/plugins/
    
    # Entry point group for external plugins
    entry_point: sage.plugins
    
    # Auto-discovery on startup
    auto_discover: true
```

### 2.2 Discovery Process

```
1. Scan bundled plugins directory
2. Search entry points (sage.plugins)
3. Scan custom plugin paths
4. Validate plugin manifests
5. Register valid plugins
```

### 2.3 Entry Point Configuration

For external plugins (in plugin's `pyproject.toml`):

```toml
[project.entry-points."sage.plugins"]
my_plugin = "my_package.plugin:MyPlugin"
```

---

## 3. Plugin Configuration

### 3.1 Global Plugin Settings

```yaml
# config/sage.yaml
plugins:
  # Enable/disable plugin system
  enabled: true
  
  # Plugin loading behavior
  loading:
    lazy: true              # Load plugins on demand
    parallel: true          # Parallel loading
    timeout: 5000           # Loading timeout (ms)
  
  # Plugin isolation
  isolation:
    enabled: true
    sandbox: false          # Experimental
  
  # Default settings for all plugins
  defaults:
    enabled: true
    log_level: INFO
    timeout: 10000
```

### 3.2 Per-Plugin Configuration

```yaml
# config/sage.yaml
plugins:
  config:
    # Plugin-specific settings
    knowledge_analyzer:
      enabled: true
      settings:
        max_depth: 5
        include_metadata: true
    
    content_validator:
      enabled: true
      settings:
        strict_mode: false
        rules:
          - check_links
          - check_format
    
    export_plugin:
      enabled: false  # Disabled
```

### 3.3 Environment Variables

```bash
# Global
export SAGE_PLUGINS_ENABLED=true
export SAGE_PLUGINS_PATH=/custom/plugins

# Per-plugin (pattern: SAGE_PLUGIN_<NAME>_<SETTING>)
export SAGE_PLUGIN_ANALYZER_ENABLED=true
export SAGE_PLUGIN_ANALYZER_MAX_DEPTH=10
```

---

## 4. Bundled Plugins

### 4.1 Available Bundled Plugins

| Plugin              | Purpose                   | Default  |
|---------------------|---------------------------|----------|
| `knowledge_loader`  | Load knowledge content    | Enabled  |
| `content_analyzer`  | Analyze content structure | Enabled  |
| `search_indexer`    | Index for search          | Enabled  |
| `cache_manager`     | Caching functionality     | Enabled  |
| `metrics_collector` | Usage metrics             | Disabled |

### 4.2 Bundled Plugin Configuration

```yaml
plugins:
  bundled:
    knowledge_loader:
      enabled: true
      settings:
        file_extensions:
          - .md
          - .yaml
          - .json
        ignore_patterns:
          - ".*"
          - "_*"
          - "node_modules"
    
    content_analyzer:
      enabled: true
      settings:
        analyzers:
          - structure
          - links
          - metadata
    
    search_indexer:
      enabled: true
      settings:
        index_path: .cache/search_index
        update_on_change: true
    
    cache_manager:
      enabled: true
      settings:
        backend: memory       # memory | file | redis
        ttl: 3600
        max_size: 1000
```

---

## 5. Custom Plugins

### 5.1 Plugin Structure

```
plugins/
└── my_plugin/
    ├── __init__.py
    ├── plugin.py          # Main plugin class
    ├── config.yaml        # Plugin config schema
    └── README.md          # Documentation
```

### 5.2 Plugin Manifest

```yaml
# plugins/my_plugin/config.yaml
name: my_plugin
version: "1.0.0"
description: Custom plugin description
author: Your Name

# Dependencies
requires:
  sage: ">=0.1.0"
  python: ">=3.12"

# Plugin capabilities
capabilities:
  - analyzer
  - transformer

# Configuration schema
config_schema:
  type: object
  properties:
    option1:
      type: string
      default: "value"
    option2:
      type: integer
      default: 10
```

### 5.3 Plugin Registration

```yaml
# config/sage.yaml
plugins:
  custom:
    # Local plugin
    my_plugin:
      enabled: true
      path: plugins/my_plugin
      settings:
        option1: custom_value
        option2: 20
    
    # External package
    sage_community_plugin:
      enabled: true
      package: sage-community-plugin
      settings:
        api_key: ${PLUGIN_API_KEY}
```

---

## 6. Security

### 6.1 Security Configuration

```yaml
plugins:
  security:
    # Allowed operations
    permissions:
      file_read: true
      file_write: false
      network: false
      subprocess: false
    
    # Sandboxing (experimental)
    sandbox:
      enabled: false
      memory_limit: 100MB
      cpu_limit: 1.0
    
    # Allowed paths
    allowed_paths:
      - .knowledge/
      - .cache/
    
    # Blocked plugins
    blocklist:
      - untrusted_plugin
```

### 6.2 Permission Levels

| Level          | File Read | File Write | Network | Subprocess |
|----------------|-----------|------------|---------|------------|
| **Restricted** | ✗         | ✗          | ✗       | ✗          |
| **Read-Only**  | ✓         | ✗          | ✗       | ✗          |
| **Standard**   | ✓         | Limited    | ✗       | ✗          |
| **Extended**   | ✓         | ✓          | Limited | ✗          |
| **Full**       | ✓         | ✓          | ✓       | ✓          |

### 6.3 Plugin Validation

```yaml
plugins:
  validation:
    # Require signed plugins
    require_signature: false
    
    # Allowed sources
    trusted_sources:
      - pypi
      - github.com/sage-kb
    
    # Hash verification
    verify_hash: true
    hash_algorithm: sha256
```

---

## Quick Reference

### Plugin Commands

```bash
# List plugins
sage plugin list
sage plugin list --all
sage plugin list --enabled

# Plugin info
sage plugin info <plugin_name>

# Enable/disable
sage plugin enable <plugin_name>
sage plugin disable <plugin_name>

# Install external plugin
sage plugin install <package_name>
sage plugin uninstall <package_name>

# Reload plugins
sage plugin reload
sage plugin reload <plugin_name>
```

### Plugin Development

```python
# plugins/my_plugin/plugin.py
from sage.plugins import Plugin, hook

class MyPlugin(Plugin):
    """Custom SAGE plugin."""
    
    name = "my_plugin"
    version = "1.0.0"
    
    def initialize(self) -> None:
        """Called when plugin is loaded."""
        self.logger.info("Plugin initialized")
    
    def shutdown(self) -> None:
        """Called when plugin is unloaded."""
        self.logger.info("Plugin shutdown")
    
    @hook("content.loaded")
    def on_content_loaded(self, content: str) -> str:
        """Hook into content loading."""
        return self.process(content)
```

### Configuration Validation

```bash
# Validate plugin configuration
sage plugin validate
sage plugin validate <plugin_name>

# Show plugin configuration
sage plugin config <plugin_name>
```

---

## Related

- `service_settings.md` — Service configuration
- `memory_settings.md` — Memory/persistence settings
- `.context/decisions/ADR-0008-plugin-system.md` — Plugin system ADR
- `.knowledge/scenarios/plugin_development/` — Plugin development guide

---

*Part of SAGE Knowledge Base - Configuration Reference*
