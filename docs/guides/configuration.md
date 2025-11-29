# Configuration Guide

> Complete reference for SAGE Knowledge Base configuration options

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Configuration Files](#2-configuration-files)
- [3. Core Settings](#3-core-settings)
- [4. Knowledge Settings](#4-knowledge-settings)
- [5. Service Settings](#5-service-settings)
- [6. Environment Variables](#6-environment-variables)
- [7. Advanced Configuration](#7-advanced-configuration)
- [8. Configuration Recipes](#8-configuration-recipes)

---

## 1. Overview

### 1.1 Configuration Philosophy

| Principle      | Description                          |
|----------------|--------------------------------------|
| **Modular**    | Split by concern into separate files |
| **Layered**    | Defaults → File → Environment        |
| **Validated**  | Schema-based validation              |
| **Documented** | Self-documenting with comments       |

### 1.2 Configuration Hierarchy

```
Priority (highest to lowest):
1. Environment variables (SAGE_*)
2. config/*.yaml files
3. Built-in defaults
```

### 1.3 Directory Structure

```
config/
├── sage.yaml              # Main config (optional override)
├── index.md               # Config documentation
├── core/                  # Core system settings
│   ├── timeout.yaml       # Timeout configuration
│   ├── logging.yaml       # Logging configuration
│   ├── memory.yaml        # Memory settings
│   ├── security.yaml      # Security settings
│   └── di.yaml            # Dependency injection
├── knowledge/             # Knowledge base settings
│   ├── loading.yaml       # Loading configuration
│   ├── content.yaml       # Content settings
│   ├── triggers.yaml      # Auto-load triggers
│   ├── search.yaml        # Search configuration
│   ├── guidelines.yaml    # Guidelines config
│   └── token_budget.yaml  # Token limits
├── services/              # Service configurations
│   ├── cli.yaml           # CLI settings
│   ├── mcp.yaml           # MCP server settings
│   └── api.yaml           # API settings
├── capabilities/          # Feature configurations
│   ├── autonomy.yaml      # Autonomy levels
│   ├── quality.yaml       # Quality settings
│   ├── plugins.yaml       # Plugin config
│   ├── features.yaml      # Feature flags
│   └── documentation.yaml # Doc settings
└── environments/          # Environment-specific
    ├── development.yaml
    ├── testing.yaml
    └── production.yaml
```

---

## 2. Configuration Files

### 2.1 Main Configuration (sage.yaml)

```yaml
# config/sage.yaml
# Main configuration file - overrides modular configs

# Project identification
project:
  name: "my-project"
  version: "1.0.0"

# Include other configs (optional)
includes:
  - core/timeout.yaml
  - knowledge/loading.yaml

# Override specific values
timeout:
  default_ms: 5000

knowledge:
  content_path: "./content"
```

### 2.2 Loading Configuration

Configuration is loaded in this order:

1. Load `config/sage.yaml` if exists
2. Load modular configs from subdirectories
3. Apply environment variable overrides
4. Validate against schemas

```python
from sage.core.config import load_config

# Load all configuration
config = load_config()

# Load specific section
timeout_config = load_config("core/timeout")
```

---

## 3. Core Settings

### 3.1 Timeout Configuration

**File**: `config/core/timeout.yaml`

```yaml
# Timeout levels in milliseconds
levels:
  T1: 100      # Cache lookup
  T2: 500      # Single file read
  T3: 2000     # Layer load
  T4: 5000     # Full KB load
  T5: 10000    # Complex analysis

# Default timeout level
default: T3

# Operation-specific timeouts
operations:
  cache_lookup: T1
  file_read: T2
  layer_load: T3
  full_load: T4
  analysis: T5
  search: T3

# Timeout behavior
behavior:
  # Action when timeout occurs
  on_timeout: "fallback"  # fallback | error | partial

  # Enable timeout statistics
  track_stats: true

  # Warning threshold (percentage of timeout)
  warning_threshold: 0.8
```

### 3.2 Logging Configuration

**File**: `config/core/logging.yaml`

```yaml
# Default log level
default_level: INFO  # DEBUG | INFO | WARNING | ERROR

# Log format
format: "structured"  # structured | simple | json

# Log destinations
outputs:
  console:
    enabled: true
    level: INFO
    format: simple

  file:
    enabled: true
    path: ".logs/sage.log"
    level: DEBUG
    max_size_mb: 10
    backup_count: 5

  error_file:
    enabled: true
    path: ".logs/error.log"
    level: ERROR

# Module-specific levels
modules:
  sage.core.loader: DEBUG
  sage.services.mcp_server: INFO
  sage.core.timeout: WARNING

# Sensitive field redaction
redact_fields:
  - password
  - api_key
  - token
  - secret
```

### 3.3 Memory Configuration

**File**: `config/core/memory.yaml`

```yaml
# Memory limits
limits:
  max_cache_mb: 100
  max_content_mb: 50
  warning_threshold: 0.8

# Cache settings
cache:
  enabled: true
  ttl_seconds: 300
  max_items: 1000
  eviction_policy: "lru"  # lru | lfu | fifo

# Memory monitoring
monitoring:
  enabled: true
  check_interval_seconds: 60
  alert_on_high_usage: true
```

### 3.4 Security Configuration

**File**: `config/core/security.yaml`

```yaml
# Authentication
authentication:
  enabled: false
  method: "api_key"  # api_key | jwt | oauth2

# API key settings (if enabled)
api_keys:
  header_name: "X-API-Key"
  # Keys loaded from environment: SAGE_API_KEYS

# Rate limiting
rate_limiting:
  enabled: true
  requests_per_minute: 100
  burst_size: 20

# CORS settings
cors:
  enabled: true
  allow_origins: [ "*" ]
  allow_methods: [ "GET", "POST" ]
  allow_headers: [ "Authorization", "Content-Type" ]

# Content security
content:
  sanitize_html: true
  max_file_size_mb: 10
```

---

## 4. Knowledge Settings

### 4.1 Loading Configuration

**File**: `config/knowledge/loading.yaml`

```yaml
# Content paths
paths:
  content: "./content"
  context: "./.context"
  templates: "./content/templates"

# Layer definitions
layers:
  - name: core
    priority: 0
    auto_load: true
    paths:
      - content/core

  - name: guidelines
    priority: 1
    auto_load: true
    paths:
      - content/guidelines

  - name: frameworks
    priority: 2
    auto_load: false
    paths:
      - content/frameworks

  - name: practices
    priority: 3
    auto_load: false
    paths:
      - content/practices

# Loading behavior
behavior:
  lazy_load: true
  parallel_load: true
  max_parallel: 4

# File patterns
patterns:
  include:
    - "**/*.md"
    - "**/*.yaml"
    - "**/*.json"
  exclude:
    - "**/node_modules/**"
    - "**/.git/**"
    - "**/.*"
```

### 4.2 Content Configuration

**File**: `config/knowledge/content.yaml`

```yaml
# File handling
files:
  max_size_kb: 500
  encoding: "utf-8"

# Markdown processing
markdown:
  extract_frontmatter: true
  extract_headings: true
  extract_links: true

# Content validation
validation:
  require_frontmatter: false
  require_title: true
  max_heading_depth: 4

# Content indexing
indexing:
  enabled: true
  fields:
    - title
    - tags
    - content
```

### 4.3 Triggers Configuration

**File**: `config/knowledge/triggers.yaml`

```yaml
# Task-based triggers
task_triggers:
  - pattern: "auth|login|security"
    load:
      - content/practices/engineering/security.md
      - content/frameworks/patterns/authentication.md

  - pattern: "test|testing"
    load:
      - content/practices/engineering/testing_strategy.md

  - pattern: "api|endpoint"
    load:
      - content/practices/engineering/api_design.md
      - content/templates/api_spec.md

# File-based triggers
file_triggers:
  - pattern: "*.test.py"
    load:
      - content/practices/engineering/testing_strategy.md

  - pattern: "*.yaml"
    load:
      - content/practices/engineering/yaml_conventions.md

# Context triggers
context_triggers:
  - condition: "new_session"
    load:
      - content/core/quick_reference.md
```

### 4.4 Token Budget Configuration

**File**: `config/knowledge/token_budget.yaml`

```yaml
# Token limits by context
limits:
  default: 8000
  minimal: 2000
  standard: 8000
  extended: 16000
  maximum: 32000

# Layer allocations (percentage of budget)
allocations:
  core: 20
  guidelines: 30
  frameworks: 25
  practices: 15
  context: 10

# Overflow handling
overflow:
  strategy: "truncate"  # truncate | summarize | error
  preserve_structure: true
  min_content_ratio: 0.5
```

---

## 5. Service Settings

### 5.1 CLI Configuration

**File**: `config/services/cli.yaml`

```yaml
# Output settings
output:
  format: "rich"  # rich | plain | json
  color: true
  width: auto

# Default command options
defaults:
  layer: 0
  timeout_ms: 5000
  max_results: 10

# Progress display
progress:
  show_spinner: true
  show_elapsed: true
```

### 5.2 MCP Server Configuration

**File**: `config/services/mcp.yaml`

```yaml
# Server settings
server:
  name: "sage-kb"
  version: "0.1.0"

# Transport
transport:
  type: "stdio"  # stdio | sse | websocket

# SSE settings (if type: sse)
sse:
  host: "127.0.0.1"
  port: 8080

# Tool configuration
tools:
  enabled:
    - get_knowledge
    - search_knowledge
    - kb_info
    - get_guidelines
    - get_framework
    - get_template
    - list_tools
    # Capability tools
    - analyze_quality
    - analyze_content
    - check_health
    # Dev tools
    - build_knowledge_graph
    - check_links
    - check_structure
    - get_timeout_stats
    - create_backup
    - list_backups

# Request handling
requests:
  timeout_ms: 30000
  max_concurrent: 10
```

### 5.3 API Configuration

**File**: `config/services/api.yaml`

```yaml
# Server settings
server:
  host: "127.0.0.1"
  port: 8000
  workers: 4

# API versioning
versioning:
  current: "v1"
  supported: [ "v1" ]

# Endpoints
endpoints:
  knowledge: "/api/v1/knowledge"
  search: "/api/v1/search"
  health: "/health"

# Documentation
docs:
  enabled: true
  path: "/docs"
  openapi_path: "/openapi.json"
```

---

## 6. Environment Variables

### 6.1 Core Variables

| Variable            | Description            | Default     |
|---------------------|------------------------|-------------|
| `SAGE_CONFIG_PATH`  | Config directory path  | `./config`  |
| `SAGE_CONTENT_PATH` | Content directory path | `./content` |
| `SAGE_LOG_LEVEL`    | Log level              | `INFO`      |
| `SAGE_LOG_PATH`     | Log file path          | `./.logs`   |

### 6.2 Timeout Variables

| Variable               | Description          | Default |
|------------------------|----------------------|---------|
| `SAGE_TIMEOUT_DEFAULT` | Default timeout (ms) | `5000`  |
| `SAGE_TIMEOUT_T1`      | T1 timeout (ms)      | `100`   |
| `SAGE_TIMEOUT_T2`      | T2 timeout (ms)      | `500`   |
| `SAGE_TIMEOUT_T3`      | T3 timeout (ms)      | `2000`  |
| `SAGE_TIMEOUT_T4`      | T4 timeout (ms)      | `5000`  |
| `SAGE_TIMEOUT_T5`      | T5 timeout (ms)      | `10000` |

### 6.3 Service Variables

| Variable             | Description        | Default     |
|----------------------|--------------------|-------------|
| `SAGE_MCP_TRANSPORT` | MCP transport type | `stdio`     |
| `SAGE_MCP_PORT`      | MCP SSE port       | `8080`      |
| `SAGE_API_PORT`      | API server port    | `8000`      |
| `SAGE_API_HOST`      | API server host    | `127.0.0.1` |

### 6.4 Security Variables

| Variable            | Description          | Default |
|---------------------|----------------------|---------|
| `SAGE_API_KEY`      | API key for auth     | -       |
| `SAGE_JWT_SECRET`   | JWT signing secret   | -       |
| `SAGE_CORS_ORIGINS` | CORS allowed origins | `*`     |

---

## 7. Advanced Configuration

### 7.1 Environment-Specific Configuration

**Development** (`config/environments/development.yaml`):

```yaml
extends: base

logging:
  default_level: DEBUG

timeout:
  default: T4  # More lenient

features:
  debug_mode: true
  hot_reload: true
```

**Production** (`config/environments/production.yaml`):

```yaml
extends: base

logging:
  default_level: WARNING

timeout:
  default: T3  # Stricter

security:
  authentication:
    enabled: true
  rate_limiting:
    enabled: true

features:
  debug_mode: false
```

### 7.2 Dynamic Configuration

```python
from sage.core.config import ConfigManager

config = ConfigManager()

# Watch for changes
config.watch("config/", on_change=reload_handler)

# Update at runtime
config.set("timeout.default_ms", 3000)

# Get with fallback
timeout = config.get("timeout.default_ms", default=5000)
```

### 7.3 Configuration Validation

```bash
# Validate all configs
sage config validate

# Validate specific file
sage config validate --file config/core/timeout.yaml

# Show effective configuration
sage config show

# Show specific section
sage config show --section timeout
```

---

## 8. Configuration Recipes

### 8.1 Minimal Configuration

For simple projects:

```yaml
# config/sage.yaml
project:
  name: "my-project"

timeout:
  default_ms: 5000

knowledge:
  content_path: "./content"
```

### 8.2 High-Performance Configuration

For large knowledge bases:

```yaml
# config/sage.yaml
timeout:
  levels:
    T3: 3000
    T4: 8000

knowledge:
  loading:
    lazy_load: true
    parallel_load: true
    max_parallel: 8

cache:
  enabled: true
  max_mb: 200
  ttl_seconds: 600
```

### 8.3 Secure Production Configuration

```yaml
# config/sage.yaml
security:
  authentication:
    enabled: true
    method: jwt
  rate_limiting:
    enabled: true
    requests_per_minute: 60
  cors:
    allow_origins:
      - "https://app.example.com"

logging:
  default_level: WARNING
  redact_fields:
    - password
    - token
    - api_key
```

### 8.4 Development Configuration

```yaml
# config/sage.yaml
logging:
  default_level: DEBUG
  outputs:
    console:
      format: simple

timeout:
  default_ms: 10000  # Lenient for debugging

features:
  hot_reload: true
  debug_endpoints: true
```

---

## Quick Reference

### Configuration Commands

```bash
sage config validate          # Validate configuration
sage config show              # Show effective config
sage config show --section X  # Show specific section
sage config reset             # Reset to defaults
sage config migrate           # Migrate config version
```

### Common Overrides

```bash
# Set log level
export SAGE_LOG_LEVEL=DEBUG

# Set timeout
export SAGE_TIMEOUT_DEFAULT=10000

# Set content path
export SAGE_CONTENT_PATH=/path/to/content
```

---

## Related

- `.context/policies/` — Project-specific config docs
- `.context/decisions/ADR-0007-configuration.md` — Config architecture
- `docs/guides/faq.md` — Configuration FAQ
- `content/practices/engineering/yaml_conventions.md` — YAML best practices

---

*Part of SAGE Knowledge Base — 信达雅 (Xin-Da-Ya)*
