---
title: SAGE Knowledge Base - Architecture Design
version: "0.1.0"
last_updated: "2025-11-30"
status: production-ready
tokens: ~1500
---

# Architecture Design

> **Core-Services-Capabilities Modular Architecture with Dev Tools Isolation**

---

## Table of Contents

- [1. Document Series](#1-document-series)
- [2. Implementation Status](#2-implementation-status)
- [3. Architecture Overview](#3-architecture-overview)
- [4. Dependency Rules](#4-dependency-rules)
- [5. Directory Structure](#5-directory-structure)

---

## 1. Document Series

This document is part of the Architecture Design series:

| Document                   | Content                                            |
|----------------------------|----------------------------------------------------|
| **01-ARCHITECTURE.MD** (this) | Core architecture, layers, directory structure  |
| `01A-INFRASTRUCTURE.md`    | Logging, toolchain, packaging, platform support    |
| `01B-CONFIGURATION.md`     | Configuration hierarchy, timeout, YAML DSL         |
| `01C-USAGE.md`             | Bootstrap, quick start, exceptions, AI scenarios   |

---

## 2. Implementation Status

> ⚠️ **Document Type: Design Specification (Target Architecture)**

| Aspect              | Design Target               | Current State                    | Status      |
|---------------------|-----------------------------|----------------------------------|-------------|
| Package name        | `sage-kb`                   | `sage-kb` in pyproject.toml      | ✅ Complete |
| Source location     | `src/sage/`                 | `src/sage/`                      | ✅ Complete |
| Config file         | `sage.yaml`                 | Created at project root          | ✅ Complete |
| Directory structure | Core/Services/Capabilities  | core/, services/, capabilities/  | ✅ Complete |
| Capabilities layer  | analyzers, checkers, monitors | Implemented                    | ✅ Complete |
| Core infrastructure | DI, EventBus, Protocols     | core/di/, core/events/           | ✅ Complete |
| Structured logging  | structlog integration       | core/logging/                    | ✅ Complete |
| Memory persistence  | MemoryStore, TokenBudget    | core/memory/                     | ✅ Complete |
| SAGE Protocol       | models, protocols, exceptions | core/models.py, core/protocols.py | ✅ Complete |

**Status**: M3 complete. 841+ tests passing, 89% coverage. See `07-ROADMAP.md` for details.

---

## 3. Architecture Overview

```
                              [Config File sage.yaml]
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           Core Engine Layer                             │
│                        (<500 lines minimal core)                        │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ SAGE Protocol Interface (Source-Analyze-Generate-Evolve)          │  │
│  │ +-- SourceProtocol    (S) - Knowledge sourcing                    │  │
│  │ +-- AnalyzeProtocol   (A) - Processing & analysis                 │  │
│  │ +-- GenerateProtocol  (G) - Multi-channel output                  │  │
│  │ +-- EvolveProtocol    (E) - Metrics & optimization                │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ TimeoutManager | EventBus | DI Container                          │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                        │
           ┌────────────────────────────┼────────────────────────────┐
           ▼                            ▼                            ▼
┌─────────────────────┐      ┌─────────────────────┐      ┌─────────────────────┐
│    CLI Service      │      │    MCP Service      │      │    API Service      │
│      (Typer)        │      │     (FastMCP)       │      │     (FastAPI)       │
├─────────────────────┤      ├─────────────────────┤      ├─────────────────────┤
│ • get, search       │      │ • get_knowledge     │      │ GET /knowledge      │
│ • info, serve       │      │ • search_knowledge  │      │ GET /search         │
│ • analyze, check    │      │ • kb_info           │      │ GET /health         │
└─────────────────────┘      └─────────────────────┘      └─────────────────────┘
           │                            │                            │
           └────────────────────────────┼────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        Capabilities Layer                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐         │
│  │    Analyzers    │  │    Checkers     │  │    Monitors     │         │
│  │ quality,content │  │  links,struct   │  │ health,timeout  │         │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘         │
└─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  tools/ (Dev-Only, Isolated)                                            │
│  NOT imported at runtime - monitors, dev utilities                      │
└─────────────────────────────────────────────────────────────────────────┘
```

**Key Distinctions**:
- TimeoutManager (Core): Infrastructure for timeout execution
- HealthMonitor (Capabilities): Runtime health checks exposed via MCP
- tools/ (Isolated): Dev-only tools, NOT imported at runtime

---

## 4. Dependency Rules

| Rule                      | Description                                 | Example                                       |
|---------------------------|---------------------------------------------|-----------------------------------------------|
| ✅ Services → Core         | Services can import from Core               | `from sage.core.loader import TimeoutLoader`  |
| ✅ Services → Capabilities | Services can import from Capabilities       | `from sage.capabilities.analyzers import ...` |
| ✅ Capabilities → Core     | Capabilities can import from Core           | `from sage.core.config import SageSettings`   |
| ❌ Core → Services         | Core cannot import from Services            | Forbidden: circular dependency                |
| ❌ Core → Capabilities     | Core cannot import from Capabilities        | Forbidden: core should be independent         |
| ❌ Services ↔ Services     | Services cannot import each other           | Use EventBus for communication                |
| ⚠️ tools/ (isolated)      | tools/ is dev-only, not imported at runtime | Monitors, dev utilities                       |

### Key Design Principles

1. **Zero Cross-Import**: Layers communicate via EventBus, no direct dependencies
2. **Capabilities Layer**: Runtime abilities (analyzers, checkers) exposed via Services
3. **Pluggable**: Every module is an independent plugin, can be enabled/disabled
4. **On-Demand Loading**: Minimal core engine, features loaded as needed
5. **Unidirectional Dependency**: Lower layers don't depend on upper layers
6. **Interface-First**: All interactions through explicit Protocol interfaces
7. **Dev Tools Isolation**: tools/ directory is for development only

---

## 5. Directory Structure

> **Key Features**: MECE 8-directory organization, modular architecture

### 5.1 Root Structure

```
sage/                           # Project root
├── README.md, LICENSE          # Documentation
├── pyproject.toml              # Python project config
├── sage.yaml                   # Smart loading configuration
├── INDEX.md                    # Navigation entry
│
├── .context/                   # Project-specific knowledge
├── .history/                   # AI session history
├── .archive/                   # Historical archives
├── .knowledge/                 # Knowledge content
├── docs/                       # Project documentation
│
├── src/sage/                   # Source code
│   ├── core/                   # Core layer (<500 lines)
│   ├── services/               # Services layer (CLI, MCP, API)
│   ├── capabilities/           # Runtime capabilities
│   ├── domain/                 # Domain models
│   └── plugins/                # Plugin infrastructure
│
├── tools/                      # Dev-only tools (isolated)
├── tests/                      # Test suite
└── examples/                   # Usage examples
```

### 5.2 Directory Statistics

| Directory              | Files | Purpose                                |
|------------------------|-------|----------------------------------------|
| `.knowledge/core/`     | 3     | Core principles (~500 tokens)          |
| `.knowledge/guidelines/`| 11   | Engineering guidelines (~1,200 tokens) |
| `.knowledge/frameworks/`| 5    | Deep frameworks (~2,000 tokens)        |
| `src/sage/core/`       | 9     | Core layer (<500 lines)                |
| `src/sage/services/`   | 4     | Services layer                         |
| `src/sage/capabilities/`| 7    | Runtime capabilities                   |
| `tools/`               | 5     | Dev-only tools (isolated)              |
| **Total**              | ~105  | Production-ready structure             |

### 5.3 Generated Directories (Git Ignored)

| Directory         | Purpose                | Generated By     |
|-------------------|------------------------|------------------|
| `allure-results/` | Test results (JSON)    | pytest           |
| `htmlcov/`        | Coverage HTML reports  | pytest-cov       |
| `.mypy_cache/`    | Type check cache       | mypy             |
| `.ruff_cache/`    | Linter cache           | ruff             |
| `build/`, `dist/` | Build artifacts        | hatchling        |

---

## Related

- `docs/design/01A-INFRASTRUCTURE.md` — Logging, toolchain, packaging, platform support
- `docs/design/01B-CONFIGURATION.md` — Configuration hierarchy, timeout, YAML DSL
- `docs/design/01C-USAGE.md` — Bootstrap, quick start, exceptions, AI scenarios
- `docs/design/02-SAGE-PROTOCOL.md` — SAGE protocol design
- `docs/design/03-SERVICES.md` — Services layer design

---

*Part of SAGE Knowledge Base*
