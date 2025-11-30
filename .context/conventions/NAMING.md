# SAGE Naming Conventions

> Project-specific naming standards for SAGE Knowledge Base

---

## Table of Contents

- [1. Generic Python Conventions](#1-generic-python-conventions)
- [2. SAGE-Specific Patterns](#2-sage-specific-patterns)
- [3. Configuration Keys](#3-configuration-keys)
- [4. Events](#4-events)
- [5. Files & Directories](#5-files--directories)
- [6. Versioning & Milestones](#6-versioning--milestones)
- [7. Anti-Patterns](#7-anti-patterns-to-avoid)

---

## 1. Generic Python Conventions

> **Reference**: See `.knowledge/guidelines/python.md` for comprehensive Python naming conventions

**SAGE-specific principles:**

| Principle            | Description                                              |
|:---------------------|:---------------------------------------------------------|
| Clarity over brevity | Prefer `knowledge_loader` over `kb_ldr`                  |
| Domain alignment     | Use SAGE terminology (Source, Analyze, Generate, Evolve) |

**Quick reference** (from generic Python guidelines):

- Modules/packages: `snake_case`
- Classes: `PascalCase` (Protocols: `*Protocol`, Exceptions: `*Error`)
- Functions/methods: `snake_case` (private: `_snake_case`)
- Constants: `UPPER_SNAKE_CASE`

---

## 2. SAGE-Specific Patterns

### 2.1 Protocol Names

SAGE protocols follow the Source-Analyze-Generate-Evolve pattern:

```python
# Core SAGE protocols
class SourceProtocol(Protocol):
    ...  # S - Knowledge sourcing


class AnalyzeProtocol(Protocol):
    ...  # A - Processing & analysis


class GenerateProtocol(Protocol):
    ...  # G - Multi-channel output


class EvolveProtocol(Protocol):
    ...  # E - Metrics & optimization
```

### 2.2 Service Names

| Service | Class Name   | Module            |
|:--------|:-------------|:------------------|
| CLI     | `CLIService` | `services/cli.py` |
| MCP     | `MCPService` | `services/mcp.py` |
| API     | `APIService` | `services/api.py` |

### 2.3 Capability Names

| Type     | Class Pattern | Example                              |
|:---------|:--------------|:-------------------------------------|
| Analyzer | `*Analyzer`   | `CodeAnalyzer`, `ContentAnalyzer`    |
| Checker  | `*Checker`    | `HealthChecker`, `ConfigChecker`     |
| Monitor  | `*Monitor`    | `PerformanceMonitor`, `UsageMonitor` |

### 2.4 Domain Models

```python
# Knowledge domain
class KnowledgeAsset:
    ...  # Base knowledge unit


class KnowledgeLayer:
    ...  # Layer abstraction (core, frameworks, etc.)


class KnowledgeIndex:
    ...  # Index/navigation structure


# Session domain
class Session:
    ...  # User/AI session


class SessionContext:
    ...  # Session state container
```

---

## 3. Configuration Keys

### 3.1 YAML Configuration

```yaml
# Top-level sections: lowercase
sage:
  version: "0.1.0"

# Nested keys: snake_case
timeout:
  cache_lookup: 100ms
  file_read: 500ms

# Lists: plural nouns
layers:
  - name: core
  - name: frameworks

# Feature flags: is_* or enable_*
features:
  enable_caching: true
  is_debug_mode: false
```

### 3.2 Environment Variables

| Pattern                | Example                       |
|:-----------------------|:------------------------------|
| `SAGE_` prefix         | `SAGE_CONFIG_PATH`            |
| `UPPER_SNAKE_CASE`     | `SAGE_TIMEOUT_MS`             |
| Hierarchical with `__` | `SAGE__TIMEOUT__CACHE_LOOKUP` |

---

## 4. Events

### 4.1 Event Topics

Events follow the pattern: `{domain}.{action}` or `{domain}.{entity}.{action}`

```python
# Domain events
"source.started"  # Source operation started
"source.completed"  # Source operation completed
"source.failed"  # Source operation failed

# Entity events
"knowledge.layer.loaded"  # Specific layer loaded
"knowledge.asset.updated"  # Asset updated

# Lifecycle events
"system.initialized"  # System startup complete
"system.shutdown"  # System shutting down
```

### 4.2 Event Classes

```python
# Event class naming
class SourceStartedEvent:
    ...


class KnowledgeLoadedEvent:
    ...


class TimeoutOccurredEvent:
    ...
```

---

## 5. Files & Directories

### 5.1 Source Files

| Type         | Pattern             | Example              |
|:-------------|:--------------------|:---------------------|
| Module       | `snake_case.py`     | `timeout_manager.py` |
| Package init | `__init__.py`       | Always present       |
| Test file    | `test_*.py`         | `test_timeout.py`    |
| Config file  | `*.yaml` or `*.yml` | `sage.yaml`          |

### 5.2 Documentation Files

| Type       | Pattern              | Example                 | Forbidden        |
|:-----------|:---------------------|:------------------------|:-----------------|
| Markdown   | `UPPER_SNAKE_CASE.md`| `TIMEOUT_HIERARCHY.md`  | ❌ numeric prefix |
| ADR        | `ADR_NNNN_TOPIC.md`  | `ADR_0001_ARCHITECTURE.md` | ❌ hyphens     |
| Index      | `INDEX.md`           | `INDEX.md`              | ❌ lowercase     |
| Root docs  | `README.md`, etc.    | `CHANGELOG.md`          | —                |

**Naming Rules:**
- ✅ Use `UPPER_SNAKE_CASE` for all Markdown files
- ✅ Use lowercase `.md` extension (not `.MD`)
- ❌ No numeric prefixes (e.g., `01-`, `02-`)
- ❌ No kebab-case (e.g., `timeout-hierarchy.md`)

### 5.3 Directory Structure

| Directory   | Purpose         | Naming         |
|:------------|:----------------|:---------------|
| `src/sage/` | Source code     | Package name   |
| `tests/`    | Test suite      | Mirrors source |
| `docs/`     | Documentation   | Categorical    |
| `config/`   | Configuration   | By function    |
| `.context/` | Project context | By type        |

---

## 6. Versioning & Milestones

### 6.1 Project Version

The project version follows [Semantic Versioning](https://semver.org/):

| Component | Format   | Example | Meaning             |
|:----------|:---------|:--------|:--------------------|
| Version   | `X.Y.Z`  | `0.1.0` | MAJOR.MINOR.PATCH   |
| Pre-alpha | `0.x.y`  | `0.1.0` | Initial development |
| Alpha     | `0.x.y`  | `0.5.0` | Feature incomplete  |
| Beta      | `0.x.y`  | `0.9.0` | Feature complete    |
| Release   | `1.0.0`+ | `1.0.0` | Production ready    |

**Source of Truth**: `pyproject.toml` → `[project].version`

### 6.2 Milestone Naming

Internal development milestones use **M-prefix** format to avoid confusion with release versions:

| Milestone | Format | Description            | Example Reference |
|:----------|:-------|:-----------------------|:------------------|
| MVP       | `M1`   | Minimum Viable Product | "M1 complete"     |
| Phase 2   | `M2`   | Second major milestone | "M2 in progress"  |
| Phase 3   | `M3`   | Third major milestone  | "M3 planned"      |
| Phase N   | `MN`   | Nth milestone          | "M4 future"       |

**Why M-prefix?**

- ❌ `v1.0`, `v1.1`, `v1.2` — Confuses with release versions
- ✅ `M1`, `M2`, `M3` — Clearly internal milestones

### 6.3 Version References in Documentation

| Context             | Format               | Example                     |
|:--------------------|:---------------------|:----------------------------|
| Code/config version | `"X.Y.Z"`            | `version: "0.1.0"`          |
| Milestone reference | `MN`                 | "Completed in M2"           |
| Roadmap phases      | `MN` or `Phase N`    | "M3 Phases:", "Phase I:"    |
| Future features     | `MN+`                | "Available in M2+"          |
| External tool ver.  | Keep original format | `rev: v1.11.0` (pre-commit) |

**Important**: External tool versions (e.g., pre-commit hooks, dependencies) should retain their original version
format.

---

## 7. Anti-Patterns to Avoid

| Avoid                          | Prefer           | Reason                |
|:-------------------------------|:-----------------|:----------------------|
| `kb` abbreviation              | `knowledge_base` | Clarity               |
| `mgr` suffix                   | `manager`        | Full word             |
| `Impl` suffix                  | Descriptive name | Implementation detail |
| Hungarian notation             | Type hints       | Python convention     |
| `get_*` for properties         | `@property`      | Pythonic              |
| Generic names (`data`, `info`) | Specific names   | Self-documenting      |

---

## Related

- `.junie/guidelines.md` — General coding guidelines
- `.knowledge/practices/engineering/` — Engineering practices
- `docs/design/architecture/INDEX.md` — Architecture patterns
- `.context/conventions/DOC_TEMPLATE.md` — Document template

---

*AI Collaboration Knowledge Base*
