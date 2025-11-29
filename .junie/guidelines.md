# SAGE Knowledge Base - Project Guidelines

> **Purpose**: Primary entry point for JetBrains Junie AI collaboration.
> **Last Updated**: 2025-11-30
> **Version**: 0.1.0
> **Status**: Alpha - Under active development and testing
> **Compatibility**: Junie v2024.3+, MCP v1.0+
> **Schema Version**: 1.0

---

<!-- ========================================================================
     TEMPLATE USAGE NOTES
     
     This file follows a template structure for cross-project reusability.
     
     📌 PROJECT-SPECIFIC sections: Must be customized per project
     🔄 GENERIC sections: Can be reused across projects with minimal changes
     
     Project variables are centralized in: project.yaml
     ======================================================================== -->

## 📋 Project Overview

<!-- 📌 PROJECT-SPECIFIC: Customize for your project -->
<!-- Reference: project.yaml → project.name, project.description -->

**SAGE Knowledge Base (sage-kb)** is a production-grade knowledge management system designed for
AI-human collaboration. It provides structured knowledge via CLI, MCP, and API services with built-in timeout protection
and smart loading.

### Design Philosophy

<!-- 📌 PROJECT-SPECIFIC: Your project's guiding principles -->
<!-- Reference: project.yaml → project.philosophy -->

- **信 (Xin/Faithfulness)**: Accurate, reliable, testable
- **达 (Da/Clarity)**: Clear, maintainable, structured
- **雅 (Ya/Elegance)**: Refined, balanced, sustainable

---

## 🛠️ Tech Stack

<!-- 📌 PROJECT-SPECIFIC: Your project's technology choices -->
<!-- Reference: project.yaml → tech_stack -->

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

<!-- 📌 PROJECT-SPECIFIC: Your project's directory layout -->
<!-- Reference: project.yaml → directories -->

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

### Key Directories Explained

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

<!-- 🔄 GENERIC: Structure is reusable; update references per project -->

> **Reference**: See `content/guidelines/python.md` and `.context/conventions/naming.md` for full details

**Quick Summary:**
- **Formatter**: Ruff (line-length: 88) | **Type Hints**: Required | **Docstrings**: Google style
- **Naming**: Files `snake_case.py`, Classes `PascalCase`, Constants `UPPER_SNAKE_CASE`
- **Architecture**: Core → Services → Capabilities (see `.context/conventions/code_patterns.md`)

---

## 📝 Documentation Standards

<!-- 🔄 GENERIC: Reference pattern is reusable -->

> **Reference**: See `content/practices/documentation/DOCUMENTATION_STANDARDS.md` for full SSOT (format rules, knowledge placement, index maintenance)

---

## 📄 Important Files

<!-- 📌 PROJECT-SPECIFIC: Your project's key files -->
<!-- Reference: project.yaml → key_files -->

| File                 | Purpose                                          |
|----------------------|--------------------------------------------------|
| `config/sage.yaml`   | Main configuration (timeouts, triggers, loading) |
| `docs/design/`       | Design documents (architecture, services, etc.)  |
| `src/sage/core/`     | Core layer (loader, timeout, config)             |
| `src/sage/services/` | Service layer (CLI, MCP, API)                    |
| `pyproject.toml`     | Python project configuration                     |
| `index.md`           | Knowledge base navigation entry                  |

---

## 🤖 AI Collaboration Rules

<!-- 🔄 GENERIC: This entire section is reusable across projects -->

### Autonomy Levels

> **Reference**: See `content/frameworks/autonomy/levels.md` for full 6-level autonomy framework

| Level | Name                        | Description           | Example Tasks                                        |
|-------|-----------------------------|-----------------------|------------------------------------------------------|
| L1-L2 | Minimal/Low (0-40%)         | Ask before changes    | Breaking changes, new dependencies, critical systems |
| L3-L4 | Medium/Medium-High (40-80%) | Proceed, report after | Bug fixes, refactoring, routine development ⭐        |
| L5-L6 | High/Full (80-100%)         | High autonomy         | Formatting, comments, docs, trusted patterns         |

**Default**: L4 (Medium-High) for mature collaboration.

### Key Behaviors

<!-- 🔄 GENERIC: These behaviors apply to any project -->

1. **Always respect timeout limits** (T1:100ms → T5:10s)
2. **Use English** for code and documentation
3. **Follow existing patterns** in the codebase
4. **Run tests** before committing changes
5. **Update relevant documentation** when modifying features
6. **Output files to `.outputs/`** — All temporary/intermediate files must go to `.outputs/`, never project root
7. **Create session records** for significant work sessions (see Session History below)

### Session History Management

<!-- 🔄 GENERIC: Pattern is reusable; directory names may vary -->

> **Reference**: See `content/practices/ai_collaboration/session_checklist.md` for generic checklist
> **Project-specific**: See `.history/_session-end-checklist.md` for SAGE-specific additions

At session end, create records in `.history/`: **conversations/** (decisions), **handoffs/** (continuation), **current/** (active work).
Templates available in `content/templates/` (conversation_record, task_handoff, session_state).

### Expert Committee Pattern

<!-- 🔄 GENERIC: Reusable cognitive framework -->

> **Reference**: See `content/frameworks/cognitive/expert_committee.md` for full methodology

For complex decisions, simulate a **Level 5 Expert Committee** review with 4 groups (Architecture, Knowledge Engineering, AI Collaboration, Engineering Practice).

---

## ⏱️ Timeout Hierarchy

<!-- 🔄 GENERIC: Timeout concept is reusable; values may vary -->

> **Reference**: See `.context/policies/timeout_hierarchy.md` for full details and implementation guidelines

**Quick Reference**: T1:100ms (cache) → T2:500ms (file) → T3:2s (layer) → T4:5s (full KB) → T5:10s (analysis)

---

## 🔗 References

<!-- 📌 PROJECT-SPECIFIC: Update paths per project -->

- **Project Variables**: @file:project.yaml
- **Design Documents**: @file:docs/design/00-overview.md
- **Documentation Standards**: @file:content/practices/documentation/DOCUMENTATION_STANDARDS.md
- **Documentation Index**: @file:docs/index.md
- **Configuration**: @file:config/sage.yaml
- **Project Context**: @file:.context/index.md
- **Knowledge Content**: @file:content/index.md
- **Directory Conventions**: @file:content/practices/documentation/project_directory_structure.md
- **Timeout Hierarchy**: @file:.context/policies/timeout_hierarchy.md
- **Core Principles**: @file:content/core/principles.md

---

## 📝 Quick Commands

<!-- 📌 PROJECT-SPECIFIC: Your project's commands -->
<!-- Reference: project.yaml → commands -->

```bash
# Run tests
pytest tests/ -v

# Start MCP server
sage serve

# CLI usage
sage get --layer core
sage search "timeout"
sage info
```

---

## 📋 Template Information

<!-- 🔄 GENERIC: Template metadata -->

This `.junie/` configuration follows the **薄层 (Thin Layer)** principle:

- **Entry Point**: `guidelines.md` (this file)
- **Project Variables**: `project.yaml` — centralized project-specific values
- **AI Configuration**: `config.yaml` — Junie-specific settings
- **Quick Reference**: `quickref.md` — instant lookup card
- **MCP Configuration**: `mcp/mcp.json` — MCP server settings

**Reusability**: Sections marked with 🔄 GENERIC can be copied to new projects with minimal changes.
Sections marked with 📌 PROJECT-SPECIFIC should be customized using values from `project.yaml`.

---

*This guideline follows the SAGE design philosophy: 信达雅 (Xin-Da-Ya)*
