---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~800
---

# Knowledge Base Navigation

> Entry point for SAGE knowledge content

---

## Table of Contents

- [1. Directory Structure](#1-directory-structure)
- [2. Layer Overview](#2-layer-overview)
- [3. Complete File List](#3-complete-file-list)
- [4. Navigation Pattern](#4-navigation-pattern)

---

## 1. Directory Structure

| Layer          | Path          | Purpose                                   | Files |
|----------------|---------------|-------------------------------------------|-------|
| **Core**       | `core/`       | Principles, defaults, quick reference     | 4     |
| **Guidelines** | `guidelines/` | Code style, engineering, AI collaboration | 15    |
| **Frameworks** | `frameworks/` | Autonomy, timeout, cognitive patterns     | 24    |
| **Practices**  | `practices/`  | Documentation, engineering, decisions     | 43    |
| **References** | `references/` | Quick reference guides and checklists     | 4     |
| **Scenarios**  | `scenarios/`  | Context-specific guides                   | 23    |
| **Templates**  | `templates/`  | Reusable document templates               | 17    |

**Total**: ~132 knowledge files

---

## 2. Layer Overview

### 2.1 Core (4 files)

Foundation knowledge loaded on every session:

| File                 | Purpose                         |
|----------------------|---------------------------------|
| `principles.md`      | 信达雅 + 术法道 philosophy            |
| `quick_reference.md` | 5 questions + autonomy levels   |
| `defaults.md`        | Default behaviors + calibration |

### 2.2 Guidelines (15 files)

Code style and collaboration standards:

| File                  | Purpose                       |
|-----------------------|-------------------------------|
| `quick_start.md`      | 3-minute productivity guide   |
| `code_style.md`       | Code style standards          |
| `ai_collaboration.md` | Human-AI interaction patterns |
| `python.md`           | Python-specific guidelines    |
| `typescript.md`       | TypeScript guidelines         |
| `sql.md`              | SQL conventions               |
| `shell.md`            | Shell scripting standards     |
| `documentation.md`    | Documentation standards       |
| `engineering.md`      | Engineering practices         |
| `security.md`         | Security guidelines           |
| `quality.md`          | Quality assurance             |
| `cognitive.md`        | Cognitive patterns            |
| `planning.md`         | Planning guidelines           |
| `success.md`          | Success metrics               |

### 2.3 Frameworks (24 files)

Reusable patterns and strategies across 7 categories:

| Subdirectory   | Files | Purpose                          |
|----------------|-------|----------------------------------|
| `autonomy/`    | 2     | AI autonomy levels (L1-L6)       |
| `cognitive/`   | 3     | Expert committee, info density   |
| `design/`      | 2     | Design axioms and principles     |
| `patterns/`    | 5     | Collaboration, decision patterns |
| `performance/` | 4     | Caching, optimization, profiling |
| `resilience/`  | 2     | Timeout patterns, fallbacks      |
| `security/`    | 5     | Auth, secrets, security checks   |

### 2.4 Practices (43 files)

Real-world implementation guidance:

| Subdirectory        | Files | Purpose                      |
|---------------------|-------|------------------------------|
| `ai_collaboration/` | 11    | Context, session, token mgmt |
| `decisions/`        | 1     | Autonomy case studies        |
| `documentation/`    | 7     | Knowledge org, standards     |
| `engineering/`      | 23    | API, testing, CI/CD, logging |

### 2.5 Scenarios (23 files)

Context-specific project guides:

| Subdirectory            | Files | Purpose                    |
|-------------------------|-------|----------------------------|
| `data_pipeline/`        | 2     | Data pipeline projects     |
| `devops/`               | 2     | DevOps workflows           |
| `documentation/`        | 2     | Documentation projects     |
| `knowledge_management/` | 1     | Knowledge management       |
| `legacy_modernization/` | 1     | Legacy system updates      |
| `mcp_integration/`      | 1     | MCP integration            |
| `microservices/`        | 1     | Microservices architecture |
| `monorepo/`             | 1     | Monorepo management        |
| `plugin_development/`   | 1     | Plugin development         |
| `python_backend/`       | 2     | Python backend projects    |
| `typescript_frontend/`  | 2     | TypeScript frontend        |

### 2.6 References (2 files)

Quick reference guides and checklists:

| File                       | Purpose                         |
|----------------------------|---------------------------------|
| `knowledge_quick_ref.md`   | Knowledge organization patterns |
| `performance_checklist.md` | Performance optimization checks |

### 2.7 Templates (14 files)

Reusable document templates:

| File                       | Purpose                      |
|----------------------------|------------------------------|
| `adr.md`                   | Architecture Decision Record |
| `api_spec.md`              | API specification            |
| `case_study.md`            | Case study template          |
| `conversation_record.md`   | Conversation logging         |
| `expert_committee.md`      | Expert committee review      |
| `meeting_notes.md`         | Meeting notes template       |
| `postmortem.md`            | Incident postmortem          |
| `project_setup.md`         | Project setup checklist      |
| `release_notes.md`         | Release notes format         |
| `runbook.md`               | Operational runbook          |
| `session_state.md`         | AI session state             |
| `task_handoff.md`          | Task handoff document        |
| `troubleshooting_guide.md` | Troubleshooting template     |

---

## 3. Complete File List

### Core

- `.knowledge/core/index.md` — Core layer navigation
- `.knowledge/core/principles.md` — 信达雅 philosophy
- `.knowledge/core/quick_reference.md` — Quick reference guide
- `.knowledge/core/defaults.md` — Default configurations

### Guidelines

- `.knowledge/guidelines/index.md` — Guidelines navigation
- `.knowledge/guidelines/quick_start.md` — Quick start guide
- `.knowledge/guidelines/code_style.md` — Code style standards
- `.knowledge/guidelines/ai_collaboration.md` — AI collaboration patterns
- `.knowledge/guidelines/python.md` — Python guidelines
- `.knowledge/guidelines/typescript.md` — TypeScript guidelines
- `.knowledge/guidelines/sql.md` — SQL conventions
- `.knowledge/guidelines/shell.md` — Shell scripting
- `.knowledge/guidelines/documentation.md` — Documentation standards
- `.knowledge/guidelines/engineering.md` — Engineering practices
- `.knowledge/guidelines/security.md` — Security guidelines
- `.knowledge/guidelines/quality.md` — Quality assurance
- `.knowledge/guidelines/cognitive.md` — Cognitive patterns
- `.knowledge/guidelines/planning.md` — Planning guidelines
- `.knowledge/guidelines/success.md` — Success metrics

### Frameworks

- `.knowledge/frameworks/index.md` — Frameworks navigation
- `.knowledge/frameworks/autonomy/index.md` — Autonomy framework
- `.knowledge/frameworks/autonomy/levels.md` — L1-L6 autonomy levels
- `.knowledge/frameworks/cognitive/index.md` — Cognitive framework
- `.knowledge/frameworks/cognitive/expert_committee.md` — Expert committee pattern
- `.knowledge/frameworks/cognitive/information_density.md` — Information density
- `.knowledge/frameworks/design/index.md` — Design framework
- `.knowledge/frameworks/design/axioms.md` — Design axioms
- `.knowledge/frameworks/patterns/index.md` — Patterns framework
- `.knowledge/frameworks/patterns/collaboration.md` — Collaboration patterns
- `.knowledge/frameworks/patterns/decision.md` — Decision patterns
- `.knowledge/frameworks/patterns/integration.md` — Integration patterns
- `.knowledge/frameworks/patterns/persistence.md` — Persistence patterns
- `.knowledge/frameworks/performance/index.md` — Performance framework
- `.knowledge/frameworks/performance/caching_patterns.md` — Caching strategies
- `.knowledge/frameworks/performance/optimization_strategies.md` — Optimization
- `.knowledge/frameworks/performance/profiling_guide.md` — Profiling guide
- `.knowledge/frameworks/resilience/index.md` — Resilience framework
- `.knowledge/frameworks/resilience/timeout_patterns.md` — Timeout patterns
- `.knowledge/frameworks/security/index.md` — Security framework
- `.knowledge/frameworks/security/authentication.md` — Authentication
- `.knowledge/frameworks/security/authorization.md` — Authorization
- `.knowledge/frameworks/security/secrets_management.md` — Secrets management
- `.knowledge/frameworks/security/security_checklist.md` — Security checklist

### References

- `.knowledge/references/knowledge_quick_ref.md` — Knowledge organization patterns
- `.knowledge/references/performance_checklist.md` — Performance optimization checks

*Note: Practices, Scenarios, and Templates files are listed in their respective index.md files.*

---

## 4. Navigation Pattern

```
[layer]/index.md → [layer]/[topic].md → [layer]/[topic]/[detail].md
```

Each layer has an `index.md` for navigation. Use layer indexes for discovery, specific files for detailed guidance.

---

## Related

- `config/sage.yaml` — Main configuration
- `docs/design/00-overview.md` — Design overview
- `.context/index.md` — Project context
- `./index.md` — Root navigation

---

*Part of SAGE Knowledge Base*
