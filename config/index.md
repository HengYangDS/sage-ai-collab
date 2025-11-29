# Configuration Directory

> SAGE Knowledge Base runtime configuration files

---

## Table of Contents

[1. Overview](#1-overview) · [2. Directory Structure](#2-directory-structure) · [3. Configuration Files](#3-configuration-files) · [4. Configuration Hierarchy](#4-configuration-hierarchy)

---

## 1. Overview

This directory contains runtime configuration files for SAGE Knowledge Base. Configurations are organized into subdirectories by functional area:

| Subdirectory | Purpose |
|--------------|---------|
| `services/` | Service layer configurations (API, CLI, MCP) |
| `core/` | Core infrastructure (DI, logging, memory, timeout) |
| `knowledge/` | Knowledge base management (content, loading, triggers) |
| `capabilities/` | System capabilities (features, plugins, autonomy) |

---

## 2. Directory Structure

```
config/
├── sage.yaml           # Main configuration entry point
├── index.md            # This documentation
├── capabilities/       # Capability configurations
│   ├── autonomy.yaml   # Autonomy level settings
│   ├── documentation.yaml # Documentation generation
│   ├── features.yaml   # Feature flags
│   ├── plugins.yaml    # Plugin system
│   └── quality.yaml    # Quality checks
├── core/               # Core infrastructure
│   ├── di.yaml         # Dependency injection
│   ├── logging.yaml    # Logging configuration
│   ├── memory.yaml     # Memory persistence
│   └── timeout.yaml    # Timeout settings (T1-T5)
├── knowledge/          # Knowledge management
│   ├── content.yaml    # Content directories
│   ├── guidelines.yaml # Guidelines mapping
│   ├── loading.yaml    # Smart loading
│   ├── search.yaml     # Search configuration
│   ├── token_budget.yaml # Token budgets
│   └── triggers.yaml   # Keyword triggers
└── services/           # Service layer
    ├── api.yaml        # HTTP REST API
    ├── cli.yaml        # Command-line interface
    └── mcp.yaml        # MCP protocol
```

---

## 3. Configuration Files

### 3.1 Main Configuration

| File | Purpose |
|------|---------|
| `sage.yaml` | Main configuration entry point, imports other configs |

### 3.2 Services (`services/`)

| File | Purpose |
|------|---------|
| `api.yaml` | HTTP REST API service settings |
| `cli.yaml` | Command-line interface settings |
| `mcp.yaml` | MCP protocol service settings |

### 3.3 Core (`core/`)

| File | Purpose |
|------|---------|
| `di.yaml` | Dependency injection container settings |
| `logging.yaml` | Structured logging configuration |
| `memory.yaml` | Memory persistence settings |
| `timeout.yaml` | Timeout hierarchy (T1-T5) settings |

### 3.4 Knowledge (`knowledge/`)

| File | Purpose |
|------|---------|
| `content.yaml` | Content directory configuration |
| `guidelines.yaml` | Guidelines section mapping |
| `loading.yaml` | Smart loading strategies |
| `search.yaml` | Search functionality settings |
| `token_budget.yaml` | Token budget per layer |
| `triggers.yaml` | Keyword triggers for auto-loading |

### 3.5 Capabilities (`capabilities/`)

| File | Purpose |
|------|---------|
| `autonomy.yaml` | Autonomy level configuration |
| `documentation.yaml` | Documentation generation settings |
| `features.yaml` | Feature flags (enable/disable) |
| `plugins.yaml` | Plugin system configuration |
| `quality.yaml` | Quality check settings |

---

## 4. Configuration Hierarchy

Configuration values are resolved in this order (later overrides earlier):

| Priority | Source | Example |
|----------|--------|---------|
| 1 (lowest) | Default values | Built-in defaults |
| 2 | Config files | `config/**/*.yaml` |
| 3 | Environment variables | `SAGE_TIMEOUT_T1=100` |
| 4 (highest) | Runtime parameters | CLI arguments |

---

## Related

- `.context/configurations/` — Project-specific configuration documentation
- `docs/design/09-configuration.md` — Configuration design details

---

*Part of SAGE Knowledge Base - Configuration*
