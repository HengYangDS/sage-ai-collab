---
title: SAGE Knowledge Base - Content Structure & Knowledge Taxonomy
version: 0.1.0
date: 2025-11-28
status: production-ready
---

# Content Structure & Knowledge Taxonomy

> **Content organization, knowledge layers, and AI collaboration directories**

## Overview

This document covers:

1. **Directory Structure** - Production-ready project layout
2. **Content Organization** - Knowledge content hierarchy
3. **Chapter Consolidation** - Guidelines restructuring (16 → 10)
4. **AI Collaboration Directories** - Project-level AI artifacts
5. **Knowledge Taxonomy** - 4-layer classification system

---

## 6.1 Directory Structure (Production-Ready)

> **Status**: Production-Ready Design
> **Key Innovations**: Core-Services-Capabilities architecture, unified logging, dev tools isolation

```
sage/                          # Project root directory
│
├── README.md                          # 🔹 Project documentation
├── LICENSE                            # 🔹 Open source license
├── CHANGELOG.md                       # 🔹 Change log
├── pyproject.toml                     # 🔹 Python project configuration
├── Makefile                           # 🔹 Make development commands
├── justfile                           # 🔹 Just commands (cross-platform, modern)
├── .pre-commit-config.yaml            # 🔹 Pre-commit hook configuration
├── .env.example                       # 🔹 Environment variables template
├── .gitignore                         # 🔹 Git ignore rules
│
├── sage.yaml                          # 🔹 Smart loading configuration
├── index.md                           # 🔹 Navigation entry (~100 tokens, Always Load)
├── features.yaml                      # 🔹 Feature flags configuration
│
├── docs/                              # 📖 Project documentation
│   ├── design/                        #    Design documents (00-08)
│   ├── api/                           #    API documentation
│   ├── guides/                        #    Development guides
│   └── standards/                     #    Standards documentation
│
├── .knowledge/                           # 📚 Knowledge content directory
│   ├── core/                          # 🔸 Core principles (~500 tokens)
│   ├── guidelines/                    # 🔸 Engineering guidelines (~1,200 tokens)
│   ├── frameworks/                    # 🔸 Deep frameworks (~2,000 tokens)
│   ├── practices/                     # 🔸 Best practices (~1,500 tokens)
│   ├── scenarios/                     # 🔸 Scenario presets (~500 tokens)
│   └── templates/                     # 🔸 Reusable templates (~300 tokens)
│
├── src/sage/                          # 💻 Source code (modular architecture)
│   ├── __init__.py                    #    Package entry, version info
│   ├── __main__.py                    #    Unified entry point (python -m sage)
│   ├── interfaces/                    #    Protocol definitions (centralized)
│   ├── domain/                        #    Business domain models
│   ├── core/                          # 🔷 Core layer (<500 lines)
│   │   └── logging/                   #    Unified logging subpackage
│   ├── services/                      # 🔶 Services layer (CLI, MCP, API)
│   ├── capabilities/                  # 🆕 Runtime capabilities (exposed via MCP)
│   │   ├── analyzers/                 #    Quality, Content analyzers
│   │   ├── checkers/                  #    Link checker
│   │   └── monitors/                  #    Health monitor
│   └── plugins/                       # 🔌 Plugin infrastructure
│       └── bundled/                   #    Bundled plugin implementations
│
├── tools/                             # 🔧 Dev-Only (NOT imported at runtime)
│   ├── monitors/                      #    TimeoutMonitor (dev performance)
│   └── dev_scripts/                   #    Development setup scripts
│
├── tests/                             # 🧪 Test directory (mirrors src/)
│   ├── conftest.py                    #    Global pytest fixtures
│   ├── fixtures/                      #    Test data (sample content, mocks)
│   ├── unit/                          #    Unit tests
│   ├── integration/                   #    Integration tests
│   ├── tools/                         #    Tool tests
│   └── performance/                   #    Performance tests + benchmarks
│
├── examples/                          # 📝 Usage examples
└── scripts/                           # 🛠️ Development scripts
```

---

## 6.2 Content Directory Detail

### .knowledge/core/ - Core Principles (~500 tokens, Always Load)

| File                 | Purpose                                  |
|----------------------|------------------------------------------|
| `principles.md`      | Xin-Da-Ya philosophy, core values        |
| `quick_reference.md` | 5 critical questions, autonomy quick ref |
| `defaults.md`        | Default behaviors, calibration standards |

### .knowledge/guidelines/ - Engineering Guidelines (~1,200 tokens, On-Demand)

