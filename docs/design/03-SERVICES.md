---
title: SAGE Knowledge Base - Services Design
version: "0.1.0"
last_updated: "2025-11-30"
status: production-ready
tokens: ~800
---

# Services Design

> **Multi-channel service layer: CLI, MCP, and HTTP API**

---

## Table of Contents

- [1. Document Series](#1-document-series)
- [2. Service Overview](#2-service-overview)
- [3. Service Comparison](#3-service-comparison)
- [4. Shared Components](#4-shared-components)
- [5. Error Handling Summary](#5-error-handling-summary)
- [6. Testing Summary](#6-testing-summary)

---

## 1. Document Series

This document is part of the Services Design series:

| Document                    | Content                                |
|-----------------------------|----------------------------------------|
| **03-SERVICES.MD** (this)   | Overview, comparison, shared components|
| `03A-CLI-SERVICE.md`        | CLI service with Typer + Rich          |
| `03B-MCP-SERVICE.md`        | MCP service with FastMCP               |
| `03C-API-SERVICE.md`        | HTTP API with FastAPI                  |

---

## 2. Service Overview

SAGE provides three service channels for knowledge access:

| Service | Protocol  | Use Case                   | Client               |
|---------|-----------|----------------------------|----------------------|
| **CLI** | Terminal  | Developer local use        | Terminal             |
| **MCP** | JSON-RPC  | AI assistant integration   | Claude, Cursor, etc. |
| **API** | HTTP REST | Web apps, external systems | Any HTTP client      |

```
┌─────────────────────────────────────────────────────────────┐
│                     Services Layer                          │
├───────────────┬───────────────┬───────────────┬─────────────┤
│  CLI Service  │  MCP Service  │  API Service  │   Shared    │
│   (Typer)     │  (FastMCP)    │  (FastAPI)    │  Components │
├───────────────┼───────────────┼───────────────┼─────────────┤
│ • sage get    │ • get_knowledge│ GET /knowledge│ • Loader   │
│ • sage search │ • search_knowledge│ GET /search│ • Search    │
│ • sage info   │ • get_framework│ GET /layers   │ • Timeout   │
│ • sage serve  │ • kb_info     │ GET /health   │ • Config    │
└───────────────┴───────────────┴───────────────┴─────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   Core Layer    │
                    │ (Protocols, DI) │
                    └─────────────────┘
```

---

## 3. Service Comparison

| Feature           | CLI              | MCP                | HTTP API         |
|-------------------|------------------|--------------------| -----------------|
| **Framework**     | Typer + Rich     | FastMCP            | FastAPI          |
| **Transport**     | Terminal I/O     | stdio/SSE          | HTTP REST        |
| **Output**        | Rich formatting  | JSON               | JSON             |
| **Auth**          | N/A              | Client-managed     | Bearer token     |
| **Use Case**      | Interactive      | AI integration     | System integration|
| **Timeout**       | Per-command      | Per-tool           | Per-request      |

### Command/Tool Mapping

| Operation        | CLI Command      | MCP Tool           | API Endpoint         |
|------------------|------------------|--------------------| ---------------------|
| Get knowledge    | `sage get`       | `get_knowledge`    | `GET /v1/knowledge`  |
| Search           | `sage search`    | `search_knowledge` | `GET /v1/search`     |
| Get framework    | `sage get -l 2`  | `get_framework`    | `GET /v1/frameworks` |
| System info      | `sage info`      | `kb_info`          | `GET /health`        |
| Start server     | `sage serve`     | N/A                | N/A                  |

---

## 4. Shared Components

All services share these core components via dependency injection:

| Component       | Purpose                    | Interface          |
|-----------------|----------------------------|--------------------|
| **Loader**      | Knowledge loading          | `SourceProtocol`   |
| **Search**      | Content search             | `AnalyzeProtocol`  |
| **Timeout**     | Timeout management         | `TimeoutManager`   |
| **Config**      | Configuration access       | `SAGEConfig`       |
| **EventBus**    | Inter-service communication| `EventBus`         |

### Dependency Injection Pattern

```python
from sage.core.di import get_container
from sage.core.protocols import SourceProtocol

# All services use the same pattern
container = get_container()
loader = container.resolve(SourceProtocol)
result = await loader.source(request)
```

---

## 5. Error Handling Summary

All services use a unified error handling approach:

### Error Code Ranges

| Range     | Category      | Example                    |
|-----------|---------------|----------------------------|
| 1xxx      | Loading       | `SAGE-1001` TimeoutError   |
| 2xxx      | Configuration | `SAGE-2002` ValidationError|
| 3xxx      | Service       | `SAGE-3001` MCPError       |
| 4xxx      | Plugin        | `SAGE-4001` PluginLoadError|

### Error Response Format

```json
{
  "error": {
    "code": "SAGE-1001",
    "message": "Operation timed out",
    "details": {"timeout_ms": 5000},
    "recoverable": true
  }
}
```

### Graceful Degradation

| Timeout Level | Action                              |
|---------------|-------------------------------------|
| T1-T2         | Return cached content               |
| T3            | Return partial + warning            |
| T4-T5         | Return core only + error indication |

---

## 6. Testing Summary

### Test Pyramid

```
                ╱╲
               ╱E2E╲           5% - End-to-end
              ╱──────╲
             ╱Integration╲     15% - Integration
            ╱────────────╲
           ╱  Unit Tests  ╲    80% - Unit tests
          ╱────────────────╲
```

### Coverage Targets

| Component    | Target  | Focus                        |
|--------------|---------|------------------------------|
| `core/`      | 90%+    | Protocols, timeout, DI       |
| `services/`  | 80%+    | CLI, MCP, API endpoints      |
| `capabilities/`| 85%+  | Analyzers, checkers, monitors|

### Test Categories

| Category        | Location             | Speed    |
|-----------------|----------------------|----------|
| Unit            | `tests/unit/`        | <100ms   |
| Integration     | `tests/integration/` | <5s      |
| E2E             | `tests/e2e/`         | <30s     |
| Performance     | `tests/performance/` | Variable |

---

## Related

- `docs/design/03A-CLI-SERVICE.md` — CLI service implementation
- `docs/design/03B-MCP-SERVICE.md` — MCP service implementation
- `docs/design/03C-API-SERVICE.md` — HTTP API implementation
- `docs/design/01-ARCHITECTURE.md` — Architecture overview
- `docs/design/04-TIMEOUT-LOADING.md` — Timeout patterns

---

*Part of SAGE Knowledge Base*
