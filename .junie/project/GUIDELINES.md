# SAGE Project - AI Collaboration Guidelines

> Project-specific AI collaboration rules and quick reference for SAGE Knowledge Base

---

## Table of Contents

- [1. Project Overview](#1-project-overview)
- [2. Tech Stack](#2-tech-stack)
- [3. Project Structure](#3-project-structure)
- [4. Key Behaviors](#4-key-behaviors)
- [5. Coding Standards](#5-coding-standards)
- [6. Session Management](#6-session-management)
- [7. Expert Committee](#7-expert-committee)
- [8. Quick Commands](#8-quick-commands)
- [9. Key Paths](#9-key-paths)
- [10. Timeout Hierarchy](#10-timeout-hierarchy)
- [11. References](#11-references)

---

## 1. Project Overview

**SAGE Knowledge Base (sage-kb)** is a production-grade knowledge management system designed for
AI-human collaboration. It provides structured knowledge via CLI, MCP, and API services with built-in timeout protection
and smart loading.

### 1.1 Design Philosophy

**信达雅 (Xin-Da-Ya)**:

- **信 (Xin/Faithfulness)**: Accurate, reliable, testable
- **达 (Da/Clarity)**: Clear, maintainable, structured
- **雅 (Ya/Elegance)**: Refined, balanced, sustainable

---

## 2. Tech Stack

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

## 3. Project Structure

```
sage-kb/
├── .junie/          # JetBrains Junie configuration (this directory)
├── .context/        # Project-specific knowledge base
├── .history/        # AI session history and handoffs
├── .outputs/        # Intermediate process files (git-ignored)
├── config/          # Runtime configuration (modular YAML)
├── docs/            # User-facing documentation
├── .knowledge/      # Generic knowledge (distributable)
├── src/sage/        # Source code (3-layer architecture)
├── tools/           # Development tools
└── tests/           # Test suite
```

### 3.1 Key Directories

| Directory     | Purpose                                        | Visibility |
|---------------|------------------------------------------------|------------|
| `.junie/`     | AI client config for JetBrains Junie           | Hidden     |
| `.context/`   | Project-specific knowledge (ADRs, conventions) | Hidden     |
| `.history/`   | AI session records and task handoffs           | Hidden     |
| `.outputs/`   | Intermediate process files                     | Hidden     |
| `config/`     | Runtime configuration (modular YAML structure) | Visible    |
| `docs/`       | User-facing documentation                      | Visible    |
| `.knowledge/` | Generic, distributable knowledge               | Visible    |

---

## 4. Key Behaviors

SAGE project-specific behaviors for AI collaboration:

| Behavior | Description |
|:---------|:------------|
| Follow existing patterns | Maintain consistency with SAGE 3-layer architecture |
| Run tests | Execute `pytest` before committing changes |
| Update documentation | Modify `docs/` when changing features |
| Output directory | Use `.outputs/` for intermediate files |
| Session records | Create records in `.history/` for significant work |
| Language | Use English for code and documentation |
| Timeout limits | Respect T1-T5 hierarchy (see `.context/policies/TIMEOUT_HIERARCHY.md`) |

---

## 5. Coding Standards

> **Full Reference**: `.knowledge/guidelines/CODE_STYLE.md`, `.knowledge/guidelines/PYTHON.md`

### 5.1 Quick Summary

| Aspect | Standard |
|:-------|:---------|
| Formatter | Ruff (line-length: 88) |
| Type Hints | Required for all functions |
| Docstrings | Google style |
| Files | `snake_case.py` |
| Classes | `PascalCase` |
| Constants | `UPPER_SNAKE_CASE` |
| Architecture | Core → Services → Capabilities |
| Naming | See `.context/conventions/NAMING.md` |
| Patterns | See `.context/conventions/CODE_PATTERNS.md` |

### 5.2 Architecture Layers

```
src/sage/
├── core/         # Foundation layer (loader, timeout, config)
├── services/     # Service layer (CLI, MCP, API)
└── capabilities/ # Capability layer (analyzers, monitors)
```

---

## 6. Session Management

### 6.1 Session History

At session end, create records in `.history/`:

| Directory | Purpose | Naming Pattern |
|:----------|:--------|:---------------|
| `conversations/` | Key decisions and outcomes | `YYYYMMDD-TOPIC.md` |
| `handoffs/` | Task continuation context | `YYYYMMDD-TASK-HANDOFF.md` |
| `current/` | Active work state | `current-state.md` |

### 6.2 Record Content

**Conversation Records** should include:
- Session date and duration
- Key decisions made
- Important outcomes
- Unresolved issues

**Handoff Records** should include:
- Task status and progress
- Next steps
- Blocking issues
- Context for continuation

### 6.3 Session Automation

Use MCP tools for session management:

| Tool | When | Purpose |
|:-----|:-----|:--------|
| `session_start` | Beginning of significant work | Creates session state |
| `session_end` | Work completed/ending | Creates record |
| `session_status` | Start of new session | Check state |

---

## 7. Expert Committee

For complex SAGE decisions, simulate **Level 5 Expert Committee** review:

| Expert Group | Focus Areas |
|:-------------|:------------|
| **Architecture** | 3-layer design, DI, EventBus, scalability |
| **Knowledge Engineering** | Content organization, loading strategies |
| **AI Collaboration** | Junie integration, MCP patterns |
| **Engineering Practice** | Python best practices, testing |

### 7.1 When to Use

- Architecture changes affecting multiple layers
- New capability or plugin design
- Knowledge base reorganization
- Performance optimization decisions

---

## 8. Quick Commands

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

## 9. Key Paths

| Category        | Path                     | Purpose                     |
|-----------------|--------------------------|-----------------------------|
| **Conventions** | `.context/conventions/`  | Naming, patterns, structure |
| **Policies**    | `.context/policies/`     | Timeouts, loading, runtime  |
| **ADRs**        | `.context/decisions/`    | Architecture decisions      |
| **AI Patterns** | `.context/intelligence/` | Interaction patterns        |
| **Config**      | `config/sage.yaml`       | Main configuration          |
| **Core Code**   | `src/sage/core/`         | Core layer                  |
| **Services**    | `src/sage/services/`     | CLI, MCP, API               |

---

## 10. Timeout Hierarchy

> **Reference**: See `.context/policies/TIMEOUT_HIERARCHY.md` for full details

**SAGE-specific timeout configuration**:

| Tier | Duration | SAGE Use Case    |
|------|----------|------------------|
| T1   | 100ms    | Cache lookup     |
| T2   | 500ms    | Single file read |
| T3   | 2s       | Layer load       |
| T4   | 5s       | Full KB load     |
| T5   | 10s      | Complex analysis |

---

## 11. References

### 11.1 Project-Specific

| Topic | Location |
|:------|:---------|
| Timeout Hierarchy | `.context/policies/TIMEOUT_HIERARCHY.md` |
| Code Patterns | `.context/conventions/CODE_PATTERNS.md` |
| Naming Conventions | `.context/conventions/NAMING.md` |
| Project Calibration | `.context/intelligence/calibration/CALIBRATION.md` |
| Session Checklist | `.history/_SESSION-END-CHECKLIST.md` |
| Project Variables | `config.yaml` |
| Design Documents | `docs/design/OVERVIEW.md` |

### 11.2 Generic Knowledge

| Topic | Location |
|:------|:---------|
| Code Style | `.knowledge/guidelines/CODE_STYLE.md` |
| Python Guidelines | `.knowledge/guidelines/PYTHON.md` |
| AI Collaboration | `.knowledge/guidelines/AI_COLLABORATION.md` |
| Autonomy Levels | `.knowledge/frameworks/autonomy/LEVELS.md` |
| Documentation Standards | `.knowledge/guidelines/DOCUMENTATION.md` |

---

## Related

- [Junie Guidelines](../guidelines.md) — Core Junie AI rules
- [Quick Reference](../generic/QUICKREF.md) — Quick lookup card
- [Project Config](config.yaml) — Project identity and settings
- [Timeout Hierarchy](../../.context/policies/TIMEOUT_HIERARCHY.md) — Project timeout configuration
- [Autonomy Calibration](../../.context/intelligence/calibration/CALIBRATION.md) — Project calibration data

---

*AI Collaboration Knowledge Base*
