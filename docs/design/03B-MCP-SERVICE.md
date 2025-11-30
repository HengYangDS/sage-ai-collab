---
title: SAGE Knowledge Base - MCP Service Design
version: "0.1.0"
last_updated: "2025-11-30"
status: production-ready
tokens: ~900
---

# MCP Service Design

> **Model Context Protocol server with FastMCP**

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Implementation](#2-implementation)
- [3. Tools Reference](#3-tools-reference)
- [4. Prompt Templates](#4-prompt-templates)

---

## 1. Overview

The MCP Service provides AI assistant integration via Model Context Protocol.

| Feature            | Technology | Description                      |
|--------------------|------------|----------------------------------|
| Protocol           | MCP        | Standard AI tool interface       |
| Framework          | FastMCP    | High-performance MCP server      |
| Timeout protection | Built-in   | All operations have timeouts     |
| Response format    | Structured | Consistent JSON responses        |

---

## 2. Implementation

```python
# src/sage/services/mcp_server.py
"""
MCP Service - Model Context Protocol server.
"""
from mcp.server.fastmcp import FastMCP
import asyncio
import time

from sage.core.di import get_container
from sage.core.protocols import SourceProtocol, AnalyzeProtocol
from sage.core.models import SourceRequest

mcp = FastMCP("sage")


@mcp.tool()
async def get_knowledge(
    layer: int = 0,
    task: str = "",
    timeout_ms: int = 5000
) -> dict:
    """
    Get AI collaboration knowledge with timeout guarantee.
    
    Args:
        layer: Knowledge layer (0=core, 1=guidelines, 2=frameworks, 3=practices)
        task: Task description for smart loading
        timeout_ms: Maximum time in milliseconds (default: 5000)
    
    Returns:
        dict with content, tokens, status, duration_ms
    """
    start = time.time()
    layer_names = ["core", "guidelines", "frameworks", "practices"]
    layer_name = layer_names[min(layer, len(layer_names) - 1)]

    container = get_container()
    loader = container.resolve(SourceProtocol)

    try:
        result = await asyncio.wait_for(
            loader.source(SourceRequest(
                layers=[layer_name],
                query=task,
                timeout_ms=timeout_ms
            )),
            timeout=timeout_ms / 1000
        )
        status = result.status
    except asyncio.TimeoutError:
        result = await loader.get_fallback()
        status = "timeout_fallback"

    return {
        "content": result.content,
        "tokens": result.tokens,
        "status": status,
        "duration_ms": int((time.time() - start) * 1000),
        "layer": layer_name,
    }


@mcp.tool()
async def search_knowledge(
    query: str,
    max_results: int = 5,
    timeout_ms: int = 3000
) -> list:
    """
    Search knowledge base with timeout.
    
    Args:
        query: Search query string
        max_results: Maximum number of results (default: 5)
        timeout_ms: Maximum time in milliseconds (default: 3000)
    """
    container = get_container()
    analyzer = container.resolve(AnalyzeProtocol)

    try:
        results = await asyncio.wait_for(
            analyzer.search(query, max_results),
            timeout=timeout_ms / 1000
        )
        return [
            {"path": r.path, "score": r.score, "preview": r.preview, "layer": r.layer}
            for r in results
        ]
    except asyncio.TimeoutError:
        return []


@mcp.tool()
async def get_framework(name: str, timeout_ms: int = 5000) -> dict:
    """Get framework documentation."""
    container = get_container()
    loader = container.resolve(SourceProtocol)

    result = await loader.source(SourceRequest(
        layers=["frameworks"],
        query=name,
        timeout_ms=timeout_ms
    ))

    return {"content": result.content, "framework": name, "status": result.status}


@mcp.tool()
async def kb_info() -> dict:
    """Get knowledge base information."""
    return {
        "version": "0.1.0",
        "layers": {
            "core": {"tokens": 500, "always_load": True},
            "guidelines": {"tokens": 1200, "always_load": False},
            "frameworks": {"tokens": 2000, "always_load": False},
            "practices": {"tokens": 1500, "always_load": False},
        },
        "timeout_levels": ["T1:100ms", "T2:500ms", "T3:2s", "T4:5s", "T5:10s"],
    }


async def run_mcp_server(host: str = "localhost", port: int = 8000):
    """Run the MCP server."""
    await mcp.run()
```

---

## 3. Tools Reference

| Tool               | Description            | Parameters                           |
|--------------------|------------------------|--------------------------------------|
| `get_knowledge`    | Get knowledge by layer | `layer`, `task`, `timeout_ms`        |
| `search_knowledge` | Search knowledge base  | `query`, `max_results`, `timeout_ms` |
| `get_framework`    | Get framework docs     | `name`, `timeout_ms`                 |
| `kb_info`          | Get KB information     | (none)                               |

### Layer Mapping

| Layer Value | Layer Name   | Token Budget | Always Load |
|-------------|--------------|--------------|-------------|
| 0           | core         | ~500         | Yes         |
| 1           | guidelines   | ~1200        | No          |
| 2           | frameworks   | ~2000        | No          |
| 3           | practices    | ~1500        | No          |

---

## 4. Prompt Templates

### Recommended Prompts

| Tool               | Recommended Prompt                                       |
|--------------------|----------------------------------------------------------|
| `get_knowledge`    | "Load [layer] knowledge for [task description]"          |
| `search_knowledge` | "Search KB for [topic] to find [what you need]"          |
| `get_framework`    | "Get the [autonomy/timeout] framework for [decision]"    |
| `kb_info`          | "Show KB structure and available layers"                 |

### Example Usage

```python
# Starting a new coding task
get_knowledge(layer=1, task="implement user authentication")

# Need guidance on decision-making
get_framework(name="autonomy")

# Looking for specific information
search_knowledge(query="timeout configuration", max_results=5)

# Understanding available resources
kb_info()
```

### Best Practices

| Practice         | Description                                          |
|------------------|------------------------------------------------------|
| Be specific      | Include task context in the `task` parameter         |
| Layer selection  | Start with `layer=0` (core) for general guidance     |
| Search first     | Use `search_knowledge` when unsure which layer       |
| Combine tools    | Use `kb_info` → `search` → `get_knowledge` workflow  |

---

## Related

- `docs/design/03-services.md` — Services overview
- `docs/design/03a-cli-service.md` — CLI service design
- `docs/design/03c-api-service.md` — HTTP API design
- `docs/api/mcp.md` — MCP API reference

---

*Part of SAGE Knowledge Base*
