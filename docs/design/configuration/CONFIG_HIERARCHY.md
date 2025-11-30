# Configuration Hierarchy

> Multi-level configuration system for SAGE

---

## 1. Overview

SAGE uses a hierarchical configuration system where settings cascade from defaults through environment-specific overrides to runtime values.

---

## 2. Hierarchy Levels

```
Priority (highest to lowest):

1. Runtime      → Command line, environment variables
2. User         → ~/.sage/config.yaml
3. Project      → .sage/config.yaml
4. Environment  → config/{env}.yaml
5. Default      → Built-in defaults
```

---

## 3. Configuration Sources

| Level | Source | Scope | Priority |
|-------|--------|-------|----------|
| **Runtime** | CLI args, env vars | Session | ★★★★★ |
| **User** | ~/.sage/config.yaml | User | ★★★★☆ |
| **Project** | .sage/config.yaml | Project | ★★★☆☆ |
| **Environment** | config/{env}.yaml | Deployment | ★★☆☆☆ |
| **Default** | Built-in | Global | ★☆☆☆☆ |

---

## 4. Resolution Algorithm

```python
class ConfigResolver:
    def resolve(self, key: str) -> Any:
        # Check sources in priority order
        sources = [
            self.runtime_config,
            self.user_config,
            self.project_config,
            self.env_config,
            self.default_config,
        ]
        
        for source in sources:
            value = source.get(key)
            if value is not None:
                return value
        
        return None
```

---

## 5. Configuration Files

### 5.1 Default Configuration

```yaml
# Built-in defaults (sage/config/defaults.yaml)
sage:
  version: "1.0.0"
  
  knowledge:
    layers:
      - .knowledge
      - .context
      - .junie
      - docs
    token_budget: 6000
  
  timeout:
    default_ms: 5000
    max_ms: 30000
  
  services:
    cli:
      format: rich
    mcp:
      transport: stdio
    api:
      port: 8080
```

### 5.2 Environment Configuration

```yaml
# config/production.yaml
sage:
  timeout:
    default_ms: 10000
  
  services:
    api:
      port: 443
      workers: 4
  
  logging:
    level: warning
```

### 5.3 Project Configuration

```yaml
# .sage/config.yaml
sage:
  knowledge:
    token_budget: 8000
  
  scenarios:
    default: python_backend
```

### 5.4 User Configuration

```yaml
# ~/.sage/config.yaml
sage:
  services:
    cli:
      format: json
  
  preferences:
    theme: dark
```

---

## 6. Environment Variables

### 6.1 Naming Convention

```
SAGE_{SECTION}_{KEY}

Examples:
SAGE_TIMEOUT_DEFAULT_MS=10000
SAGE_SERVICES_API_PORT=8080
SAGE_KNOWLEDGE_TOKEN_BUDGET=6000
```

### 6.2 Type Conversion

| Type | Format | Example |
|------|--------|---------|
| String | As-is | `SAGE_ENV=production` |
| Integer | Numeric | `SAGE_PORT=8080` |
| Boolean | true/false | `SAGE_DEBUG=true` |
| List | Comma-separated | `SAGE_LAYERS=.knowledge,.context` |

---

## 7. CLI Arguments

```bash
sage get --timeout 5000 --format json --layer 2

# Maps to:
# timeout.default_ms = 5000
# services.cli.format = json
# knowledge.default_layer = 2
```

---

## 8. Merge Strategy

### 8.1 Deep Merge

```python
def deep_merge(base: dict, override: dict) -> dict:
    result = base.copy()
    
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    
    return result
```

### 8.2 Merge Example

```yaml
# Base (default)
services:
  api:
    port: 8080
    workers: 2

# Override (project)
services:
  api:
    workers: 4

# Result
services:
  api:
    port: 8080    # From base
    workers: 4    # From override
```

---

## 9. Validation

### 9.1 Schema Validation

```python
from pydantic import BaseModel

class TimeoutConfig(BaseModel):
    default_ms: int = 5000
    max_ms: int = 30000
    
    @validator('default_ms')
    def validate_default(cls, v):
        if v < 100 or v > 60000:
            raise ValueError('default_ms must be 100-60000')
        return v
```

### 9.2 Validation Errors

```python
class ConfigValidator:
    def validate(self, config: dict) -> list[ConfigError]:
        errors = []
        
        # Required fields
        for field in self.required_fields:
            if field not in config:
                errors.append(ConfigError(f"Missing required: {field}"))
        
        # Type checks
        for field, expected_type in self.type_rules.items():
            if field in config and not isinstance(config[field], expected_type):
                errors.append(ConfigError(f"Invalid type for {field}"))
        
        return errors
```

---

## 10. Configuration API

### 10.1 Access Configuration

```python
from sage.config import get_config

config = get_config()

# Get with default
timeout = config.get("timeout.default_ms", default=5000)

# Get required
port = config.require("services.api.port")

# Get section
services = config.section("services")
```

### 10.2 Runtime Updates

```python
# Temporary override
with config.override({"timeout.default_ms": 10000}):
    # Uses overridden value
    result = do_operation()
# Original value restored
```

---

## 11. Configuration

```yaml
# Meta-configuration for the config system itself
config:
  sources:
    - type: default
      enabled: true
    - type: environment
      path: config/{env}.yaml
    - type: project
      path: .sage/config.yaml
    - type: user
      path: ~/.sage/config.yaml
    - type: env_vars
      prefix: SAGE_
  
  validation:
    strict: true
    fail_on_unknown: false
  
  caching:
    enabled: true
    ttl_seconds: 300
```

---

## Related

- `YAML_DSL.md` — Configuration DSL
- `CONFIG_REFERENCE.md` — Full reference
- `../core_engine/BOOTSTRAP.md` — Startup configuration

---

*AI Collaboration Knowledge Base*
