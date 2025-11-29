# MCP Protocol Reference

> SAGE Model Context Protocol (MCP) Server Documentation

---

## Overview

SAGE provides an MCP server for AI agent integration. Built with FastMCP, it exposes knowledge base functionality through standardized tools and resources.

---

## Server Configuration

### Starting the Server

```bash
# Via CLI
sage serve --host localhost --port 8000

# Via Python
python -m sage.services.mcp_server
```

### Configuration

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

## Tools

### sage_get_knowledge

Retrieve knowledge from the knowledge base.

**Input Schema:**

```json
{
  "type": "object",
  "properties": {
    "layer": {
      "type": "string",
      "enum": ["core", "guidelines", "frameworks", "practices", "all"],
      "description": "Knowledge layer to retrieve"
    },
    "topic": {
      "type": "string",
      "description": "Specific topic within the layer"
    },
    "timeout_ms": {
      "type": "integer",
      "default": 2000,
      "description": "Timeout in milliseconds"
    }
  },
  "required": ["layer"]
}
```

**Output:**

```json
{
  "content": "...",
  "metadata": {
    "layer": "core",
    "files_loaded": 3,
    "load_time_ms": 150,
    "from_cache": false
  }
}
```

**Example:**

```json
{
  "tool": "sage_get_knowledge",
  "arguments": {
    "layer": "core",
    "timeout_ms": 2000
  }
}
```

---

### sage_search

Search the knowledge base.

**Input Schema:**

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "Search query"
    },
    "limit": {
      "type": "integer",
      "default": 10,
      "description": "Maximum number of results"
    },
    "layer": {
      "type": "string",
      "enum": ["core", "guidelines", "frameworks", "practices", "all"],
      "default": "all",
      "description": "Layer to search in"
    }
  },
  "required": ["query"]
}
```

**Output:**

```json
{
  "results": [
    {
      "path": "content/core/principles.md",
      "title": "Core Principles",
      "snippet": "...matching text...",
      "score": 0.95
    }
  ],
  "total": 5,
  "query_time_ms": 45
}
```

---

### sage_get_context

Get task-specific context based on task type.

**Input Schema:**

```json
{
  "type": "object",
  "properties": {
    "task_type": {
      "type": "string",
      "enum": ["coding", "debugging", "reviewing", "planning", "documenting"],
      "description": "Type of task"
    },
    "language": {
      "type": "string",
      "default": "python",
      "description": "Programming language context"
    },
    "token_budget": {
      "type": "integer",
      "default": 4000,
      "description": "Maximum tokens for response"
    }
  },
  "required": ["task_type"]
}
```

**Output:**

```json
{
  "context": "...",
  "sections": ["principles", "guidelines", "patterns"],
  "token_count": 3500,
  "load_time_ms": 200
}
```

---

### sage_info

Get system information and status.

**Input Schema:**

```json
{
  "type": "object",
  "properties": {}
}
```

**Output:**

```json
{
  "version": "0.1.0",
  "status": "healthy",
  "knowledge_base": {
    "content_files": 45,
    "total_size_kb": 256
  },
  "cache": {
    "enabled": true,
    "hit_rate": 0.85
  },
  "uptime_seconds": 3600
}
```

---

## Resources

### knowledge://core

Core principles and philosophy.

**URI Pattern:** `knowledge://core/{topic?}`

**Examples:**
- `knowledge://core` — All core content
- `knowledge://core/principles` — Principles only
- `knowledge://core/defaults` — Default values

---

### knowledge://guidelines

Coding and collaboration guidelines.

**URI Pattern:** `knowledge://guidelines/{category?}`

**Examples:**
- `knowledge://guidelines` — All guidelines
- `knowledge://guidelines/python` — Python guidelines
- `knowledge://guidelines/ai_collaboration` — AI collaboration

---

### knowledge://frameworks

Conceptual frameworks and patterns.

**URI Pattern:** `knowledge://frameworks/{framework?}`

**Examples:**
- `knowledge://frameworks` — All frameworks
- `knowledge://frameworks/autonomy` — Autonomy levels
- `knowledge://frameworks/timeout` — Timeout patterns

---

### knowledge://practices

Best practices and engineering patterns.

**URI Pattern:** `knowledge://practices/{category?}`

**Examples:**
- `knowledge://practices` — All practices
- `knowledge://practices/engineering` — Engineering practices
- `knowledge://practices/documentation` — Documentation practices

---

## Prompts

### sage_task_prompt

Generate a task-specific system prompt.

**Arguments:**

| Argument | Type | Description |
|----------|------|-------------|
| `task_type` | string | Type of task |
| `context` | string | Additional context |

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

## Error Handling

### Error Codes

| Code | Name | Description |
|------|------|-------------|
| `TIMEOUT` | Timeout Error | Operation exceeded timeout |
| `NOT_FOUND` | Not Found | Requested resource not found |
| `INVALID_INPUT` | Invalid Input | Invalid request parameters |
| `INTERNAL` | Internal Error | Server-side error |

### Error Response Format

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

## Timeout Behavior

The MCP server respects the 5-level timeout hierarchy:

| Level | Timeout | MCP Behavior |
|-------|---------|--------------|
| T1 | 100ms | Cache-only responses |
| T2 | 500ms | Single file operations |
| T3 | 2s | Standard tool calls |
| T4 | 5s | Full knowledge load |
| T5 | 10s | Complex analysis |

**Graceful Degradation:**

When a timeout is approaching:
1. Return partial results
2. Include `complete: false` flag
3. Provide fallback content
4. Log timeout event

---

## Client Integration

### Claude Desktop

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

### Generic MCP Client

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

- [API Index](index.md) — API overview
- [CLI Reference](cli.md) — CLI documentation
- [Python API](python.md) — Python library
- `config/services/mcp.yaml` — MCP configuration
- `docs/design/02-sage-protocol.md` — Protocol design

---

*SAGE Knowledge Base - MCP Protocol Reference*
