# SAGE Knowledge Base

> **Smart AI-Guided Expertise** — Navigation Entry

---

## Table of Contents

- [1. Project Structure](#1-project-structure)
- [2. Directory Definitions](#2-directory-definitions)
- [3. Quick Access](#3-quick-access)
- [4. CLI Commands](#4-cli-commands)

---

## 1. Project Structure

```
sage-kb/
├── .backups/        # Backup files (hidden, tracked)
├── .context/        # Project-specific knowledge (hidden)
├── .history/        # AI session history (hidden)
├── .archive/        # Historical archives (hidden)
├── .junie/          # AI client configuration (hidden)
├── .logs/           # Runtime logs (hidden, git-ignored)
├── .outputs/        # Intermediate files (hidden, git-ignored)
├── config/          # Runtime configuration
│   ├── capabilities/  # Feature and plugin configs
│   ├── core/          # Core infrastructure configs
│   ├── environments/  # Environment-specific configs
│   ├── knowledge/     # Knowledge management configs
│   ├── services/      # Service layer configs
│   └── sage.yaml      # Main configuration entry
├── .knowledge/         # Generic reusable knowledge
├── docs/            # User-facing documentation
├── src/sage/        # Source code
├── tests/           # Test suite
└── tools/           # Development tools
```

---

## 2. Directory Definitions

### 2.1 Knowledge & Context

| Directory     | Purpose                                                         | Visibility |
|---------------|-----------------------------------------------------------------|------------|
| `.context/`   | Project-specific knowledge (ADRs, conventions, configurations)  | Hidden     |
| `.knowledge/` | Generic, reusable knowledge (principles, frameworks, practices) | Visible    |
| `docs/`       | User-facing documentation (design, API, guides)                 | Visible    |

### 2.2 Configuration & Runtime

| Directory              | Purpose                                            | Visibility           |
|------------------------|----------------------------------------------------|----------------------|
| `config/`              | Runtime configuration (modular YAML structure)     | Visible              |
| `config/core/`         | Core infrastructure (timeout, logging, memory, DI) | Visible              |
| `config/environments/` | Environment-specific configs (dev, prod, test)     | Visible              |
| `config/services/`     | Service layer (CLI, MCP, API)                      | Visible              |
| `config/knowledge/`    | Knowledge management (content, loading, search)    | Visible              |
| `config/capabilities/` | Features and plugins (autonomy, quality)           | Visible              |
| `.backups/`            | Backup files                                       | Hidden (tracked)     |
| `.logs/`               | Runtime log files                                  | Hidden (git-ignored) |
| `.outputs/`            | Intermediate process files                         | Hidden (git-ignored) |

### 2.3 History & Archives

| Directory   | Purpose                                 | Visibility |
|-------------|-----------------------------------------|------------|
| `.history/` | AI session records and task handoffs    | Hidden     |
| `.archive/` | Historical/deprecated content           | Hidden     |
| `.junie/`   | JetBrains Junie AI client configuration | Hidden     |

### 2.4 Development

| Directory   | Purpose                                     | Visibility |
|-------------|---------------------------------------------|------------|
| `src/sage/` | Source code (3-layer architecture)          | Visible    |
| `tests/`    | Test suite                                  | Visible    |
| `tools/`    | Development tools (not imported at runtime) | Visible    |

---

## 3. Quick Access

### 3.1 Knowledge Content

| Layer          | Path                     | Purpose                                   |
|----------------|--------------------------|-------------------------------------------|
| **Core**       | `.knowledge/core/`       | Principles, defaults, quick reference     |
| **Guidelines** | `.knowledge/guidelines/` | Code style, engineering, AI collaboration |
| **Frameworks** | `.knowledge/frameworks/` | Autonomy, timeout, cognitive patterns     |
| **Practices**  | `.knowledge/practices/`  | Documentation, engineering patterns       |
| **References** | `.knowledge/references/` | Quick reference, glossary                 |
| **Scenarios**  | `.knowledge/scenarios/`  | Context presets, workflow triggers        |
| **Templates**  | `.knowledge/templates/`  | Reusable document templates               |

### 3.2 Key Files

| File                            | Purpose                                          |
|---------------------------------|--------------------------------------------------|
| `config/sage.yaml`              | Main configuration (timeouts, triggers, loading) |
| `.knowledge/core/PRINCIPLES.md` | Core philosophy (信达雅)                            |
| `.context/INDEX.md`             | Project-specific context navigation              |
| `.junie/guidelines.md`          | AI collaboration guidelines                      |
| `docs/design/00-OVERVIEW.md`    | Design overview                                  |

---

## 4. CLI Commands

```bash
sage get core          # Load core knowledge
sage search "keyword"  # Search knowledge base
sage serve             # Start MCP server
sage info              # Show system information
```

---

## Related

- `.knowledge/INDEX.md` — Knowledge content navigation
- `.context/INDEX.md` — Project context navigation
- `config/INDEX.md` — Configuration documentation
- `docs/INDEX.md` — User documentation navigation
- `.history/INDEX.md` — Session history navigation
- `.archive/INDEX.md` — Archive navigation

---

*AI Collaboration Knowledge Base*
