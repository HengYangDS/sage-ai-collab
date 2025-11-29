# ADR-0007: Configuration Management

> Architecture Decision Record for SAGE Knowledge Base

---

## Status

**Accepted** | Date: 2025-11-28

---

## Context

SAGE Knowledge Base requires flexible configuration that:

1. Supports multiple environments (development, production)
2. Allows runtime overrides without code changes
3. Validates configuration at startup
4. Provides sensible defaults
5. Is human-readable and editable

### Requirements

- YAML-based configuration files
- Environment variable overrides
- Type-safe configuration access
- Validation with clear error messages
- Hierarchical configuration structure

---

## Decision

Implement a **YAML + Environment Variable** configuration system with Pydantic validation.

### Configuration Hierarchy

```
┌─────────────────────────────────────────────────────────┐
│ 1. Environment Variables (SAGE__*)     [Highest Priority]│
├─────────────────────────────────────────────────────────┤
│ 2. Command-line Arguments                               │
├─────────────────────────────────────────────────────────┤
│ 3. sage.yaml (project root)                             │
├─────────────────────────────────────────────────────────┤
│ 4. config/*.yaml (additional configs)                   │
├─────────────────────────────────────────────────────────┤
│ 5. Default Values in Code               [Lowest Priority]│
└─────────────────────────────────────────────────────────┘
```

Higher priority sources override lower priority sources.

### Configuration Files

```
project/
├── sage.yaml              # Main configuration
└── config/
    ├── core/
    │   └── logging.yaml   # Logging config
    ├── services/
    │   ├── cli.yaml       # CLI service config
    │   ├── mcp.yaml       # MCP service config
    │   └── api.yaml       # API service config
    └── knowledge/
        └── layers.yaml    # Knowledge layer config
```

---

## Alternatives Considered

### Alternative 1: JSON Configuration

Use JSON for configuration files.

- **Pros**: Widely supported, strict syntax
- **Cons**: No comments, verbose, less readable
- **Rejected**: YAML more human-friendly

### Alternative 2: TOML Configuration

Use TOML format.

- **Pros**: Clean syntax, Python standard (pyproject.toml)
- **Cons**: Less suitable for deep nesting
- **Rejected**: YAML better for hierarchical config

### Alternative 3: Python Config Files

Use Python files for configuration.

- **Pros**: Full Python power, type checking
- **Cons**: Security concerns, harder for non-developers
- **Rejected**: Need non-code configuration

### Alternative 4: Environment Only

All configuration via environment variables.

- **Pros**: 12-factor compliant, simple
- **Cons**: Hard to manage complex config, no structure
- **Rejected**: Need structured configuration

---

## Consequences

### Positive

1. **Readability**: YAML is human-readable
2. **Flexibility**: Multiple override mechanisms
3. **Type safety**: Pydantic validation
4. **Documentation**: Config file serves as documentation
5. **Environment support**: Easy deployment customization

### Negative

1. **Complexity**: Multiple config sources to understand
2. **Debugging**: May be unclear which source applies
3. **YAML pitfalls**: Boolean/string ambiguity

### Mitigations

1. **Logging**: Log effective configuration at startup
2. **Validation**: Clear errors for invalid config
3. **Schema**: Document expected structure

---

## Implementation

### Main Configuration (sage.yaml)

```yaml
# SAGE Knowledge Base Configuration
sage:
  version: "0.1.0"
  name: "SAGE Knowledge Base"

# Timeout configuration
timeout:
  operations:
    cache_lookup: 100ms
    file_read: 500ms
    layer_load: 2s
    full_load: 5s
    analysis: 10s
  fallback:
    strategy: graceful

# Knowledge configuration
knowledge:
  base_path: .knowledge/
  layers:
    - name: core
      path: core/
      priority: 1
    - name: frameworks
      path: frameworks/
      priority: 2
    - name: practices
      path: practices/
      priority: 3

# Logging configuration
logging:
  level: INFO
  format: json
  output: stderr

# Feature flags
features:
  enable_caching: true
  enable_metrics: true
```

### Pydantic Configuration Model

```python
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class TimeoutConfig(BaseModel):
    cache_lookup: int = Field(default=100, ge=10)
    file_read: int = Field(default=500, ge=50)
    layer_load: int = Field(default=2000, ge=500)
    full_load: int = Field(default=5000, ge=1000)
    analysis: int = Field(default=10000, ge=2000)


class SAGEConfig(BaseSettings):
    version: str = "0.1.0"
    timeout: TimeoutConfig = TimeoutConfig()

    class Config:
        env_prefix = "SAGE__"
        env_nested_delimiter = "__"
```

### Environment Variable Override

```bash
# Override timeout.cache_lookup
export SAGE__TIMEOUT__CACHE_LOOKUP=200

# Override logging.level
export SAGE__LOGGING__LEVEL=DEBUG

# Override feature flag
export SAGE__FEATURES__ENABLE_CACHING=false
```

### Configuration Access

```python
from sage.core.config import get_config

# Get global config (singleton)
config = get_config()

# Access values
timeout = config.timeout.cache_lookup
layers = config.knowledge.layers
```

### Configuration Loading

```python
def load_config(config_path: str | None = None) -> SAGEConfig:
    """Load configuration with hierarchy."""
    # 1. Start with defaults
    config_dict = {}

    # 2. Load from YAML files
    if config_path:
        yaml_config = load_yaml(config_path)
        config_dict = deep_merge(config_dict, yaml_config)

    # 3. Environment variables applied by Pydantic
    return SAGEConfig(**config_dict)
```

### Validation Errors

```python
from pydantic import ValidationError

try:
    config = load_config("sage.yaml")
except ValidationError as e:
    for error in e.errors():
        print(f"Config error: {error['loc']} - {error['msg']}")
```

### Runtime Configuration

```python
# Check feature flags
if config.features.enable_caching:
    cache = initialize_cache()

# Dynamic timeout selection
level = TimeoutLevel(config.timeout.cache_lookup)
```

---

## Related

- `ADR-0003-timeout-hierarchy.md` — Timeout configuration
- `.context/policies/` — Configuration documentation
- `docs/design/09-configuration.md` — Full configuration design
- `config/` — Configuration files

---

*Part of SAGE Knowledge Base - Architecture Decisions*
