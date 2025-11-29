# API Reference

> SAGE Knowledge Base API Documentation

---

## Overview

SAGE provides three interface layers for accessing knowledge:

| Interface | Use Case | Technology |
|-----------|----------|------------|
| **CLI** | Interactive terminal usage | Typer + Rich |
| **MCP** | AI agent integration | FastMCP |
| **Python** | Programmatic access | Native Python |

---

## Quick Links

- [CLI Reference](cli.md) — Command-line interface commands
- [MCP Protocol](mcp.md) — MCP server tools and resources
- [Python API](python.md) — Python library usage

---

## Interface Comparison

| Feature | CLI | MCP | Python |
|---------|-----|-----|--------|
| Interactive | ✓ | - | - |
| AI Integration | - | ✓ | ✓ |
| Streaming | - | ✓ | ✓ |
| Async Support | - | ✓ | ✓ |
| Rich Output | ✓ | - | - |

---

## Common Patterns

### Loading Knowledge

All interfaces support the same knowledge loading patterns:

```
# By layer
core, guidelines, frameworks, practices

# By topic
search "timeout", search "autonomy"

# By task type
coding, debugging, reviewing, planning
```

### Timeout Behavior

All interfaces respect the 5-level timeout hierarchy:

| Level | Timeout | Scope |
|-------|---------|-------|
| T1 | 100ms | Cache lookup |
| T2 | 500ms | Single file |
| T3 | 2s | Layer load |
| T4 | 5s | Full KB |
| T5 | 10s | Complex analysis |

---

## Related

- `docs/guides/` — User guides and tutorials
- `docs/design/03-services.md` — Service layer design
- `config/services/` — Service configuration

---

*SAGE Knowledge Base - API Reference*
