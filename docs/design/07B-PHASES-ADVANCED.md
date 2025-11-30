---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~1400
---

# Roadmap: Advanced Phases (G-J)

> Advanced feature phases: Event system, memory persistence, DI, and services

---

## Document Series

This document is part of the Implementation Roadmap series:

| Document                       | Content                                |
|--------------------------------|----------------------------------------|
| `07-ROADMAP.md`                | Overview, status, KPIs, success criteria |
| `07A-PHASES-FOUNDATION.md`     | Phase 0-F: MVP foundation phases       |
| **07B-PHASES-ADVANCED.MD** (this) | Phase G-J: Advanced feature phases  |

---

## Table of Contents

- [1. Phase G: Event-Driven Plugin Architecture](#1-phase-g-event-driven-plugin-architecture)
- [2. Phase H: Cross-Task Memory Persistence](#2-phase-h-cross-task-memory-persistence)
- [3. Phase I: DI Container](#3-phase-i-di-container)
- [4. Phase J: Configuration & Services](#4-phase-j-configuration--services)

---

## 1. Phase G: Event-Driven Plugin Architecture

**Duration**: Day 9-12 | **Status**: ✅ COMPLETE | **Score**: 99.5/100 🏆

**Goal**: Implement Protocol + EventBus async decoupling for plugin system

| Task | Priority | Status | Deliverable |
|------|----------|--------|-------------|
| Create core/events/ module structure | P0 | ✅ | events/__init__.py, bus.py, events.py, protocols.py |
| Implement Event base class and types | P0 | ✅ | Event, LoadEvent, TimeoutEvent, SearchEvent |
| Implement EventType enum | P0 | ✅ | Standard event types with namespacing |
| Implement Protocol interfaces | P0 | ✅ | LoaderHandler, TimeoutHandler, SearchHandler |
| Implement EventBus with async support | P0 | ✅ | subscribe, publish, wildcard matching |
| Add priority-based subscription ordering | P0 | ✅ | Lower priority = earlier execution |
| Add per-handler timeout protection | P0 | ✅ | Error isolation between handlers |
| Implement PluginAdapter for migration | P1 | ✅ | Backward compatibility with old plugins |
| Add unit tests for EventBus | P0 | ✅ | 39 tests, 89% coverage |

**Directory Structure**:

```
src/sage/core/events/
├── __init__.py          # Exports: EventBus, Event, get_event_bus
├── bus.py               # EventBus implementation
├── events.py            # Event class definitions
├── protocols.py         # Protocol interfaces
└── adapter.py           # PluginAdapter for migration
```

**Acceptance Criteria**:
- [x] `from sage.core.events import EventBus, Event, get_event_bus` works
- [x] Subscribe/publish pattern with wildcard matching
- [x] Priority-based handler ordering (lower = earlier)
- [x] Per-handler timeout protection with error isolation
- [x] PluginAdapter for legacy plugin compatibility
- [x] 39 event system tests passing

---

## 2. Phase H: Cross-Task Memory Persistence

**Duration**: Day 13-16 | **Status**: ✅ COMPLETE | **Score**: 100/100 🏆

**Goal**: Implement memory persistence, token management, and session continuity

| Task | Priority | Status | Deliverable |
|------|----------|--------|-------------|
| Create core/memory/ module structure | P0 | ✅ | memory/__init__.py, store.py, token_budget.py, session.py |
| Implement MemoryType and MemoryPriority enums | P0 | ✅ | 6 memory types, 6 priority levels |
| Implement MemoryEntry dataclass | P0 | ✅ | Complete entry structure with serialization |
| Implement MemoryStore with file backend | P0 | ✅ | CRUD, query, checkpoint support (78% coverage) |
| Implement TokenWarningLevel enum | P0 | ✅ | 5 warning levels (70%, 80%, 90%, 95%) |
| Implement TokenBudget controller | P0 | ✅ | Real-time tracking, auto-actions (89% coverage) |
| Implement SessionState dataclass | P0 | ✅ | Full session state tracking |
| Implement HandoffPackage with to_prompt() | P0 | ✅ | Cross-task continuation |
| Implement SessionContinuity service | P0 | ✅ | Start, update, checkpoint, handoff (92% coverage) |
| Add unit tests for memory system | P0 | ✅ | 102 tests, 86% average coverage |

**Directory Structure**:

```
src/sage/core/memory/
├── __init__.py          # Exports: MemoryStore, TokenBudget, SessionContinuity
├── store.py             # MemoryStore, MemoryEntry, MemoryType, MemoryPriority
├── token_budget.py      # TokenBudget, TokenWarningLevel, TokenBudgetConfig
└── session.py           # SessionContinuity, SessionState, HandoffPackage
```

**Storage Location** (platformdirs):

| Platform | Path |
|----------|------|
| Linux | `~/.local/share/sage/memory/` |
| macOS | `~/Library/Application Support/sage/memory/` |
| Windows | `C:\Users\<user>\AppData\Local\sage\memory\` |

**Acceptance Criteria**:
- [x] MemoryStore with file-based persistence
- [x] 6-level memory priority (EPHEMERAL → PERMANENT)
- [x] 5-level token warnings (NORMAL, CAUTION, WARNING, CRITICAL, OVERFLOW)
- [x] Auto-pruning at OVERFLOW level
- [x] Session checkpoint/restore capability
- [x] HandoffPackage with to_prompt() for cross-task continuation
- [x] 102 unit tests with 86% average coverage

---

## 3. Phase I: DI Container

**Duration**: Day 17 | **Status**: ✅ COMPLETE | **Score**: 100/100 🏆

**Goal**: Implement dependency injection container with lifetime management

| Task | Priority | Status | Deliverable |
|------|----------|--------|-------------|
| Create core/di/ module structure | P0 | ✅ | di/__init__.py, container.py |
| Implement lifetime management | P0 | ✅ | Singleton, Transient, Scoped |
| Implement auto-wiring | P0 | ✅ | Type-based dependency resolution |
| Add config/core/di.yaml service registration | P0 | ✅ | Declarative service configuration |
| Add unit tests | P0 | ✅ | 94% test coverage |

**Milestone**: DI container operational with auto-wiring

---

## 4. Phase J: Configuration & Services

**Duration**: Day 18-24 | **Status**: 🔄 IN PROGRESS

**Goal**: Complete configuration system alignment with design document

### Part 1: Configuration Completeness ✅ COMPLETE

| Task | Priority | Status | Deliverable |
|------|----------|--------|-------------|
| Add missing triggers to triggers.yaml | P1 | ✅ | documentation, python triggers |
| Add missing keywords to existing triggers | P1 | ✅ | bug, function, class, method, etc. |
| Add optimization features to features.yaml | P1 | ✅ | client_cache, lazy_expansion, etc. |
| Create src/sage/data/fallback_core.yaml | P1 | ✅ | Fallback content for degradation |
| Create config/services/api.yaml | P1 | ✅ | HTTP API service configuration |
| Create docs/design/09-CONFIGURATION.md | P1 | ✅ | Configuration design documentation |

### Part 2: DI Services Implementation 📋 PLANNED

| Task | Priority | Status | Deliverable |
|------|----------|--------|-------------|
| Implement KnowledgeProtocol/Service | P2 | 📋 | Knowledge search and retrieval |
| Implement OutputProtocol/MultiChannel | P2 | 📋 | Multi-channel output formatting |
| Implement RefineProtocol/Metrics | P2 | 📋 | Metrics collection and refinement |
| Add unit tests for new services | P2 | 📋 | 90%+ coverage target |

### Part 3: API Service Implementation 📋 PLANNED

| Task | Priority | Status | Deliverable |
|------|----------|--------|-------------|
| Implement FastAPI service | P2 | 📋 | HTTP REST API endpoints |
| Implement CORS and rate limiting | P2 | 📋 | Security middleware |
| Implement health check endpoint | P2 | 📋 | /health with details |
| Add API integration tests | P2 | 📋 | End-to-end API testing |

### Part 4: Optimization Features 📋 PLANNED

| Task | Priority | Status | Deliverable |
|------|----------|--------|-------------|
| Implement differential_loading | P3 | 📋 | Load only changed content |
| Implement compressed_loading | P3 | 📋 | ~50% smaller content loading |
| Implement context_pruning | P3 | 📋 | Auto-remove irrelevant sections |
| Add optimization benchmarks | P3 | 📋 | Performance regression tests |

**Acceptance Criteria**:
- [x] 9 triggers with complete bilingual keywords
- [x] 12 config files in sage.yaml includes
- [x] Fallback content for graceful degradation
- [x] Configuration design document created
- [ ] DI services implemented
- [ ] API service operational
- [ ] Optimization features implemented

---

## Related

- `docs/design/07-ROADMAP.md` — Roadmap overview and KPIs
- `docs/design/07A-PHASES-FOUNDATION.md` — Foundation phases (0-F)
- `docs/design/05-PLUGIN-MEMORY.md` — Plugin and memory design

---

*Part of SAGE Knowledge Base*
