---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~1200
---

# Roadmap: Foundation Phases (0-F)

> MVP implementation phases: Package alignment through enhancement

---

## Document Series

This document is part of the Implementation Roadmap series:

| Document                       | Content                                |
|--------------------------------|----------------------------------------|
| `07-roadmap.md`                | Overview, status, KPIs, success criteria |
| **07a-phases-foundation.md** (this) | Phase 0-F: MVP foundation phases     |
| `07b-phases-advanced.md`       | Phase G-J: Advanced feature phases     |

---

## Table of Contents

- [1. Phase 0: Package Alignment](#1-phase-0-package-alignment)
- [2. Phase A: Base Reorganization](#2-phase-a-base-reorganization)
- [3. Phase B: Core Migration](#3-phase-b-core-migration)
- [4. Phase C: Logging System](#4-phase-c-logging-system)
- [5. Phase D: Tools & Capabilities](#5-phase-d-tools--capabilities)
- [6. Phase E: Tests Reorganization](#6-phase-e-tests-reorganization)
- [7. Phase F: Enhancement & Polish](#7-phase-f-enhancement--polish)

---

## 1. Phase 0: Package Alignment

**Duration**: Day 0.5 | **Status**: ✅ COMPLETE

**Goal**: Fix package configuration so `pip install -e .` works correctly

| Task | Priority | Deliverable |
|------|----------|-------------|
| Update pyproject.toml `name` to "sage-kb" | P0 | Correct package identity |
| Fix entry point: `sage = "sage.cli:main"` | P0 | Working CLI command |
| Update wheel packages: `["src/sage"]` | P0 | Correct build target |
| Add missing dependencies | P1 | Complete dependency list |
| Verify `pip install -e .` succeeds | P0 | Functional dev install |

**Acceptance Criteria**:
- [x] `pip install -e .` completes without errors
- [x] `sage --help` displays help text
- [x] `python -c "import sage"` works
- [x] Package name shows as "sage-kb" in pip list

---

## 2. Phase A: Base Reorganization

**Duration**: Day 1-2 | **Status**: ✅ COMPLETE

**Goal**: Create new directory structure for 3-layer architecture

| Task | Priority | Deliverable |
|------|----------|-------------|
| Create docs/ directory structure | P0 | docs/design/, docs/api/, docs/guides/ |
| Create src/sage/core/ directory | P0 | Layer 1 structure |
| Create src/sage/services/ directory | P0 | Layer 2 structure |
| Move loader.py to core/ | P0 | Core layer migration |
| Move cli.py, mcp_server.py to services/ | P0 | Services layer migration |
| Run tests to verify | P0 | No regressions |

**Milestone**: 3-layer directory structure created

---

## 3. Phase B: Core Migration

**Duration**: Day 2 | **Status**: ✅ COMPLETE

**Goal**: Complete core layer with timeout and unified entry point

| Task | Priority | Deliverable |
|------|----------|-------------|
| Move timeout_manager.py to core/timeout.py | P0 | Core timeout module |
| Create core/config.py with enhanced Config class | P0 | YAML+ENV+defaults support |
| Create core/models.py with data classes | P0 | Document, Layer, SearchResult |
| Create __main__.py unified entry point | P0 | python -m sage |
| Update all import statements | P0 | No import errors |

**Milestone**: Core layer complete, unified entry point working

---

## 4. Phase C: Logging System

**Duration**: Day 3 | **Status**: ✅ COMPLETE

**Goal**: Implement unified structured logging

| Task | Priority | Status | Deliverable |
|------|----------|--------|-------------|
| Create core/logging/ subpackage | P0 | ✅ | Logging directory |
| Implement logging/__init__.py exports | P0 | ✅ | get_logger, bind_context |
| Implement logging/config.py | P0 | ✅ | configure_logging() |
| Implement logging/context.py | P0 | ✅ | Context management |
| Add structlog to pyproject.toml | P0 | ✅ | Dependency added |
| Integrate logging in loader.py | P1 | ✅ | Structured log output |
| Add logging unit tests | P1 | ✅ | 22 tests, 98% coverage |

**Acceptance Criteria**:
- [x] `from sage.core.logging import get_logger, configure_logging` works
- [x] Structured logs with context binding operational
- [x] JSON and console output formats supported
- [x] 22 logging tests passing

---

## 5. Phase D: Tools & Capabilities

**Duration**: Day 4-5 | **Status**: ✅ COMPLETE

**Goal**: Implement Capabilities layer and isolate dev-only tools

### Day 4: Capabilities Layer

| Task | Priority | Deliverable |
|------|----------|-------------|
| Create src/sage/capabilities/ directory | P0 | Capabilities layer structure |
| Create capabilities/analyzers/ | P0 | MCP: analyze_quality, analyze_content |
| Create capabilities/checkers/ | P0 | MCP: check_links |
| Create capabilities/monitors/ | P0 | MCP: check_health |
| Update MCP server to use Capabilities | P0 | Services → Capabilities integration |

### Day 5: Tools Isolation

| Task | Priority | Deliverable |
|------|----------|-------------|
| Restructure tools/ to monitors/ + dev_scripts/ | P0 | Dev-only isolation |
| Move TimeoutMonitor to tools/monitors/ | P0 | Dev performance tool |
| Create tools/dev_scripts/ for setup scripts | P0 | Development utilities |
| Update tools/__init__.py with lazy imports | P1 | Dynamic import only when called |

**Key Distinction**:
- **Capabilities** (src/sage/capabilities/): Runtime abilities exposed via MCP/API
- **Tools** (tools/): Dev-only utilities, never imported at runtime

---

## 6. Phase E: Tests Reorganization

**Duration**: Day 6 | **Status**: ✅ COMPLETE

**Goal**: Mirror source structure in tests

| Task | Priority | Deliverable |
|------|----------|-------------|
| Create tests/fixtures/ directory | P0 | Test data home |
| Add sample_.knowledge/, mock_responses/, configs/ | P0 | Test fixtures |
| Create tests/unit/core/ directory | P0 | Core unit tests |
| Create tests/unit/services/ directory | P0 | Services unit tests |
| Move existing tests to new structure | P0 | Mirrored structure |
| Create tests/integration/ directory | P1 | Integration tests |
| Create conftest.py with global fixtures | P0 | Shared fixtures |

**Milestone**: Test structure mirrors source, all tests pass

---

## 7. Phase F: Enhancement & Polish

**Duration**: Day 7-8 | **Status**: ✅ COMPLETE

**Goal**: Add development toolchain and polish

### Day 7: Development Toolchain

| Task | Priority | Deliverable |
|------|----------|-------------|
| Create Makefile with all commands | P0 | make install/test/lint/serve |
| Create .pre-commit-config.yaml | P0 | ruff, mypy hooks |
| Create .env.example | P1 | Environment template |
| Add py.typed marker | P1 | PEP 561 compliance |
| Create examples/ directory with samples | P1 | Usage examples |

### Day 8: Documentation & Release Prep

| Task | Priority | Deliverable |
|------|----------|-------------|
| Complete README.md user documentation | P0 | Comprehensive docs |
| Add CHANGELOG.md | P1 | Version history |
| Prepare PyPI release | P1 | Package on PyPI |
| Final integration testing | P0 | Release validation |

**Acceptance Criteria**:
- [ ] Average response time < 500ms
- [ ] Timeout rate < 1%
- [ ] Complete documentation
- [ ] Successful PyPI release

---

## Related

- `docs/design/07-roadmap.md` — Roadmap overview and KPIs
- `docs/design/07b-phases-advanced.md` — Advanced phases (G-J)
- `docs/design/01-architecture.md` — Architecture design

---

*Part of SAGE Knowledge Base*
