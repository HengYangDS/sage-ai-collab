# Architecture

> System architecture and structural design for SAGE

---

## 1. Overview

This directory documents the architectural foundations of SAGE, including layer structure, dependencies, and infrastructure.

---

## 2. Documents

| Document | Description | Status |
|----------|-------------|--------|
| `THREE_LAYER.md` | Three-layer architecture (Core, Services, Capabilities) | Planned |
| `DEPENDENCIES.md` | Dependency rules and boundaries | Planned |
| `DIRECTORY_LAYOUT.md` | Project directory structure | Planned |
| `INFRASTRUCTURE.md` | Infrastructure and deployment | Planned |

---

## 3. Architecture Overview

```mermaid
graph TD
    Services["Services Layer<br/>(CLI, MCP, API interfaces)"]
    Capabilities["Capabilities Layer<br/>(analyzers, checkers, monitors,<br/>converters, generators)"]
    Core["Core Layer<br/>(DI, Events, Models, Plugins, Config)"]
    
    Services --> Capabilities --> Core
```

---

## 4. Key Principles

| Principle | Description |
|-----------|-------------|
| **Layered** | Clear separation of concerns |
| **Pluggable** | Extension via plugin system |
| **Configurable** | Flexible configuration |
| **Resilient** | Timeout and fault tolerance |

---

## Related

- `../philosophy/INDEX.md` — Design philosophy
- `../core_engine/INDEX.md` — Core engine details
- `.context/conventions/FOUR_LAYER_MODEL.md` — Four layer model

---

*AI Collaboration Knowledge Base*
