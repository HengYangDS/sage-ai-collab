# YAML DSL

> Domain-specific language for SAGE configuration

---

## 1. Overview

SAGE uses YAML as its configuration DSL with custom extensions for expressions, references, and conditional logic.

---

## 2. Basic Syntax

### 2.1 Scalar Values

```yaml
# Strings
name: "SAGE"
path: /path/to/file

# Numbers
port: 8080
timeout_ms: 5000
ratio: 0.75

# Booleans
enabled: true
debug: false

# Null
optional_value: null
```

### 2.2 Collections

```yaml
# Lists
layers:
  - .knowledge
  - .context
  - .junie

# Maps
services:
  cli:
    format: rich
  api:
    port: 8080
```

---

## 3. DSL Extensions

### 3.1 Variable References

```yaml
# Define variables
_vars:
  base_timeout: 5000
  max_retries: 3

# Reference variables with ${}
timeout:
  default_ms: ${base_timeout}
  extended_ms: ${base_timeout * 2}

retries:
  count: ${max_retries}
```

### 3.2 Environment References

```yaml
# Reference environment variables with $env{}
database:
  host: ${env:DB_HOST}
  port: ${env:DB_PORT:5432}  # With default
  password: ${env:DB_PASSWORD}
```

### 3.3 File Includes

```yaml
# Include other config files
_include:
  - base.yaml
  - ${env:SAGE_ENV:development}.yaml

# Partial includes
services:
  _include: services/*.yaml
```

---

## 4. Conditional Logic

### 4.1 When Conditions

```yaml
services:
  api:
    port: 8080
    
    # Conditional based on environment
    _when:
      env: production
      _then:
        port: 443
        workers: 4
        ssl: true
```

### 4.2 If-Else

```yaml
logging:
  level: ${if:${env:DEBUG}:debug:info}
  
  # Expanded form
  _if: ${env:DEBUG}
  _then:
    level: debug
    verbose: true
  _else:
    level: info
```

---

## 5. Expressions

### 5.1 Arithmetic

```yaml
timeout:
  base_ms: 5000
  extended_ms: ${base_ms * 2}
  reduced_ms: ${base_ms / 2}
  with_buffer: ${base_ms + 1000}
```

### 5.2 String Operations

```yaml
paths:
  base: /opt/sage
  config: ${base}/config
  logs: ${base}/logs
  
names:
  full: ${first_name} ${last_name}
```

### 5.3 Built-in Functions

```yaml
# Available functions
computed:
  # String functions
  upper: ${upper(name)}
  lower: ${lower(NAME)}
  
  # Path functions
  dirname: ${dirname(file_path)}
  basename: ${basename(file_path)}
  
  # Default
  value: ${default(optional, "fallback")}
```

---

## 6. Type Coercion

### 6.1 Explicit Types

```yaml
# Force specific types
settings:
  port: !int "8080"
  enabled: !bool "true"
  ratio: !float "0.75"
  items: !list "a,b,c"
```

### 6.2 Auto-detection

| Pattern | Detected Type |
|---------|---------------|
| `123` | Integer |
| `12.34` | Float |
| `true/false` | Boolean |
| `[a, b]` | List |
| `{a: 1}` | Map |

---

## 7. Validation Rules

### 7.1 Schema Annotations

```yaml
# Define schema inline
timeout:
  default_ms:
    _type: integer
    _min: 100
    _max: 60000
    _default: 5000
    _description: "Default timeout in milliseconds"
```

### 7.2 Required Fields

```yaml
database:
  host:
    _required: true
    _type: string
  
  port:
    _required: false
    _default: 5432
```

### 7.3 Pattern Validation

```yaml
naming:
  file_pattern:
    _type: string
    _pattern: "^[A-Z_]+\\.md$"
    _description: "Must be UPPER_SNAKE_CASE.md"
```

---

## 8. Secrets Handling

### 8.1 Secret References

```yaml
# Reference secrets (never stored in plain text)
database:
  password: ${secret:db_password}
  
api:
  key: ${secret:api_key}
```

### 8.2 Vault Integration

```yaml
secrets:
  provider: vault
  path: secret/sage
  
  # Or file-based
  provider: file
  path: ~/.sage/secrets.yaml
```

---

## 9. Profiles

### 9.1 Profile Definition

```yaml
_profiles:
  development:
    debug: true
    logging:
      level: debug
  
  production:
    debug: false
    logging:
      level: warning

# Active profile
_active_profile: ${env:SAGE_PROFILE:development}
```

### 9.2 Profile Inheritance

```yaml
_profiles:
  base:
    timeout_ms: 5000
  
  production:
    _extends: base
    timeout_ms: 10000
```

---

## 10. Examples

### 10.1 Complete Configuration

```yaml
# sage.yaml
_vars:
  base_timeout: 5000

sage:
  knowledge:
    layers:
      - .knowledge
      - .context
    token_budget: 6000
  
  timeout:
    default_ms: ${base_timeout}
    max_ms: ${base_timeout * 6}
  
  services:
    cli:
      format: ${env:SAGE_FORMAT:rich}
    api:
      port: ${env:SAGE_PORT:8080}
      _when:
        env: production
        _then:
          port: 443
```

---

## Related

- `CONFIG_HIERARCHY.md` — Configuration levels
- `CONFIG_REFERENCE.md` — Full reference
- `.knowledge/practices/engineering/YAML_CONVENTIONS.md` — YAML best practices

---

*AI Collaboration Knowledge Base*
