
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
| [CLI Reference](cli.md)             | Command-line interface         |
| [MCP Protocol](mcp.md)              | MCP server overview            |
| [Python API](python.md)             | Python library basics          |

### 2.2 MCP Detailed References

> **Scope**: These documents cover SAGE as an **MCP server**.
> For Junie **MCP client configuration**, see `.junie/docs/mcp/`.

| Document                                  | Description                    |
|-------------------------------------------|--------------------------------|
| [MCP Tools Reference](mcp_tools_ref.md)   | Detailed tool schemas          |
| [MCP Resources](mcp_resources.md)         | Resources, prompts, errors     |
| [MCP Quick Reference](mcp_quick_ref.md)   | One-page quick reference       |

### 2.3 Python Detailed References

| Document                                    | Description                  |
|---------------------------------------------|------------------------------|
| [Python Advanced](python_advanced.md)       | Search, events, exceptions   |
| [Plugin API Quick Ref](plugin_quick_ref.md) | Plugin development API       |

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

All interfaces respect the 5-level timeout hierarchy (T1-T5).

> **See**: `.context/policies/TIMEOUT_HIERARCHY.md` for authoritative timeout values and fallback strategies.

---

## Related

- `docs/guides/` — User guides and tutorials
- `docs/design/03-services.md` — Service layer design
- `config/services/` — Service configuration

---

*AI Collaboration Knowledge Base*
