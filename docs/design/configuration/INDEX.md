# Configuration

> Configuration system design for SAGE

---

## 1. Overview

The configuration system provides flexible, hierarchical configuration management for SAGE.

---

## 2. Documents

| Document | Description | Status |
|----------|-------------|--------|
| `CONFIG_HIERARCHY.md` | Configuration hierarchy and precedence | Planned |
| `YAML_DSL.md` | YAML configuration DSL | Planned |
| `CONFIG_REFERENCE.md` | Complete configuration reference | Planned |

---

## 3. Configuration Hierarchy

Priority (highest to lowest):

```mermaid
graph TD
    CLI["1. Command-line arguments"]
    ENV["2. Environment variables (SAGE_*)"]
    USER["3. User config (~/.sage/config.yaml)"]
    PROJECT["4. Project config (./sage.yaml)"]
    DEFAULT["5. Default values (built-in)"]
    
    CLI --> ENV --> USER --> PROJECT --> DEFAULT
```

---

## 4. Configuration Categories

| Category | Purpose | Example |
|----------|---------|---------|
| **Core** | Core settings | `sage.version` |
| **Timeout** | Timeout hierarchy | `timeout.cache_lookup` |
| **Loading** | Knowledge loading | `loading.strategy` |
| **Plugins** | Plugin settings | `plugins.enabled` |
| **Services** | Service config | `services.mcp.port` |

---

## 5. Environment Variables

| Pattern | Example | Description |
|---------|---------|-------------|
| `SAGE_*` | `SAGE_CONFIG_PATH` | Basic settings |
| `SAGE__*__*` | `SAGE__TIMEOUT__CACHE` | Nested settings |

---

## Related

- `../core_engine/INDEX.md` — Core engine
- `../knowledge_system/INDEX.md` — Knowledge system
- `.context/decisions/ADR_0007_CONFIGURATION.md` — Config ADR

---

*AI Collaboration Knowledge Base*