| File                  | Purpose                             | Lines |
|-----------------------|-------------------------------------|-------|
| `quick_start.md`      | 3-minute quick start                | ~60   |
| `planning_design.md`  | Planning and architecture           | ~80   |
| `code_style.md`       | Code style standards                | ~150  |
| `engineering.md`      | Config/test/perf/change/maintain    | ~120  |
| `documentation.md`    | Documentation standards             | ~100  |
| `python.md`           | Python best practices               | ~130  |
| `ai_collaboration.md` | AI collaboration and autonomy       | ~200  |
| `cognitive.md`        | Cognitive enhancement core          | ~100  |
| `quality.md`          | Quality framework                   | ~80   |
| `success.md`          | Xin-Da-Ya mapping, success criteria | ~80   |

### .knowledge/frameworks/ - Deep Frameworks (~2,000 tokens, On-Demand)

| Directory        | File                  | Purpose                                         |
|------------------|-----------------------|-------------------------------------------------|
| `autonomy/`      | `levels.md`           | 6-level autonomy spectrum definition            |
| `cognitive/`     | `expert_committee.md` | Expert committee, chain-of-thought, iteration   |
| `collaboration/` | `patterns.md`         | Collaboration patterns, instruction engineering |
| `decision/`      | `quality_angles.md`   | Quality angles, expert roles                    |
| `timeout/`       | `hierarchy.md`        | Timeout principles, strategies, recovery        |

### .knowledge/practices/ - Best Practices (~1,500 tokens, On-Demand)

| Directory           | File                         | Purpose                         |
|---------------------|------------------------------|---------------------------------|
| `ai_collaboration/` | `workflow.md`                | Workflow, interaction patterns  |
| `documentation/`    | `documentation_standards.md` | Documentation standards (SSOT)  |
| `engineering/`      | `patterns.md`                | Design patterns, best practices |

### .knowledge/scenarios/ - Scenario Presets (~500 tokens, On-Demand)

| Directory         | File         | Purpose                                    |
|-------------------|--------------|--------------------------------------------|
| `python_backend/` | `context.md` | Context configuration, specific guidelines |

### .knowledge/templates/ - Reusable Templates (~300 tokens, On-Demand)

| File               | Purpose                         |
|--------------------|---------------------------------|
| `project_setup.md` | Project initialization template |

---

## 6.3 Directory Statistics

| Directory                        | Files    | Subdirs | Primary Function                              |
|----------------------------------|----------|---------|-----------------------------------------------|
| Root                             | 12       | 8       | Project entry, config, dev toolchain          |
| docs/                            | 7        | 4       | Project documentation (+standards/)           |
| .knowledge/core/                    | 3        | 0       | Core principles (~500 tokens, Always Load)    |
| .knowledge/guidelines/              | 11       | 0       | Engineering guidelines (+guidelines_index)    |
| .knowledge/frameworks/              | 5        | 5       | Deep frameworks (~2,000 tokens)               |
| .knowledge/practices/               | 4        | 4       | Best practices (+decisions/)                  |
| .knowledge/scenarios/               | 1        | 1       | Scenario presets (~500 tokens)                |
| .knowledge/templates/               | 2        | 0       | Templates (+expert_committee.md)              |
| src/sage/interfaces/             | 2        | 0       | Protocol definitions (centralized)            |
| src/sage/domain/                 | 3        | 0       | Business domain models                        |
| src/sage/core/                   | 9        | 1       | Core layer (<500 lines)                       |
| src/sage/core/logging/           | 4        | 0       | Unified logging (structlog + stdlib)          |
| src/sage/services/               | 4        | 0       | Services layer (CLI, MCP, API)                |
| src/sage/capabilities/           | 1        | 3       | Runtime capabilities (exposed via MCP)        |
| src/sage/capabilities/analyzers/ | 3        | 0       | Analyzers (quality, content, structure)       |
| src/sage/capabilities/checkers/  | 2        | 0       | Checkers (links)                              |
| src/sage/capabilities/monitors/  | 2        | 0       | Monitors (health)                             |
| src/sage/plugins/                | 3        | 1       | Plugin infrastructure (interfaces + registry) |
| src/sage/plugins/bundled/        | 3        | 0       | Bundled plugin implementations                |
| tools/                           | 1        | 2       | Dev-only tools (NOT imported at runtime)      |
| tools/monitors/                  | 2        | 0       | TimeoutMonitor (dev performance)              |
| tools/dev_scripts/               | 2        | 0       | Development scripts                           |
| tests/fixtures/                  | 4        | 3       | Test data (sample content, mocks, configs)    |
| tests/unit/                      | 7        | 2       | Unit tests (mirrors src/ structure)           |
| tests/integration/               | 3        | 0       | Integration tests                             |
| tests/tools/                     | 2        | 0       | Tool tests                                    |
| tests/performance/               | 3        | 1       | Performance tests + benchmarks                |
| examples/                        | 5        | 0       | Usage examples                                |
| scripts/                         | 3        | 0       | Development scripts                           |
| **Total**                        | **~105** | **~40** | Production-ready structure                    |

