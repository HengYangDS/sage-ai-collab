# SAGE Knowledge Base - Project Guidelines

> **Type**: 📌 Project-specific (customized for this project)
> **Last Updated**: 2025-11-30
> **Version**: 0.1.0
> **Status**: Alpha - Under active development and testing

---

## 📋 Project Overview

**SAGE Knowledge Base (sage-kb)** is a production-grade knowledge management system designed for
AI-human collaboration. It provides structured knowledge via CLI, MCP, and API services with built-in timeout protection
and smart loading.

### Design Philosophy

**信达雅 (Xin-Da-Ya)**:

- **信 (Xin/Faithfulness)**: Accurate, reliable, testable
- **达 (Da/Clarity)**: Clear, maintainable, structured
- **雅 (Ya/Elegance)**: Refined, balanced, sustainable

---

## 🛠️ Tech Stack

| Category     | Technology                 |
|--------------|----------------------------|
| **Language** | Python 3.12+               |
| **CLI**      | Typer + Rich               |
| **MCP**      | FastMCP                    |
| **API**      | FastAPI + Uvicorn          |
| **Config**   | PyYAML + Pydantic-Settings |
| **Logging**  | structlog + stdlib logging |
| **Testing**  | pytest + pytest-asyncio    |
| **Linting**  | Ruff + MyPy                |

---

## 📁 Project Structure

```
sage-kb/
├── .junie/          # JetBrains Junie configuration (this directory)
├── .context/        # Project-specific knowledge base
├── .history/        # AI session history and handoffs
├── .outputs/        # Intermediate process files (git-ignored)
├── config/          # Runtime configuration (modular YAML)
├── docs/            # User-facing documentation
├── content/         # Generic knowledge (distributable)
├── src/sage/        # Source code (3-layer architecture)
├── tools/           # Development tools
└── tests/           # Test suite
```

### Key Directories

| Directory   | Purpose                                        | Visibility |
|-------------|------------------------------------------------|------------|
| `.junie/`   | AI client config for JetBrains Junie           | Hidden     |
| `.context/` | Project-specific knowledge (ADRs, conventions) | Hidden     |
| `.history/` | AI session records and task handoffs           | Hidden     |
| `.outputs/` | Intermediate process files                     | Hidden     |
| `config/`   | Runtime configuration (modular YAML structure) | Visible    |
| `docs/`     | User-facing documentation                      | Visible    |
| `content/`  | Generic, distributable knowledge               | Visible    |

---

## 📐 Coding Standards

> **Reference**: See `content/guidelines/python.md` and `.context/conventions/naming.md` for full details

**Quick Summary:**
- **Formatter**: Ruff (line-length: 88)
- **Type Hints**: Required
- **Docstrings**: Google style
- **Naming**: Files `snake_case.py`, Classes `PascalCase`, Constants `UPPER_SNAKE_CASE`
- **Architecture**: Core → Services → Capabilities (see `.context/conventions/code_patterns.md`)

---

## 📄 Important Files

| File                 | Purpose                                          |
|----------------------|--------------------------------------------------|
| `config/sage.yaml`   | Main configuration (timeouts, triggers, loading) |
| `docs/design/`       | Design documents (architecture, services, etc.)  |
| `src/sage/core/`     | Core layer (loader, timeout, config)             |
| `src/sage/services/` | Service layer (CLI, MCP, API)                    |
| `pyproject.toml`     | Python project configuration                     |
| `index.md`           | Knowledge base navigation entry                  |

---

## 🚀 Quick Commands

```bash
# Testing
pytest tests/ -v                    # Run all tests
pytest tests/unit/ -v               # Unit tests only
pytest tests/integration/ -v        # Integration tests only

# Services
sage serve                          # Start MCP server
sage get --layer core               # Get core layer content
sage search "timeout"               # Search knowledge base
sage info                           # System information

# Development
ruff check src/                     # Lint check
ruff format src/                    # Format code
mypy src/                           # Type check
```

---

## 📁 Key Paths

| Category | Path | Purpose |
|----------|------|---------|
| **Conventions** | `.context/conventions/` | Naming, patterns, structure |
| **Policies** | `.context/policies/` | Timeouts, loading, runtime |
| **ADRs** | `.context/decisions/` | Architecture decisions |
| **AI Patterns** | `.context/intelligence/` | Interaction patterns |
| **Config** | `config/sage.yaml` | Main configuration |
| **Core Code** | `src/sage/core/` | Core layer |
| **Services** | `src/sage/services/` | CLI, MCP, API |

---

## ⏱️ Timeout Hierarchy

> **Reference**: See `.context/policies/timeout_hierarchy.md` for full details

**SAGE-specific timeout configuration**:

| Tier | Duration | SAGE Use Case |
|------|----------|---------------|
| T1 | 100ms | Cache lookup |
| T2 | 500ms | Single file read |
| T3 | 2s | Layer load |
| T4 | 5s | Full KB load |
| T5 | 10s | Complex analysis |

---

## 🔗 References

- **Project Variables**: `project.yaml`
- **Design Documents**: `docs/design/00-overview.md`
- **Documentation Standards**: `content/practices/documentation/DOCUMENTATION_STANDARDS.md`
- **Documentation Index**: `docs/index.md`
- **Configuration**: `config/sage.yaml`
- **Project Context**: `.context/index.md`
- **Knowledge Content**: `content/index.md`
- **Directory Conventions**: `content/practices/documentation/project_directory_structure.md`
- **Timeout Hierarchy**: `.context/policies/timeout_hierarchy.md`
- **Core Principles**: `content/core/principles.md`

---

## 🤖 SAGE-Specific AI Collaboration

### Session History

> **Generic checklist**: See `content/practices/ai_collaboration/session_checklist.md`
> **SAGE-specific**: See `.history/_session-end-checklist.md`

### Expert Committee (SAGE Context)

For SAGE-related decisions, the expert groups include:

- **Architecture** — 3-layer design, DI, EventBus
- **Knowledge Engineering** — Content organization, loading strategies
- **AI Collaboration** — Junie integration, MCP patterns
- **Engineering Practice** — Python best practices, testing

---

*Part of SAGE Knowledge Base - Project-Specific Guidelines*
