# Directory Layout

> Canonical project structure for SAGE Knowledge Base

---

## 1. Overview

SAGE follows a consistent directory layout that reflects the three-layer architecture and supports the MECE principle.

---

## 2. Root Structure

```
sage-kb/
├── .knowledge/          # Universal knowledge (cross-project reusable)
├── .context/            # Project-specific knowledge
├── .junie/              # AI assistant configuration
├── config/              # Configuration files
├── docs/                # Documentation
├── scripts/             # Development scripts
├── src/                 # Source code
├── tests/               # Test suite
├── tools/               # Runtime tools
├── pyproject.toml       # Project metadata
├── README.md            # Project readme
├── CHANGELOG.md         # Change history
└── CONTRIBUTING.md      # Contribution guide
```

---

## 3. Source Code Structure

```
src/
└── sage/
    ├── __init__.py
    ├── core/                    # CORE LAYER
    │   ├── __init__.py
    │   ├── bootstrap/           # Application startup
    │   ├── config/              # Configuration management
    │   ├── di/                  # Dependency injection
    │   ├── events/              # Event bus
    │   ├── exceptions/          # Exception hierarchy
    │   ├── models/              # Data models
    │   └── plugins/             # Plugin system
    │
    ├── capabilities/            # CAPABILITIES LAYER
    │   ├── __init__.py
    │   ├── analyzers/           # Analysis capabilities
    │   ├── checkers/            # Validation capabilities
    │   ├── converters/          # Conversion capabilities
    │   ├── generators/          # Generation capabilities
    │   └── monitors/            # Monitoring capabilities
    │
    └── services/                # SERVICES LAYER
        ├── __init__.py
        ├── api/                 # HTTP API service
        ├── cli/                 # Command-line service
        └── mcp/                 # MCP protocol service
```

---

## 4. Tools Structure

```
tools/
├── __init__.py
├── INDEX.md
├── analyzers/               # Analysis tools
│   ├── __init__.py
│   ├── INDEX.md
│   └── knowledge_graph/
├── checkers/                # Validation tools
│   ├── __init__.py
│   ├── INDEX.md
│   ├── knowledge_validator.py
│   ├── link_checker.py
│   └── format_checker.py
├── converters/              # Conversion tools
│   ├── __init__.py
│   ├── INDEX.md
│   ├── migration_toolkit.py
│   └── format_converter.py
├── generators/              # Generation tools
│   ├── __init__.py
│   ├── INDEX.md
│   ├── index_generator.py
│   └── template_generator.py
└── monitors/                # Monitoring tools
    ├── __init__.py
    ├── INDEX.md
    ├── timeout_manager.py
    └── health_monitor.py
```

**Rules:**
- ❌ No top-level `.py` files (except `__init__.py`)
- ✅ Organized by MECE capability families

---

## 5. Scripts Structure

```
scripts/
├── README.md
├── dev/                     # Development utilities
│   ├── setup_dev.py
│   ├── new_file.py
│   └── generate_index.py
├── check/                   # Validation scripts
│   ├── check_architecture.py
│   ├── check_docs.py
│   ├── check_links.py
│   └── check_naming.py
├── hooks/                   # Git hooks
│   ├── pre_commit.py
│   ├── post_commit.py
│   └── pre_push.py
└── ci/                      # CI/CD scripts
    ├── build.py
    ├── test.py
    └── release.py
```

**Categories:**
- `dev/` — Development setup and utilities
- `check/` — Validation and verification
- `hooks/` — Git lifecycle hooks
- `ci/` — Continuous integration

---

## 6. Documentation Structure

```
docs/
├── design/                  # Design documents
│   ├── INDEX.md
│   ├── OVERVIEW.md
│   ├── philosophy/
│   ├── protocols/
│   ├── architecture/
│   ├── core_engine/
│   ├── timeout_resilience/
│   ├── services/
│   ├── capabilities/
│   ├── plugins/
│   ├── knowledge_system/
│   ├── memory_state/
│   ├── configuration/
│   └── evolution/
├── guides/                  # User guides
│   ├── INDEX.md
│   ├── GETTING_STARTED.md
│   ├── TOOLS.md
│   └── CONFIGURATION.md
└── api/                     # API documentation
    ├── INDEX.md
    └── REFERENCE.md
```

---

## 7. Knowledge Structure

### 7.1 Universal Knowledge (.knowledge/)

```
.knowledge/
├── INDEX.md
├── VERSION.md
├── core/                    # Core principles
├── frameworks/              # Reusable frameworks
├── guidelines/              # Coding guidelines
├── practices/               # Engineering practices
├── references/              # Quick references
├── scenarios/               # Use case scenarios
└── templates/               # Document templates
```

### 7.2 Project Knowledge (.context/)

```
.context/
├── INDEX.md
├── conventions/             # Project conventions
├── decisions/               # ADRs
├── intelligence/            # AI learning
├── overview/                # Project overview
└── policies/                # Runtime policies
```

---

## 8. Tests Structure

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── unit/                    # Unit tests
│   ├── core/
│   ├── capabilities/
│   └── services/
├── integration/             # Integration tests
│   ├── test_sage_protocol.py
│   └── test_services.py
└── e2e/                     # End-to-end tests
    └── test_cli.py
```

---

## 9. Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| **Directories** | `lower_snake_case` | `core_engine/` |
| **Python files** | `lower_snake_case.py` | `timeout_manager.py` |
| **Markdown files** | `UPPER_SNAKE_CASE.md` | `SAGE_PROTOCOL.md` |
| **Index files** | `INDEX.md` | Always uppercase |
| **Package init** | `__init__.py` | Standard Python |

---

## 10. File Placement Guide

| File Type | Location | Example |
|-----------|----------|---------|
| Core infrastructure | `src/sage/core/` | `di/container.py` |
| Capability impl | `src/sage/capabilities/` | `analyzers/content.py` |
| Service impl | `src/sage/services/` | `cli/service.py` |
| Runtime tool | `tools/{family}/` | `checkers/link_checker.py` |
| Dev script | `scripts/{category}/` | `check/check_docs.py` |
| Design doc | `docs/design/{area}/` | `protocols/SAGE.md` |
| User guide | `docs/guides/` | `GETTING_STARTED.md` |
| Unit test | `tests/unit/{layer}/` | `test_container.py` |

---

## Related

- `THREE_LAYER.md` — Architecture overview
- `DEPENDENCIES.md` — Dependency rules
- `.context/conventions/DIRECTORY_STRUCTURE.md` — Detailed conventions

---

*AI Collaboration Knowledge Base*