---

## 6.4 Chapter Consolidation (16 → 10)

The guidelines were consolidated from 16 chapters to 10 for better organization:

| Original Chapters                     | New Chapter         | Lines | Rationale     |
|---------------------------------------|---------------------|-------|---------------|
| 0. Quick Reference                    | quick_start.md      | ~60   | Keep as-is    |
| 1. Planning + 2. Design               | planning_design.md  | ~80   | Merge short   |
| 3. Code Style                         | code_style.md       | ~150  | Keep as-is    |
| 4-8. Config/Test/Perf/Change/Maintain | engineering.md      | ~120  | Merge 5 mini  |
| 9. Documentation                      | documentation.md    | ~100  | Keep as-is    |
| 10. Python + 11. Decorator            | python.md           | ~130  | Merge overlap |
| 12. AI Collab + 13. Autonomy          | ai_collaboration.md | ~200  | Unify AI      |
| 14. Cognitive (core)                  | cognitive.md        | ~100  | Extract core  |
| (new) Quality                         | quality.md          | ~80   | From 14       |
| 15. Success                           | success.md          | ~80   | Streamline    |

**Result**: 16 → 10 chapters, ~1,100 lines (from ~1,464, -25%)

---

## 6.5 AI Collaboration Directory Structure

### 6.5.1 Project-Level AI Directories

```
project-root/
│
├── .junie/                      # 🤖 AI Client: JetBrains Junie
│   ├── guidelines.md            # 📋 PRIMARY ENTRY POINT (required by Junie)
│   ├── mcp/
│   │   └── mcp.json             # MCP server configurations
│   ├── prompts/                 # Client-specific prompt overrides (optional)
│   └── config.yaml              # Client-specific settings (optional)
│
├── .cursor/                     # 🤖 AI Client: Cursor IDE (future)
├── .copilot/                    # 🤖 AI Client: GitHub Copilot (future)
├── .claude/                     # 🤖 AI Client: Claude Desktop (future)
│
├── .context/                    # 📚 Project Knowledge Base (Local, Non-Distributed)
│   ├── index.md                 # Project KB navigation & overview
│   ├── project.yaml             # Project metadata, tech stack, dependencies
│   ├── decisions/               # Architecture Decision Records (ADRs)
│   │   ├── README.md            # ADR template and index
│   │   └── 001_example.md       # Example ADR
│   ├── conventions/             # Project-specific conventions
│   │   └── naming.md            # Naming conventions
│   └── active.md                # Current focus, tasks, blockers
│
├── .history/                    # 💬 AI Session Management (Project-Scoped)
│   ├── .gitignore               # Ignore sensitive/ephemeral data
│   ├── current/                 # Current session state
│   │   └── state.json           # Active session state
│   ├── conversations/           # Conversation logs (selective tracking)
│   └── handoffs/                # Task continuation packages
│
├── .archive/                    # 📦 Archive (Historical Preservation)
│   ├── design_history/          # Historical design iterations
│   ├── deprecated/              # Deprecated features/code
│   └── migrations/              # Migration records
│
├── docs/                        # 📖 Documentation (Public, User-Facing)
│   ├── design/                  # Design documents
│   ├── api/                     # API documentation
│   └── guides/                  # User guides
│
└── .knowledge/                     # 📚 Generic Knowledge (Distributable)
    └── ... (package content)
```

### 6.5.2 Directory Purpose & Differentiation

| Directory   | Purpose                                        | Hidden | Git Track | Scope           |
|-------------|------------------------------------------------|--------|-----------|-----------------|
| `.junie/`   | AI client config for JetBrains Junie           | Yes    | Yes       | Client-specific |
| `.context/` | Project-specific knowledge (ADRs, conventions) | Yes    | Yes       | Project-local   |
| `.history/` | AI session records and task handoffs           | Yes    | Partial   | Ephemeral       |
| `.archive/` | Historical/deprecated content                  | Yes    | Yes       | Preservation    |
| `docs/`     | User-facing documentation                      | No     | Yes       | Public          |
| `.knowledge/`  | Generic, distributable knowledge               | No     | Yes       | Package         |

