---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~500
---
# SAGE Project Overview

> Quick introduction to SAGE Knowledge Base for new contributors and AI assistants

---

## Table of Contents

- [1. What is SAGE?](#1-what-is-sage)
- [2. Architecture](#2-architecture)
- [3. Key Concepts](#3-key-concepts)
- [4. Getting Started](#4-getting-started)
- [5. Related](#5-related)

---

## 1. What is SAGE?

**SAGE** (Source, Analyze, Generate, Evolve) is a production-grade knowledge management system designed for AI-human
collaboration.

### Design Philosophy — 信达雅 (Xin-Da-Ya)

| Principle        | Chinese | Description                     |
|:-----------------|:--------|:--------------------------------|
| **Faithfulness** | 信 (Xin) | Accurate, reliable, testable    |
| **Clarity**      | 达 (Da)  | Clear, maintainable, structured |
| **Elegance**     | 雅 (Ya)  | Refined, balanced, sustainable  |

### Project Status

| Attribute    | Value         |
|:-------------|:--------------|
| **Version**  | 0.1.0 (Alpha) |
| **Language** | Python 3.12+  |
| **License**  | MIT           |

---

## 2. Architecture

SAGE uses a **Core-Services-Capabilities** three-layer architecture:

```
┌─────────────────────────────────────────────────────────┐
│                    Core Engine Layer                    │
│  • SAGE Protocol  • TimeoutManager  • EventBus  • DI    │
└─────────────────────────────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   CLI Service   │ │   MCP Service   │ │   API Service   │
└─────────────────┘ └─────────────────┘ └─────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  Capabilities Layer                     │
│           (Analyzers, Checkers, Monitors)               │
└─────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

| Layer            | Purpose                               | Dependencies |
|:-----------------|:--------------------------------------|:-------------|
| **Core**         | Infrastructure, protocols, DI, events | None         |
| **Services**     | User interfaces (CLI, MCP, API)       | Core         |
| **Capabilities** | Runtime features                      | Core         |

---

## 3. Key Concepts

### SAGE Protocol

The four-phase processing model:

| Phase        | Purpose     | Description                   |
|:-------------|:------------|:------------------------------|
| **S**ource   | Acquisition | Load and search knowledge     |
| **A**nalyze  | Processing  | Enrich and validate content   |
| **G**enerate | Output      | Format for different channels |
| **E**volve   | Improvement | Track metrics and optimize    |

### Timeout Hierarchy (T1-T5)

| Level | Duration | Use Case         |
|:------|:---------|:-----------------|
| T1    | 100ms    | Cache lookup     |
| T2    | 500ms    | Single file      |
| T3    | 2s       | Layer loading    |
| T4    | 5s       | Full system      |
| T5    | 10s      | Complex analysis |

### Autonomy Levels (L1-L6)

| Level | Autonomy | AI Behavior             |
|:------|:---------|:------------------------|
| L1-L2 | 0-40%    | Ask before changes      |
| L3-L4 | 40-80%   | Proceed, report after ⭐ |
| L5-L6 | 80-100%  | High autonomy           |

---

## 4. Getting Started

### For New Contributors

1. Read `conventions/NAMING.md` and `conventions/FILE_STRUCTURE.md`
2. Review ADR-0001 (architecture) and ADR-0002 (SAGE protocol)
3. Check `intelligence/calibration/PATTERNS.md` for collaboration patterns

### For AI Assistants

1. Check `intelligence/calibration/CALIBRATION.md` for autonomy levels
2. Follow patterns in `intelligence/calibration/PATTERNS.md`
3. Use optimizations from `intelligence/optimization/`
4. Reference conventions when generating code

### Key Directories

| Directory     | Purpose                        |
|:--------------|:-------------------------------|
| `src/sage/`   | Source code                    |
| `tests/`      | Test suite                     |
| `config/`     | Configuration files            |
| `.context/`   | Project-specific knowledge     |
| `.knowledge/` | Generic reusable knowledge     |
| `.junie/`     | AI collaboration configuration |

---

## 5. Related

- `../INDEX.md` — Full project context navigation
- `../decisions/ADR-0001-ARCHITECTURE.md` — Architecture decision
- `../decisions/ADR-0002-SAGE-PROTOCOL.md` — SAGE protocol design
- `../intelligence/calibration/CALIBRATION.md` — AI autonomy calibration
- `.junie/GUIDELINES.md` — AI collaboration guidelines

---

*Part of SAGE Knowledge Base - Project Context*
