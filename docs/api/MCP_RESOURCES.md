---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~500
---

# MCP Resources and Advanced Features

> Resources, prompts, error handling, and client integration for SAGE MCP server

---

## Table of Contents

- [1. Resources](#1-resources)
- [2. Prompts](#2-prompts)
- [3. Error Handling](#3-error-handling)
- [4. Timeout Behavior](#4-timeout-behavior)
- [5. Client Integration](#5-client-integration)

---

## 1. Resources

### 1.1 knowledge://core

Core principles and philosophy.

**URI Pattern:** `knowledge://core/{topic?}`

**Examples:**

- `knowledge://core` — All core content
- `knowledge://core/principles` — Principles only
- `knowledge://core/defaults` — Default values

### 1.2 knowledge://guidelines

Coding and collaboration guidelines.

**URI Pattern:** `knowledge://guidelines/{category?}`

**Examples:**

- `knowledge://guidelines` — All guidelines
- `knowledge://guidelines/python` — Python guidelines
- `knowledge://guidelines/ai_collaboration` — AI collaboration

### 1.3 knowledge://frameworks

Conceptual frameworks and patterns.

**URI Pattern:** `knowledge://frameworks/{framework?}`

**Examples:**

- `knowledge://frameworks` — All frameworks
- `knowledge://frameworks/autonomy` — Autonomy levels
- `knowledge://frameworks/timeout` — Timeout patterns

### 1.4 knowledge://practices

Best practices and engineering patterns.

**URI Pattern:** `knowledge://practices/{category?}`

**Examples:**

- `knowledge://practices` — All practices
- `knowledge://practices/engineering` — Engineering practices
- `knowledge://practices/documentation` — Documentation practices

---

## 2. Prompts

### 2.1 sage_task_prompt

Generate a task-specific system prompt.

**Arguments:**

| Argument    | Type   | Description        |
|-------------|--------|--------------------|
| `task_type` | string | Type of task       |
| `context`   | string | Additional context |

**Example Response:**

```
You are an AI assistant with access to the SAGE Knowledge Base.

Current task: coding
Relevant guidelines:
- Follow Python style guide
- Use type hints
- Write tests

Available knowledge layers:
- core: Core principles
- guidelines: Coding standards
- practices: Best practices
```

---

## 3. Error Handling

### 3.1 Error Codes

| Code            | Name           | Description                  |
|-----------------|----------------|------------------------------|
| `TIMEOUT`       | Timeout Error  | Operation exceeded timeout   |
| `NOT_FOUND`     | Not Found      | Requested resource not found |
| `INVALID_INPUT` | Invalid Input  | Invalid request parameters   |
| `INTERNAL`      | Internal Error | Server-side error            |

### 3.2 Error Response Format

```json
{
  "error": {
    "code": "TIMEOUT",
    "message": "Operation exceeded T3 timeout (2000ms)",
    "details": {
      "timeout_level": "T3",
      "elapsed_ms": 2150
    }
  },
  "fallback": {
    "content": "Partial content loaded before timeout...",
    "complete": false
  }
}
```

---

## 4. Timeout Behavior

The MCP server respects the 5-level timeout hierarchy:

| Level | Timeout | MCP Behavior           |
|-------|---------|------------------------|
| T1    | 100ms   | Cache-only responses   |
| T2    | 500ms   | Single file operations |
| T3    | 2s      | Standard tool calls    |
| T4    | 5s      | Full knowledge load    |
| T5    | 10s     | Complex analysis       |

**Graceful Degradation:**

When a timeout is approaching:

1. Return partial results
2. Include `complete: false` flag
3. Provide fallback content
4. Log timeout event

---

## 5. Client Integration

### 5.1 Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "sage": {
      "command": "sage",
      "args": ["serve"],
      "env": {
        "SAGE_CONFIG": "/path/to/config/sage.yaml"
      }
    }
  }
}
```

### 5.2 Generic MCP Client

```python
from mcp import Client

async with Client("localhost", 8000) as client:
    # Get knowledge
    result = await client.call_tool(
        "sage_get_knowledge",
        {"layer": "core"}
    )
    
    # Search
    results = await client.call_tool(
        "sage_search",
        {"query": "timeout", "limit": 5}
    )
```

---

## Related

- `docs/api/mcp.md` — MCP protocol overview
- `docs/api/mcp_tools_ref.md` — Tools detailed reference
- `docs/api/mcp_quick_ref.md` — Quick reference guide
- `.knowledge/frameworks/resilience/timeout_patterns.md` — Timeout patterns

---

*Part of SAGE Knowledge Base*