---

## 6.6 Knowledge Taxonomy

```
┌─────────────────────────────────────────────────────────────────┐
│                    KNOWLEDGE TAXONOMY                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  DISTRIBUTABLE (Packaged with sage)                             │
│  ┌─────────────────────────────────────────┐                   │
│  │ .knowledge/                                │                   │
│  │ ├── core/        (principles, defaults) │                   │
│  │ ├── guidelines/  (engineering guides)   │                   │
│  │ ├── frameworks/  (autonomy, cognitive)  │                   │
│  │ └── practices/   (best practices)       │                   │
│  └─────────────────────────────────────────┘                   │
│                         ↓ Generic                               │
│  ─────────────────────────────────────────────────────────────  │
│                         ↑ Specific                              │
│  ┌─────────────────────────────────────────┐                   │
│  │ .context/        (project-specific KB)  │ LOCAL             │
│  │ ├── decisions/   (architecture ADRs)    │                   │
│  │ ├── conventions/ (project conventions)  │                   │
│  │ └── active.md    (current focus)        │                   │
│  └─────────────────────────────────────────┘                   │
│                                                                 │
│  EPHEMERAL (Session-specific)                                   │
│  ┌─────────────────────────────────────────┐                   │
│  │ .history/        (AI session state)     │ LOCAL             │
│  │ ├── current/     (active session)       │                   │
│  │ ├── conversations/ (past sessions)      │                   │
│  │ └── handoffs/    (task continuation)    │                   │
│  └─────────────────────────────────────────┘                   │
│                                                                 │
│  CLIENT-SPECIFIC (AI tool configuration)                        │
│  ┌─────────────────────────────────────────┐                   │
│  │ .junie/          (JetBrains Junie)      │ LOCAL             │
│  │ .cursor/         (Cursor IDE)           │                   │
│  │ .copilot/        (GitHub Copilot)       │                   │
│  └─────────────────────────────────────────┘                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Knowledge Layer Loading Strategy

| Layer | Directory             | Token Budget  | Loading         |
|-------|-----------------------|---------------|-----------------|
| L0    | `index.md`            | ~100 tokens   | **Always Load** |
| L1    | `.knowledge/core/`       | ~500 tokens   | **Always Load** |
| L2    | `.knowledge/guidelines/` | ~1,200 tokens | On-Demand       |
| L3    | `.knowledge/frameworks/` | ~2,000 tokens | On-Demand       |
| L4    | `.knowledge/practices/`  | ~1,500 tokens | On-Demand       |
| L5    | `.knowledge/scenarios/`  | ~500 tokens   | On-Demand       |
| L6    | `.knowledge/templates/`  | ~300 tokens   | On-Demand       |

---

## 6.7 `.junie/guidelines.md` Entry Point

The `.junie/guidelines.md` file is the **primary entry point** for JetBrains Junie AI collaboration. Template:

```markdown
# Project Guidelines for AI Collaboration

## Project Overview

[Brief project description, version, status]

## Tech Stack

[Technologies, frameworks, dependencies]

## Coding Standards

[Key conventions: naming, formatting, architecture rules]

## Important Files

[Critical files AI should know about]

## AI Collaboration Rules

[Autonomy levels, key behaviors, expert committee pattern]

## References

[@file references to other important files]
```

---

## 6.8 Storage Relationship

| Storage       | Location                      | Scope            | Purpose                       |
|---------------|-------------------------------|------------------|-------------------------------|
| `.history/`   | Project directory             | Project-specific | Session history, handoffs     |
| `MemoryStore` | `~/.local/share/sage/memory/` | Cross-project    | Long-term entities, relations |

Both systems work together:

- `.history/` for project-scoped, team-shareable session data
- `MemoryStore` for user-level, cross-project persistent memory

---

## 6.9 Content Versioning Strategy

Knowledge content follows semantic versioning principles for maintainability:

### Version Tracking

| Aspect              | Approach                                          |
|---------------------|---------------------------------------------------|
| **File-level**      | YAML frontmatter with `version` and `date` fields |
| **Package-level**   | `.knowledge/VERSION` file tracking content releases  |
| **Change tracking** | Git history with conventional commit messages     |

### Frontmatter Template

```yaml
---
title: Document Title
version: 1.0.0
date: 2025-11-28
status: stable  # draft | review | stable | deprecated
---
```

### Version Lifecycle

| Status       | Description             | Action                |
|--------------|-------------------------|-----------------------|
| `draft`      | Work in progress        | Not loaded by default |
| `review`     | Ready for expert review | Load with warning     |
| `stable`     | Production-ready        | Normal loading        |
| `deprecated` | Scheduled for removal   | Load with warning     |

### Compatibility Rules

- **Major version** (1.0 → 2.0): Breaking changes, requires migration
- **Minor version** (1.0 → 1.1): New content, backward compatible
- **Patch version** (1.0.0 → 1.0.1): Fixes, clarifications only

---

## 6.10 Navigation Standards

> **Source**: Level 5 Expert Committee Design Optimization (Issue 4)

### 5-Level Navigation Hierarchy

```
L0: index.md (Project Overview, ~100 tokens)
    └── What is this project? Quick links, How to navigate

