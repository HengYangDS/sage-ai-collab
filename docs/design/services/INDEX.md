# Services

> Service layer design for SAGE interfaces

---

## 1. Overview

The services layer provides multiple interfaces (CLI, MCP, API) for interacting with SAGE.

---

## 2. Documents

| Document | Description | Status |
|----------|-------------|--------|
| `SERVICE_LAYER.md` | Service layer architecture | Planned |
| `CLI_SERVICE.md` | Command-line interface | Planned |
| `MCP_SERVICE.md` | Model Context Protocol service | Planned |
| `API_SERVICE.md` | REST/HTTP API service | Planned |

---

## 3. Service Architecture

```
                    ┌─────────────────┐
                    │     Users       │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
    ┌─────────┐        ┌─────────┐        ┌─────────┐
    │   CLI   │        │   MCP   │        │   API   │
    └────┬────┘        └────┬────┘        └────┬────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                    ┌────────▼────────┐
                    │  Core Engine    │
                    └─────────────────┘
```

---

## 4. Service Responsibilities

| Service | Channel | Use Case |
|---------|---------|----------|
| **CLI** | Terminal | Developer interaction |
| **MCP** | Protocol | AI assistant integration |
| **API** | HTTP | External integrations |

---

## 5. Common Features

All services share:

- Authentication/Authorization
- Request validation
- Error handling
- Logging and metrics
- Rate limiting

---

## Related

- `../architecture/INDEX.md` — Architecture overview
- `../core_engine/INDEX.md` — Core engine
- `../capabilities/INDEX.md` — Capabilities

---

*Part of SAGE Knowledge Base*
