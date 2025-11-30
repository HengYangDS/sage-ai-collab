---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~1000
---

# Content Structure & Organization

> Directory structure, content organization, and knowledge layers

---

## Document Series

This document is part of the Content Structure series:

| Document                   | Content                                    |
|----------------------------|--------------------------------------------|
| **06-CONTENT-STRUCTURE.MD** (this) | Directory structure, content organization |
| `06A-KNOWLEDGE-TAXONOMY.md` | Knowledge taxonomy, navigation, lifecycle |

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Directory Structure](#2-directory-structure)
- [3. Content Directory Detail](#3-content-directory-detail)
- [4. Directory Statistics](#4-directory-statistics)
- [5. Chapter Consolidation](#5-chapter-consolidation)

---

## 1. Overview

This document covers:

1. **Directory Structure** - Production-ready project layout
2. **Content Organization** - Knowledge content hierarchy
3. **Chapter Consolidation** - Guidelines restructuring (16 → 10)

For AI collaboration directories, knowledge taxonomy, and lifecycle management, see `06A-KNOWLEDGE-TAXONOMY.md`.

---

## 2. Directory Structure

> **Status**: Production-Ready Design

```
sage/                              # Project root directory
│
├── README.md                      # Project documentation
├── LICENSE                        # Open source license
├── CHANGELOG.md                   # Change log
├── pyproject.toml                 # Python project configuration
├── Makefile                       # Make development commands
├── sage.yaml                      # Smart loading configuration
├── INDEX.md                       # Navigation entry (~100 tokens)
│
├── docs/                          # Project documentation
│   ├── design/                    # Design documents (00-09)
│   ├── api/                       # API documentation
│   └── guides/                    # Development guides
│
├── .knowledge/                    # Knowledge content directory
│   ├── core/                      # Core principles (~500 tokens)
│   ├── guidelines/                # Engineering guidelines (~1,200 tokens)
│   ├── frameworks/                # Deep frameworks (~2,000 tokens)
│   ├── practices/                 # Best practices (~1,500 tokens)
│   ├── scenarios/                 # Scenario presets (~500 tokens)
│   └── templates/                 # Reusable templates (~300 tokens)
│
├── src/sage/                      # Source code (modular architecture)
│   ├── __init__.py                # Package entry, version info
│   ├── __main__.py                # Unified entry point
│   ├── interfaces/                # Protocol definitions
│   ├── domain/                    # Business domain models
│   ├── core/                      # Core layer (<500 lines)
│   │   └── logging/               # Unified logging subpackage
│   ├── services/                  # Services layer (CLI, MCP, API)
│   ├── capabilities/              # Runtime capabilities (MCP)
│   │   ├── analyzers/             # Quality, Content analyzers
│   │   ├── checkers/              # Link checker
│   │   └── monitors/              # Health monitor
│   └── plugins/                   # Plugin infrastructure
│
├── tools/                         # Dev-Only (NOT imported at runtime)
│   ├── monitors/                  # TimeoutMonitor (dev performance)
│   └── dev_scripts/               # Development setup scripts
│
├── tests/                         # Test directory (mirrors src/)
│   ├── conftest.py                # Global pytest fixtures
│   ├── fixtures/                  # Test data
│   ├── unit/                      # Unit tests
│   ├── integration/               # Integration tests
│   └── performance/               # Performance tests
│
└── examples/                      # Usage examples
```

---

## 3. Content Directory Detail

### 3.1 .knowledge/core/ (~500 tokens, Always Load)

| File                 | Purpose                                  |
|----------------------|------------------------------------------|
| `PRINCIPLES.md`      | Xin-Da-Ya philosophy, core values        |
| `QUICK_REFERENCE.md` | 5 critical questions, autonomy quick ref |
| `DEFAULTS.md`        | Default behaviors, calibration standards |

### 3.2 .knowledge/guidelines/ (~1,200 tokens, On-Demand)

| File                  | Purpose                             |
|-----------------------|-------------------------------------|
| `QUICK_START.md`      | 3-minute quick start                |
| `PLANNING_DESIGN.md`  | Planning and architecture           |
| `CODE_STYLE.md`       | Code style standards                |
| `ENGINEERING.md`      | Config/test/perf/change/maintain    |
| `DOCUMENTATION.md`    | Documentation standards             |
| `PYTHON.md`           | Python best practices               |
| `AI_COLLABORATION.md` | AI collaboration and autonomy       |
| `COGNITIVE.md`        | Cognitive enhancement core          |
| `QUALITY.md`          | Quality framework                   |
| `SUCCESS.md`          | Xin-Da-Ya mapping, success criteria |

### 3.3 .knowledge/frameworks/ (~2,000 tokens, On-Demand)

| Directory        | File                  | Purpose                               |
|------------------|-----------------------|---------------------------------------|
| `autonomy/`      | `LEVELS.md`           | 6-level autonomy spectrum definition  |
| `cognitive/`     | `EXPERT_COMMITTEE.md` | Expert committee, chain-of-thought    |
| `collaboration/` | `PATTERNS.md`         | Collaboration patterns                |
| `decision/`      | `QUALITY_ANGLES.md`   | Quality angles, expert roles          |
| `timeout/`       | `HIERARCHY.md`        | Timeout principles, strategies        |

### 3.4 .knowledge/practices/ (~1,500 tokens, On-Demand)

| Directory           | File                         | Purpose                         |
|---------------------|------------------------------|---------------------------------|
| `ai_collaboration/` | `WORKFLOW.md`                | Workflow, interaction patterns  |
| `documentation/`    | `DOCUMENTATION_STANDARDS.md` | Documentation standards (SSOT)  |
| `engineering/`      | `PATTERNS.md`                | Design patterns, best practices |

### 3.5 .knowledge/scenarios/ & templates/

| Directory   | Purpose                               |
|-------------|---------------------------------------|
| `scenarios/` | Context configuration, specific guides |
| `templates/` | Project initialization templates       |

---

## 4. Directory Statistics

| Directory              | Files | Purpose                              |
|------------------------|-------|--------------------------------------|
| Root                   | 12    | Project entry, config, dev toolchain |
| docs/                  | 25+   | Project documentation                |
| .knowledge/core/       | 3     | Core principles (~500 tokens)        |
| .knowledge/guidelines/ | 11    | Engineering guidelines               |
| .knowledge/frameworks/ | 5     | Deep frameworks (~2,000 tokens)      |
| .knowledge/practices/  | 4     | Best practices                       |
| src/sage/core/         | 9     | Core layer (<500 lines)              |
| src/sage/services/     | 4     | Services layer (CLI, MCP, API)       |
| src/sage/capabilities/ | 7     | Runtime capabilities                 |
| tests/                 | 20+   | Test directory                       |
| **Total**              | ~105  | Production-ready structure           |

---

## 5. Chapter Consolidation

The guidelines were consolidated from 16 chapters to 10 for better organization:

| Original Chapters                     | New Chapter         | Lines | Rationale     |
|---------------------------------------|---------------------|-------|---------------|
| 0. Quick Reference                    | QUICK_START.md      | ~60   | Keep as-is    |
| 1. Planning + 2. Design               | PLANNING_DESIGN.md  | ~80   | Merge short   |
| 3. Code Style                         | CODE_STYLE.md       | ~150  | Keep as-is    |
| 4-8. Config/Test/Perf/Change/Maintain | ENGINEERING.md      | ~120  | Merge 5 mini  |
| 9. Documentation                      | DOCUMENTATION.md    | ~100  | Keep as-is    |
| 10. Python + 11. Decorator            | PYTHON.md           | ~130  | Merge overlap |
| 12. AI Collab + 13. Autonomy          | AI_COLLABORATION.md | ~200  | Unify AI      |
| 14. Cognitive (core)                  | COGNITIVE.md        | ~100  | Extract core  |
| (new) Quality                         | QUALITY.md          | ~80   | From 14       |
| 15. Success                           | SUCCESS.md          | ~80   | Streamline    |

**Result**: 16 → 10 chapters, ~1,100 lines (from ~1,464, -25%)

---

## Related

- `docs/design/06A-KNOWLEDGE-TAXONOMY.md` — Knowledge taxonomy and lifecycle
- `docs/design/01-ARCHITECTURE.md` — Architecture design
- `docs/design/05-PLUGIN-MEMORY.md` — Plugin and memory design
- `.knowledge/practices/documentation/KNOWLEDGE_ORGANIZATION.md` — Organization guide

---

*Part of SAGE Knowledge Base*
