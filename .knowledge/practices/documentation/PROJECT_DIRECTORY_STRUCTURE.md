---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~2150
---

# Project Directory Structure Patterns

> Universal directory organization patterns for AI-collaborative projects

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Directory Categories](#2-directory-categories)
- [3. Hidden Directory Conventions](#3-hidden-directory-conventions)
- [4. Visible Directory Conventions](#4-visible-directory-conventions)
- [5. Placement Decision Tree](#5-placement-decision-tree)
- [6. File Naming Conventions](#6-file-naming-conventions)

---

## 1. Overview

### 1.1 Design Principles

| Principle                  | Description                                           |
|----------------------------|-------------------------------------------------------|
| **Separation of Concerns** | Each directory has a single, clear purpose            |
| **Visibility Convention**  | Hidden (`.prefix`) for internal, visible for external |
| **Git Policy Clarity**     | Clear tracking rules for each directory               |
| **MECE Organization**      | Mutually exclusive, collectively exhaustive           |

### 1.2 Standard Project Layout

```
project/
├── .context/        # Project-specific knowledge (hidden, tracked)
├── .history/        # Session history and handoffs (hidden, tracked)
├── .archive/        # Historical/deprecated content (hidden, tracked)
├── .backups/        # Backup files before changes (hidden, tracked)
├── .logs/           # Runtime log files (hidden, ignored)
├── .outputs/        # Intermediate process files (hidden, ignored)
├── .knowledge/         # Generic reusable knowledge (visible, tracked)
├── docs/            # User-facing documentation (visible, tracked)
├── src/             # Source code (visible, tracked)
└── tests/           # Test suite (visible, tracked)
```

---

## 2. Directory Categories

### 2.1 By Visibility

| Category    | Prefix | Purpose                 | Example               |
|-------------|--------|-------------------------|-----------------------|
| **Hidden**  | `.`    | Internal, tooling, meta | `.context/`, `.logs/` |
| **Visible** | None   | Public, deliverable     | `docs/`, `src/`       |

### 2.2 By Git Policy

| Policy      | Directories                                                                | Rationale                                  |
|-------------|----------------------------------------------------------------------------|--------------------------------------------|
| **Tracked** | `.context/`, `.history/`, `.archive/`, `.backups/`, `.knowledge/`, `docs/` | Preserve history and collaboration context |
| **Ignored** | `.logs/`, `.outputs/`                                                      | Runtime artifacts, regenerable             |

### 2.3 By Content Lifecycle

| Stage      | Directory                                   | Description            |
|------------|---------------------------------------------|------------------------|
| Active     | `.context/`, `.knowledge/`, `docs/`, `src/` | Current, maintained    |
| Session    | `.history/`                                 | Collaboration records  |
| Backup     | `.backups/`                                 | Pre-change snapshots   |
| Deprecated | `.archive/`                                 | Historical reference   |
| Ephemeral  | `.logs/`, `.outputs/`                       | Temporary, regenerable |

---

## 3. Hidden Directory Conventions

### 3.1 `.context/` — Project-Specific Knowledge

**Purpose**: Store knowledge specific to this project only.

| Subdirectory    | Content                               |
|-----------------|---------------------------------------|
| `conventions/`  | Project-specific coding conventions   |
| `decisions/`    | Architecture Decision Records (ADRs)  |
| `intelligence/` | Learned AI patterns for this codebase |

**When to use**: Project-specific rules, decisions, patterns that don't apply universally.

### 3.2 `.history/` — Session History

**Purpose**: Store AI session records and task handoffs.

| Subdirectory     | Content                |
|------------------|------------------------|
| `current/`       | Current session state  |
| `conversations/` | Conversation records   |
| `handoffs/`      | Task handoff documents |

**When to use**: Session continuity, collaboration handoffs, context preservation.

### 3.3 `.archive/` — Historical Archives

**Purpose**: Store deprecated or historical content for reference.

**Organization**: By month (`YYYYMM/`) or by topic.

**When to use**: Content that's no longer active but may be needed for reference.

### 3.4 `.backups/` — Backup Files

**Purpose**: Store backup copies before major changes or refactoring.

**Organization**: By date (`YYYY-MM-DD/`) or by topic.

**When to use**: Pre-refactoring snapshots, configuration backups, critical data preservation.

**Best Practices**:

- Create backups before major refactoring
- Include brief description in backup folder name
- Clean up old backups periodically

### 3.5 `.logs/` — Runtime Logs

**Purpose**: Store runtime log files generated by the application.

**Git Policy**: Ignored (use `.gitkeep` to preserve directory).

**When to use**: Application logs, debug output, runtime diagnostics.

### 3.6 `.outputs/` — Intermediate Files

**Purpose**: Store intermediate process files, test outputs, generated artifacts.

**Git Policy**: Ignored (use `.gitkeep` to preserve directory).

**When to use**: Test results, generated reports, temporary processing artifacts.

---

## 4. Visible Directory Conventions

### 4.1 `.knowledge/` — Generic Knowledge

**Purpose**: Universal knowledge that helps AI collaboration, reusable across projects.

| Subdirectory  | Content                           |
|---------------|-----------------------------------|
| `core/`       | Core principles, defaults         |
| `guidelines/` | Code style, engineering standards |
| `frameworks/` | Deep conceptual frameworks        |
| `practices/`  | Best practices, workflows         |
| `scenarios/`  | Context-specific presets          |
| `templates/`  | Reusable document templates       |

**When to use**: Knowledge that applies universally, not project-specific.

### 4.2 `docs/` — User Documentation

**Purpose**: User-facing documentation for the project.

| Subdirectory | Content                   |
|--------------|---------------------------|
| `design/`    | Design documents          |
| `api/`       | API documentation         |
| `guides/`    | User and developer guides |

**When to use**: External documentation, user guides, API references.

---

## 5. Placement Decision Tree

```
Is this content project-specific?
├─ YES → .context/
│   ├─ Coding convention? → .context/conventions/
│   ├─ Architecture decision? → .context/decisions/
│   └─ AI pattern? → .context/intelligence/
│
└─ NO (Generic/Reusable) → .knowledge/

Is this user-facing documentation?
└─ YES → docs/

Is this session-related?
└─ YES → .history/

Is this deprecated content?
└─ YES → .archive/

Is this a backup before major changes?
└─ YES → .backups/

Is this a runtime log?
└─ YES → .logs/

Is this an intermediate/generated file?
└─ YES → .outputs/
```

### Quick Reference

| Content Type              | Location                 |
|---------------------------|--------------------------|
| Project conventions       | `.context/conventions/`  |
| Universal guidelines      | `.knowledge/guidelines/` |
| ADR records               | `.context/decisions/`    |
| API documentation         | `docs/api/`              |
| Session handoffs          | `.history/handoffs/`     |
| Deprecated code           | `.archive/`              |
| Pre-refactoring snapshots | `.backups/`              |
| Runtime logs              | `.logs/`                 |
| Test outputs              | `.outputs/`              |

---

## 6. File Naming Conventions

| Type           | Convention                  | Example                        |
|----------------|-----------------------------|--------------------------------|
| Markdown       | `UPPER_SNAKE_CASE.md`       | `DIRECTORY_STRUCTURE.md`       |
| ADR            | `ADR-NNNN-TITLE.md`         | `ADR-0001-FASTMCP-CHOICE.md`   |
| Session        | `YYYY-MM-DD-TOPIC.md`       | `2025-11-29-TIMEOUT.md`        |
| Handoff        | `YYYY-MM-DD-HANDOFF.md`     | `2025-11-29-API-HANDOFF.md`    |
| Index          | `INDEX.md`                  | `INDEX.md`                     |
| Special        | `UPPERCASE.md`              | `README.md`, `CHANGELOG.md`    |
| Archive folder | `YYYYMM/`                   | `202511/`                      |
| Backup folder  | `YYYY-MM-DD-DESCRIPTION/`   | `2025-11-29-PRE-REFACTOR/`     |

**Rationale**: Uppercase naming provides clear visual distinction for documentation files.

### 6.1 Naming Exceptions

| Directory | Convention      | Example           | Rationale                                    |
|-----------|-----------------|-------------------|----------------------------------------------|
| `.junie/` | `lowercase.md`  | `guidelines.md`   | AI client config directory follows tool convention |

**Note**: The `.junie/` directory is the JetBrains Junie AI client configuration directory. Its root `guidelines.md` file must use lowercase naming to comply with the Junie tool's expected file structure.

---

## Related

- `.knowledge/practices/documentation/KNOWLEDGE_ORGANIZATION.md` — Knowledge content layer architecture
- `.knowledge/practices/documentation/DOCUMENTATION_STANDARDS.md` — Documentation format standards (SSOT)
- `.knowledge/frameworks/design/AXIOMS.md` — Design principles (MECE, SSOT)

---

*Part of SAGE Knowledge Base*
