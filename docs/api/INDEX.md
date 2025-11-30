---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~300
---

# API Reference

> SAGE Knowledge Base API Documentation

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Quick Links](#2-quick-links)
- [3. Interface Comparison](#3-interface-comparison)
- [4. Common Patterns](#4-common-patterns)

---

## 1. Overview

SAGE provides three interface layers for accessing knowledge:

| Interface  | Use Case                   | Technology    |
|------------|----------------------------|---------------|
| **CLI**    | Interactive terminal usage | Typer + Rich  |
| **MCP**    | AI agent integration       | FastMCP       |
| **Python** | Programmatic access        | Native Python |

---

## 2. Quick Links

### 2.1 Main References

| Document                            | Description                    |
|-------------------------------------|--------------------------------|
| [CLI Reference](CLI.md)             | Command-line interface         |
| [MCP Protocol](MCP.md)              | MCP server overview            |
| [Python API](PYTHON.md)             | Python library basics          |

### 2.2 MCP Detailed References

| Document                                  | Description                    |
|-------------------------------------------|--------------------------------|
| [MCP Tools Reference](MCP_TOOLS_REF.md)   | Detailed tool schemas          |
| [MCP Resources](MCP_RESOURCES.md)         | Resources, prompts, errors     |
| [MCP Quick Reference](MCP_QUICK_REF.md)   | One-page quick reference       |

### 2.3 Python Detailed References

| Document                                    | Description                  |
|---------------------------------------------|------------------------------|
| [Python Advanced](PYTHON_ADVANCED.md)       | Search, events, exceptions   |
| [Plugin API Quick Ref](PLUGIN_QUICK_REF.md) | Plugin development API       |

---

## 3. Interface Comparison

| Feature        | CLI | MCP | Python |
|----------------|-----|-----|--------|
| Interactive    | ✓   | -   | -      |
| AI Integration | -   | ✓   | ✓      |
| Streaming      | -   | ✓   | ✓      |
| Async Support  | -   | ✓   | ✓      |
| Rich Output    | ✓   | -   | -      |

---

## 4. Common Patterns

### 4.1 Loading Knowledge

All interfaces support the same knowledge loading patterns:

```
# By layer
core, guidelines, frameworks, practices

# By topic
search "timeout", search "autonomy"

# By task type
coding, debugging, reviewing, planning
```

### 4.2 Timeout Behavior

All interfaces respect the 5-level timeout hierarchy:

| Level | Timeout | Scope            |
|-------|---------|------------------|
| T1    | 100ms   | Cache lookup     |
| T2    | 500ms   | Single file      |
| T3    | 2s      | Layer load       |
| T4    | 5s      | Full KB          |
| T5    | 10s     | Complex analysis |

---

## Related

- `docs/guides/` — User guides and tutorials
- `docs/design/03-SERVICES.md` — Service layer design
- `config/services/` — Service configuration

---

*Part of SAGE Knowledge Base*
