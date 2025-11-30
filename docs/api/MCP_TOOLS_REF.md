---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~600
---

# MCP Tools Reference

> Detailed reference for SAGE MCP server tools

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. sage_get_knowledge](#2-sage_get_knowledge)
- [3. sage_search](#3-sage_search)
- [4. sage_get_context](#4-sage_get_context)
- [5. sage_info](#5-sage_info)

---

## 1. Overview

SAGE MCP server exposes four primary tools for knowledge retrieval and system information.

| Tool                 | Purpose                          |
|----------------------|----------------------------------|
| `sage_get_knowledge` | Retrieve knowledge by layer      |
| `sage_search`        | Search the knowledge base        |
| `sage_get_context`   | Get task-specific context        |
| `sage_info`          | Get system information           |

---

## 2. sage_get_knowledge

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

## 3. sage_search

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
      "path": ".knowledge/core/principles.md",
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

## 4. sage_get_context

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

## 5. sage_info

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

## Related

- `docs/api/mcp.md` — MCP protocol overview
- `docs/api/mcp_resources.md` — MCP resources and prompts
- `docs/api/mcp_quick_ref.md` — Quick reference guide

---

*Part of SAGE Knowledge Base*
