# Service Layer Configuration

> Configuration reference for CLI, MCP, and API services

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. CLI Service](#2-cli-service)
- [3. MCP Service](#3-mcp-service)
- [4. API Service](#4-api-service)
- [5. Common Settings](#5-common-settings)

---

## 1. Overview

### 1.1 Service Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Service Layer                          │
├─────────────────┬─────────────────┬─────────────────────────┤
│   CLI Service   │   MCP Service   │      API Service        │
│   (Typer+Rich)  │   (FastMCP)     │    (FastAPI+Uvicorn)    │
└────────┬────────┴────────┬────────┴────────────┬────────────┘
         │                 │                      │
         └─────────────────┴──────────────────────┘
                           │
                    ┌──────▼──────┐
                    │  Core Layer │
                    └─────────────┘
```

### 1.2 Configuration Locations

| Service | Config Key     | Environment Variable |
|---------|----------------|----------------------|
| CLI     | `services.cli` | `SAGE_CLI_*`         |
| MCP     | `services.mcp` | `SAGE_MCP_*`         |
| API     | `services.api` | `SAGE_API_*`         |

---

## 2. CLI Service

### 2.1 Configuration Schema

```yaml
# config/sage.yaml
services:
  cli:
    # Output settings
    output:
      format: rich          # rich | plain | json
      color: auto           # auto | always | never
      width: null           # Terminal width (null = auto)
    
    # Progress display
    progress:
      enabled: true
      style: bar            # bar | spinner | dots
    
    # History
    history:
      enabled: true
      max_entries: 1000
      path: ~/.sage/history
    
    # Aliases
    aliases:
      g: get
      s: search
      i: info
```

### 2.2 Output Formats

| Format  | Use Case             | Example                   |
|---------|----------------------|---------------------------|
| `rich`  | Interactive terminal | Colored, formatted output |
| `plain` | Piping, scripts      | Plain text                |
| `json`  | Programmatic use     | JSON output               |

### 2.3 Environment Variables

```bash
# Output
export SAGE_CLI_FORMAT=json
export SAGE_CLI_COLOR=never
export SAGE_CLI_WIDTH=120

# History
export SAGE_CLI_HISTORY_ENABLED=false
export SAGE_CLI_HISTORY_PATH=/custom/path
```

---

## 3. MCP Service

### 3.1 Configuration Schema

```yaml
# config/sage.yaml
services:
  mcp:
    # Server settings
    server:
      name: sage-kb
      version: "0.1.0"
      transport: stdio      # stdio | sse | websocket
    
    # Connection
    connection:
      host: localhost
      port: 8080
      timeout: 30000        # ms
    
    # Tools registration
    tools:
      enabled:
        - get_knowledge
        - search_content
        - get_layer
        - get_info
      disabled: []
    
    # Resources
    resources:
      expose_content: true
      max_content_size: 100000  # bytes
    
    # Prompts
    prompts:
      enabled: true
      custom_prompts_path: config/prompts/
```

### 3.2 Transport Types

| Transport   | Use Case          | Configuration       |
|-------------|-------------------|---------------------|
| `stdio`     | Local integration | Default, no network |
| `sse`       | Web clients       | Requires host/port  |
| `websocket` | Real-time apps    | Requires host/port  |

### 3.3 Tool Configuration

```yaml
# Detailed tool settings
services:
  mcp:
    tools:
      get_knowledge:
        enabled: true
        timeout: 5000
        cache: true
      
      search_content:
        enabled: true
        timeout: 10000
        max_results: 50
```

### 3.4 Environment Variables

```bash
# Server
export SAGE_MCP_TRANSPORT=stdio
export SAGE_MCP_HOST=localhost
export SAGE_MCP_PORT=8080

# Tools
export SAGE_MCP_TOOLS_ENABLED=get_knowledge,search_content
```

---

## 4. API Service

### 4.1 Configuration Schema

```yaml
# config/sage.yaml
services:
  api:
    # Server settings
    server:
      host: 0.0.0.0
      port: 8000
      workers: 4
      reload: false         # Development only
    
    # CORS
    cors:
      enabled: true
      origins:
        - "http://localhost:3000"
        - "https://example.com"
      methods: ["GET", "POST"]
      headers: ["*"]
    
    # Rate limiting
    rate_limit:
      enabled: true
      requests_per_minute: 60
      burst: 10
    
    # Authentication
    auth:
      enabled: false
      type: api_key         # api_key | jwt | oauth2
      api_key_header: X-API-Key
    
    # Documentation
    docs:
      enabled: true
      path: /docs
      redoc_path: /redoc
```

### 4.2 Uvicorn Settings

```yaml
services:
  api:
    uvicorn:
      log_level: info
      access_log: true
      timeout_keep_alive: 5
      limit_concurrency: 100
      limit_max_requests: 10000
```

### 4.3 Environment Variables

```bash
# Server
export SAGE_API_HOST=0.0.0.0
export SAGE_API_PORT=8000
export SAGE_API_WORKERS=4

# Security
export SAGE_API_CORS_ORIGINS=http://localhost:3000
export SAGE_API_AUTH_ENABLED=true
export SAGE_API_KEY=your-secret-key

# Rate limiting
export SAGE_API_RATE_LIMIT=60
```

---

## 5. Common Settings

### 5.1 Logging Configuration

```yaml
# Applies to all services
services:
  logging:
    level: INFO             # DEBUG | INFO | WARNING | ERROR
    format: json            # json | text
    output: file            # file | stdout | both
    file:
      path: .logs/sage.log
      max_size: 10MB
      backup_count: 5
      rotation: daily
```

### 5.2 Metrics Configuration

```yaml
services:
  metrics:
    enabled: true
    endpoint: /metrics
    include:
      - request_count
      - request_latency
      - error_rate
      - cache_hits
```

### 5.3 Health Check Configuration

```yaml
services:
  health:
    enabled: true
    endpoint: /health
    checks:
      - name: knowledge_base
        type: path_exists
        path: content/
      - name: config
        type: file_valid
        path: config/sage.yaml
```

---

## Quick Reference

### Service Startup Commands

```bash
# CLI (default)
sage get --layer core

# MCP Server
sage serve --transport stdio
sage serve --port 8080 --transport sse

# API Server
sage api --host 0.0.0.0 --port 8000
sage api --workers 4 --reload
```

### Configuration Priority

```
1. Command-line arguments (highest)
2. Environment variables
3. Config file (config/sage.yaml)
4. Defaults (lowest)
```

### Validation

```bash
# Validate service configuration
sage config --validate --section services

# Show service configuration
sage config --show --section services.mcp
```

---

## Related

- `runtime_settings.md` — Runtime configuration
- `timeout_hierarchy.md` — Timeout configuration
- `docs/api/` — API documentation
- `docs/api/mcp.md` — MCP protocol reference

---

*Part of SAGE Knowledge Base - Configuration Reference*
