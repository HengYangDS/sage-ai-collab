---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~300
---

# MCP Protocol Reference

> SAGE Model Context Protocol (MCP) Server Documentation

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Server Configuration](#2-server-configuration)
- [3. Quick Reference](#3-quick-reference)
- [4. Detailed Documentation](#4-detailed-documentation)

---

## 1. Overview

SAGE provides an MCP server for AI agent integration. Built with FastMCP, it exposes knowledge base functionality through standardized tools and resources.

| Component   | Description                        |
|-------------|------------------------------------|
| Tools       | Knowledge retrieval and search     |
| Resources   | URI-based knowledge access         |
| Prompts     | Task-specific system prompts       |

---

## 2. Server Configuration

### 2.1 Starting the Server

```bash
# Via CLI
sage serve --host localhost --port 8000

# Via Python
python -m sage.services.mcp_server
```

### 2.2 Configuration

Located in `config/services/mcp.yaml`:

```yaml
mcp:
  host: localhost
  port: 8000
  timeout_ms: 5000
  max_connections: 10
  capabilities:
    - knowledge_retrieval
    - search
    - context_management
```

---

## 3. Quick Reference

### 3.1 Tools

| Tool                 | Purpose                     |
|----------------------|-----------------------------|
| `sage_get_knowledge` | Retrieve knowledge by layer |
| `sage_search`        | Search the knowledge base   |
| `sage_get_context`   | Get task-specific context   |
| `sage_info`          | Get system information      |

### 3.2 Resources

| Resource                   | Description              |
|----------------------------|--------------------------|
| `knowledge://core`         | Core principles          |
| `knowledge://guidelines`   | Coding guidelines        |
| `knowledge://frameworks`   | Conceptual frameworks    |
| `knowledge://practices`    | Best practices           |

### 3.3 Timeout Levels

| Level | Timeout | Use Case               |
|-------|---------|------------------------|
| T1    | 100ms   | Cache-only responses   |
| T2    | 500ms   | Single file operations |
| T3    | 2s      | Standard tool calls    |
| T4    | 5s      | Full knowledge load    |
| T5    | 10s     | Complex analysis       |

---

## 4. Detailed Documentation

| Document                                   | Content                              |
|--------------------------------------------|--------------------------------------|
| [MCP Tools Reference](mcp_tools_ref.md)    | Detailed tool schemas and examples   |
| [MCP Resources](mcp_resources.md)          | Resources, prompts, error handling   |
| [MCP Quick Reference](mcp_quick_ref.md)    | One-page quick reference             |

---

## Related

- `docs/api/index.md` — API overview
- `docs/api/cli.md` — CLI reference
- `docs/api/python.md` — Python API
- `docs/design/02-sage-protocol.md` — Protocol design

---

*Part of SAGE Knowledge Base*