L1: .junie/guidelines.md (AI Client Entry, ~200 tokens)
    └── Tech stack, Coding standards summary, @file references

L2: .knowledge/core/*.md (Core Principles, ~500 tokens)
    └── principles.md, quick_reference.md, defaults.md

L3: .knowledge/guidelines/*.md (On-Demand, ~100-200/file)
    └── Triggered by keywords in user query

L4: .knowledge/frameworks/*.md (Deep Dive, ~300-500/file)
    └── Loaded for complex decision tasks
```

### Navigation Decision Matrix

| Content Type      | Location              | Rationale           |
|-------------------|-----------------------|---------------------|
| Project overview  | `index.md`            | Universal entry     |
| AI client config  | `.junie/`             | Client-specific     |
| Core philosophy   | `.knowledge/core/`       | Always needed       |
| How-to guides     | `.knowledge/guidelines/` | Task-triggered      |
| Deep frameworks   | `.knowledge/frameworks/` | Complex decisions   |
| Project decisions | `.context/decisions/` | Project-specific    |
| Session history   | `.history/`           | Ephemeral           |
| Design documents  | `docs/design/`        | Technical reference |

---

## 6.11 Knowledge Lifecycles

> **Source**: Level 5 Expert Committee Design Optimization (Issues 7-8)

### Project Knowledge Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                 PROJECT KNOWLEDGE LIFECYCLE                      │
│                                                                 │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐     │
│  │ CAPTURE │ -> │ REFINE  │ -> │ PUBLISH │ -> │ ARCHIVE │     │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘     │
│       │              │              │              │           │
│       v              v              v              v           │
│  .history/      .context/      .knowledge/      .archive/        │
│  sessions/      decisions/     (generic)    design_history/   │
└─────────────────────────────────────────────────────────────────┘
```

| Phase   | Location    | Trigger               | Action                            |
|---------|-------------|-----------------------|-----------------------------------|
| CAPTURE | `.history/` | Every session         | Auto-save conversations, handoffs |
| REFINE  | `.context/` | Sprint end, milestone | Extract ADRs, conventions         |
| PUBLISH | `.knowledge/`  | Quarterly review      | Promote generic knowledge         |
| ARCHIVE | `.archive/` | Content superseded    | Preserve historical records       |

### Content Knowledge Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                 CONTENT (DISTRIBUTABLE) LIFECYCLE               │
│                                                                 │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐    │
│  │ PROPOSE  │ → │ REVIEW   │ → │ INTEGRATE│ → │ RELEASE  │    │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘    │
│       │              │              │              │            │
│       v              v              v              v            │
│  GitHub Issue   Expert Review   .knowledge/*    PyPI Release      │
│  or PR          (Level 4-5)     directory    (semver)          │
└─────────────────────────────────────────────────────────────────┘
```

### Update Frequency by Layer

| Layer | Directory             | Frequency        | Governance       |
|-------|-----------------------|------------------|------------------|
| L1    | `.knowledge/core/`       | Rare (1-2x/year) | Expert Committee |
| L2    | `.knowledge/guidelines/` | Quarterly        | 2+ reviewers     |
| L3    | `.knowledge/frameworks/` | As needed        | Expert review    |
| L4    | `.knowledge/practices/`  | Monthly          | Standard PR      |

---

## References

- **Architecture**: See `01-architecture.md`
- **SAGE Protocol**: See `02-sage-protocol.md`
- **Plugin & Memory**: See `05-plugin-memory.md`
- **Timeout & Loading**: See `04-timeout-loading.md`

---

**Document Status**: ✅ Level 5 Expert Committee Approved  
**Last Updated**: 2025-11-29
