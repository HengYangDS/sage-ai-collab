---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~1200
---

# Knowledge Taxonomy & Navigation

> AI collaboration directories, knowledge classification, and lifecycle management

---

## Document Series

This document is part of the Content Structure series:

| Document                       | Content                                |
|--------------------------------|----------------------------------------|
| `06-content-structure.md`      | Directory structure, content organization |
| **06a-knowledge-taxonomy.md** (this) | Knowledge taxonomy, navigation, lifecycle |

---

## Table of Contents

- [1. AI Collaboration Directories](#1-ai-collaboration-directories)
- [2. Knowledge Taxonomy](#2-knowledge-taxonomy)
- [3. Entry Points](#3-entry-points)
- [4. Navigation Standards](#4-navigation-standards)
- [5. Knowledge Lifecycles](#5-knowledge-lifecycles)

---

## 1. AI Collaboration Directories

### 1.1 Project-Level Structure

```
project-root/
├── .junie/                      # AI Client: JetBrains Junie
│   ├── guidelines.md            # PRIMARY ENTRY POINT
│   ├── mcp/mcp.json             # MCP server configurations
│   └── config.yaml              # Client-specific settings
│
├── .cursor/                     # AI Client: Cursor IDE (future)
├── .copilot/                    # AI Client: GitHub Copilot (future)
├── .claude/                     # AI Client: Claude Desktop (future)
│
├── .context/                    # Project Knowledge Base (Local)
│   ├── index.md                 # Project KB navigation
│   ├── project.yaml             # Project metadata
│   ├── decisions/               # Architecture Decision Records
│   ├── conventions/             # Project-specific conventions
│   └── active.md                # Current focus, tasks
│
├── .history/                    # AI Session Management
│   ├── current/state.json       # Active session state
│   ├── conversations/           # Conversation logs
│   └── handoffs/                # Task continuation packages
│
├── .archive/                    # Historical Preservation
│   ├── design_history/          # Historical design iterations
│   ├── deprecated/              # Deprecated features
│   └── migrations/              # Migration records
│
└── .knowledge/                  # Generic Knowledge (Distributable)
    └── ... (package content)
```

### 1.2 Directory Purpose

| Directory     | Purpose                              | Git Track | Scope           |
|---------------|--------------------------------------|-----------|-----------------|
| `.junie/`     | AI client config for JetBrains Junie | Yes       | Client-specific |
| `.context/`   | Project-specific knowledge           | Yes       | Project-local   |
| `.history/`   | AI session records and handoffs      | Partial   | Ephemeral       |
| `.archive/`   | Historical/deprecated content        | Yes       | Preservation    |
| `docs/`       | User-facing documentation            | Yes       | Public          |
| `.knowledge/` | Generic, distributable knowledge     | Yes       | Package         |

### 1.3 Storage Relationship

| Storage       | Location                      | Scope            | Purpose                   |
|---------------|-------------------------------|------------------|---------------------------|
| `.history/`   | Project directory             | Project-specific | Session history, handoffs |
| `MemoryStore` | `~/.local/share/sage/memory/` | Cross-project    | Long-term memory          |

---

## 2. Knowledge Taxonomy

### 2.1 Classification Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    KNOWLEDGE TAXONOMY                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  DISTRIBUTABLE (Packaged with sage)                         │
│  ┌─────────────────────────────────────────┐               │
│  │ .knowledge/                             │               │
│  │ ├── core/        (principles, defaults) │               │
│  │ ├── guidelines/  (engineering guides)   │               │
│  │ ├── frameworks/  (autonomy, cognitive)  │               │
│  │ └── practices/   (best practices)       │               │
│  └─────────────────────────────────────────┘               │
│                         ↓ Generic                           │
│  ───────────────────────────────────────────────────────── │
│                         ↑ Specific                          │
│  ┌─────────────────────────────────────────┐               │
│  │ .context/        (project-specific KB)  │ LOCAL         │
│  │ ├── decisions/   (architecture ADRs)    │               │
│  │ └── conventions/ (project conventions)  │               │
│  └─────────────────────────────────────────┘               │
│                                                             │
│  EPHEMERAL (Session-specific)                               │
│  ┌─────────────────────────────────────────┐               │
│  │ .history/        (AI session state)     │ LOCAL         │
│  │ ├── current/     (active session)       │               │
│  │ └── handoffs/    (task continuation)    │               │
│  └─────────────────────────────────────────┘               │
│                                                             │
│  CLIENT-SPECIFIC (AI tool configuration)                    │
│  ┌─────────────────────────────────────────┐               │
│  │ .junie/, .cursor/, .copilot/            │ LOCAL         │
│  └─────────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Layer Loading Strategy

| Layer | Directory                | Token Budget  | Loading         |
|-------|--------------------------|---------------|-----------------|
| L0    | `index.md`               | ~100 tokens   | **Always Load** |
| L1    | `.knowledge/core/`       | ~500 tokens   | **Always Load** |
| L2    | `.knowledge/guidelines/` | ~1,200 tokens | On-Demand       |
| L3    | `.knowledge/frameworks/` | ~2,000 tokens | On-Demand       |
| L4    | `.knowledge/practices/`  | ~1,500 tokens | On-Demand       |
| L5    | `.knowledge/scenarios/`  | ~500 tokens   | On-Demand       |
| L6    | `.knowledge/templates/`  | ~300 tokens   | On-Demand       |

---

## 3. Entry Points

### 3.1 `.junie/guidelines.md` Template

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

### 3.2 Content Versioning

| Aspect | Approach |
|--------|----------|
| File-level | YAML frontmatter with `version` and `date` |
| Package-level | `.knowledge/version.md` tracking releases |
| Change tracking | Git history with conventional commits |

**Version Lifecycle**:

| Status       | Description             | Action                |
|--------------|-------------------------|-----------------------|
| `draft`      | Work in progress        | Not loaded by default |
| `review`     | Ready for expert review | Load with warning     |
| `stable`     | Production-ready        | Normal loading        |
| `deprecated` | Scheduled for removal   | Load with warning     |

---

## 4. Navigation Standards

### 4.1 5-Level Hierarchy

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

### 4.2 Navigation Decision Matrix

| Content Type      | Location                 | Rationale           |
|-------------------|--------------------------|---------------------|
| Project overview  | `index.md`               | Universal entry     |
| AI client config  | `.junie/`                | Client-specific     |
| Core philosophy   | `.knowledge/core/`       | Always needed       |
| How-to guides     | `.knowledge/guidelines/` | Task-triggered      |
| Deep frameworks   | `.knowledge/frameworks/` | Complex decisions   |
| Project decisions | `.context/decisions/`    | Project-specific    |
| Session history   | `.history/`              | Ephemeral           |
| Design documents  | `docs/design/`           | Technical reference |

---

## 5. Knowledge Lifecycles

### 5.1 Project Knowledge Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐ │
│  │ CAPTURE │ -> │ REFINE  │ -> │ PUBLISH │ -> │ ARCHIVE │ │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘ │
│       │              │              │              │       │
│       v              v              v              v       │
│  .history/      .context/      .knowledge/    .archive/   │
└─────────────────────────────────────────────────────────────┘
```

| Phase   | Location      | Trigger               | Action                            |
|---------|---------------|-----------------------|-----------------------------------|
| CAPTURE | `.history/`   | Every session         | Auto-save conversations, handoffs |
| REFINE  | `.context/`   | Sprint end, milestone | Extract ADRs, conventions         |
| PUBLISH | `.knowledge/` | Quarterly review      | Promote generic knowledge         |
| ARCHIVE | `.archive/`   | Content superseded    | Preserve historical records       |

### 5.2 Update Frequency by Layer

| Layer | Directory                | Frequency        | Governance       |
|-------|--------------------------|------------------|------------------|
| L1    | `.knowledge/core/`       | Rare (1-2x/year) | Expert Committee |
| L2    | `.knowledge/guidelines/` | Quarterly        | 2+ reviewers     |
| L3    | `.knowledge/frameworks/` | As needed        | Expert review    |
| L4    | `.knowledge/practices/`  | Monthly          | Standard PR      |

---

## Related

- `docs/design/06-content-structure.md` — Directory structure overview
- `docs/design/01-architecture.md` — Architecture design
- `.knowledge/practices/documentation/knowledge_organization.md` — Organization guide

---

*Part of SAGE Knowledge Base*
