# Design Documents Index

> Navigation hub for SAGE Knowledge Base design documentation

---

## 1. Overview

| Document | Description |
|----------|-------------|
| `OVERVIEW.md` | Design overview and reading guide |

---

## 2. Foundation (★★★★★)

| Directory | Purpose | Key Documents |
|-----------|---------|---------------|
| `philosophy/` | Design philosophy | XIN_DA_YA, DESIGN_AXIOMS |
| `protocols/` | SAGE protocol specs | SAGE_PROTOCOL, SOURCE/ANALYZE/GENERATE/EVOLVE |
| `architecture/` | System architecture | THREE_LAYER, DEPENDENCIES, DIRECTORY_LAYOUT |

---

## 3. Core Systems (★★★★☆)

| Directory | Purpose | Key Documents |
|-----------|---------|---------------|
| `core_engine/` | Core components | DI_CONTAINER, EVENT_BUS, DATA_MODELS |
| `timeout_resilience/` | Resilience patterns | TIMEOUT_HIERARCHY, CIRCUIT_BREAKER |

---

## 4. Implementation (★★★☆☆)

| Directory | Purpose | Key Documents |
|-----------|---------|---------------|
| `services/` | Service layer | CLI_SERVICE, MCP_SERVICE, API_SERVICE |
| `capabilities/` | Capability families | ANALYZERS, CHECKERS, MONITORS, CONVERTERS, GENERATORS |
| `plugins/` | Plugin system | PLUGIN_ARCHITECTURE, EXTENSION_POINTS |

---

## 5. Knowledge & State (★★★☆☆)

| Directory | Purpose | Key Documents |
|-----------|---------|---------------|
| `knowledge_system/` | Knowledge management | LAYER_HIERARCHY, LOADING_STRATEGY |
| `memory_state/` | State persistence | SESSION_MANAGEMENT, CROSS_TASK_MEMORY |
| `configuration/` | Config system | CONFIG_HIERARCHY, YAML_DSL |

---

## 6. Evolution (★★☆☆☆)

| Directory | Purpose | Key Documents |
|-----------|---------|---------------|
| `evolution/` | Roadmap & planning | ROADMAP, MILESTONES, EVALUATION_CRITERIA |

---

## 7. Directory Structure

```
docs/design/
├── INDEX.md              ← You are here
├── OVERVIEW.md
├── philosophy/
├── protocols/
├── architecture/
├── core_engine/
├── timeout_resilience/
├── services/
├── capabilities/
├── plugins/
├── knowledge_system/
├── memory_state/
├── configuration/
└── evolution/
```

---

## Related

- `OVERVIEW.md` — Design overview and reading guide
- `.context/conventions/DIRECTORY_STRUCTURE.md` — Directory conventions
- `.context/decisions/` — Architecture Decision Records

---

*Part of SAGE Knowledge Base*
