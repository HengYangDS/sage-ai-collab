# MCP Integration Scenario Context

> Pre-configured context for Model Context Protocol integration development

---

## Table of Contents

- [1. Scenario Profile](#1-scenario-profile)

- [2. Relevant Knowledge](#2-relevant-knowledge)

- [3. Project Structure](#3-project-structure)

- [4. MCP Architecture](#4-mcp-architecture)

- [5. Implementation Patterns](#5-implementation-patterns)

- [6. Common Tasks](#6-common-tasks)

- [7. Autonomy Calibration](#7-autonomy-calibration)

- [8. Quick Commands](#8-quick-commands)

---

## 1. Scenario Profile

```yaml

scenario: mcp_integration

languages: [ python, typescript, json ]

tools: [ fastmcp, mcp-sdk, uvicorn, httpx ]

focus: [ protocol, tools, resources, prompts, transport ]

autonomy_default: L3

```

---

## 2. Relevant Knowledge

| Priority      | Files                                                                                                       |

|---------------|-------------------------------------------------------------------------------------------------------------|

| **Auto-Load** | `core/principles.md` · `docs/api/mcp_quick_ref.md` · `.knowledge/practices/engineering/api_design.md`                  |

| **On-Demand** | `docs/api/mcp.md` · `.knowledge/frameworks/resilience/timeout_patterns.md` · `.knowledge/practices/engineering/error_handling.md` |

---

## 3. Project Structure

| Directory            | Purpose                   |

|----------------------|---------------------------|

| `src/sage/services/` | MCP server implementation |

| `config/services/`   | MCP configuration         |

| `tests/integration/` | MCP integration tests     |

| `docs/api/mcp.md`    | MCP API documentation     |

---

## 4. MCP Architecture

### 4.1 Protocol Overview

```

┌─────────────────┐     MCP Protocol      ┌─────────────────┐

│   AI Client     │ ◄──────────────────► │   MCP Server    │

│  (Claude, etc.) │                       │   (SAGE)        │

└─────────────────┘                       └─────────────────┘

        │                                         │

        │  Request: tools/call                    │

        │  ─────────────────────►                 │

        │                                         │

        │  Response: tool result                  │

        │  ◄─────────────────────                 │

        │                                         │

```

### 4.2 Core Components

| Component     | Purpose             | Implementation              |

|---------------|---------------------|-----------------------------|

| **Server**    | Protocol handler    | `FastMCP` or custom         |

| **Tools**     | Callable functions  | `@mcp.tool()` decorator     |

| **Resources** | Readable content    | `@mcp.resource()` decorator |

| **Prompts**   | Reusable templates  | `@mcp.prompt()` decorator   |

| **Transport** | Communication layer | stdio, SSE, WebSocket       |

### 4.3 Transport Options

| Transport     | Use Case                | Configuration            |

|---------------|-------------------------|--------------------------|

| **stdio**     | Local CLI integration   | Default for most clients |

| **SSE**       | Web-based clients       | HTTP server required     |

| **WebSocket** | Real-time bidirectional | For streaming needs      |

---

## 5. Implementation Patterns

### 5.1 Basic Server Setup

```python

from mcp.server.fastmcp import FastMCP

# Initialize server

mcp = FastMCP("knowledge-base")

@mcp.tool()

async def sage_get(layer: str = "core", topic: str | None = None) -> str:

    """Get knowledge from SAGE knowledge base.

    

    Args:

        layer: Knowledge layer (core, guidelines, frameworks, practices)

        topic: Optional topic filter

    

    Returns:

        Knowledge content as markdown

    """

    # Implementation

    return await load_knowledge(layer, topic)

@mcp.tool()

async def sage_search(query: str, limit: int = 10) -> str:

    """Search SAGE knowledge base.

    

    Args:

        query: Search query string

        limit: Maximum results to return

    

    Returns:

        Search results as formatted text

    """

    results = await search_knowledge(query, limit)

    return format_results(results)

```

### 5.2 Resource Definition

```python

@mcp.resource("sage://core/principles")

async def get_principles() -> str:

    """Core principles of SAGE knowledge base."""

    return await load_file(".knowledge/core/principles.md")

@mcp.resource("sage://layer/{layer}")

async def get_layer(layer: str) -> str:

    """Get all content from a specific layer."""

    return await load_layer(layer)

```

### 5.3 Prompt Templates

```python

@mcp.prompt()

async def code_review(code: str, language: str = "python") -> str:

    """Generate a code review prompt with SAGE guidelines.

    

    Args:

        code: Code to review

        language: Programming language

    """

    guidelines = await load_knowledge("guidelines", language)

    return f"""Review this {language} code using these guidelines:

{guidelines}

Code to review:

```{language}

{code}

```

Provide feedback on:

1. Adherence to guidelines

2. Code quality

3. Potential improvements

   """

```

### 5.4 Error Handling

```python

from mcp.server.fastmcp import FastMCP

from mcp.types import McpError, ErrorCode

@mcp.tool()

async def sage_get(layer: str) -> str:

    """Get knowledge with proper error handling."""

    try:

        if layer not in VALID_LAYERS:

            raise McpError(

                ErrorCode.INVALID_PARAMS,

                f"Invalid layer: {layer}. Valid: {VALID_LAYERS}"

            )

        

        content = await load_with_timeout(layer)

        if not content:

            raise McpError(

                ErrorCode.INTERNAL_ERROR,

                f"No content found for layer: {layer}"

            )

        

        return content

        

    except TimeoutError:

        raise McpError(

            ErrorCode.INTERNAL_ERROR,

            f"Timeout loading layer: {layer}"

        )

```

### 5.5 Timeout Integration

```python

import asyncio

from sage.core.timeout import TimeoutLevel

@mcp.tool()

async def sage_search(query: str) -> str:

    """Search with timeout protection."""

    timeout = get_timeout(TimeoutLevel.T3_LAYER)

    try:

        async with asyncio.timeout(timeout / 1000):

            results = await search_knowledge(query)

            return format_results(results)

    except asyncio.TimeoutError:

        # Return partial results or fallback

        return "Search timed out. Try a more specific query."

```

---

## 6. Common Tasks

| Task                    | Steps                                                      |

|-------------------------|------------------------------------------------------------|

| **Add new tool**        | Define function → Add decorator → Document → Test          |

| **Add resource**        | Define URI pattern → Implement loader → Register           |

| **Add prompt**          | Design template → Implement → Document arguments           |

| **Configure transport** | Choose transport → Update config → Test connection         |

| **Handle errors**       | Catch exceptions → Map to McpError → Return useful message |

| **Add rate limiting**   | Configure limits → Implement middleware → Monitor          |

### 6.1 Adding a New Tool

```python

# 1. Define the tool function

@mcp.tool()

async def my_new_tool(param1: str, param2: int = 10) -> str:

    """Tool description for AI client.

    

    Args:

        param1: Description of param1

        param2: Description of param2 (default: 10)

    

    Returns:

        Description of return value

    """

    # Implementation

    result = await process(param1, param2)

    return format_output(result)

# 2. Add tests

async def test_my_new_tool():

    result = await my_new_tool("test", 5)

    assert "expected" in result

# 3. Update documentation

# Edit docs/api/mcp.md

```

### 6.2 Testing MCP Server

```python

import pytest

from mcp.client import Client

from mcp.client.stdio import stdio_client

@pytest.mark.asyncio

async def test_mcp_server():

    """Test MCP server end-to-end."""

    async with stdio_client("sage", ["serve"]) as client:

        # Test tool call

        result = await client.call_tool("sage_get", {"layer": "core"})

        assert result.content

        # Test resource access

        resource = await client.read_resource("sage://core/principles")

        assert "principles" in resource.lower()

```

---

## 7. Autonomy Calibration

| Task Type                | Level | Notes                          |

|--------------------------|-------|--------------------------------|

| Fix tool documentation   | L5    | Low risk                       |

| Add new tool             | L3-L4 | Follow existing patterns       |

| Modify existing tool API | L2    | May break client compatibility |

| Change transport config  | L2    | Affects all clients            |

| Add authentication       | L1-L2 | Security implications          |

| Protocol version upgrade | L1    | Breaking changes possible      |

---

## 8. Quick Commands

| Category   | Commands                                                 |

|------------|----------------------------------------------------------|

| **Start**  | `sage serve` · `sage serve --port 8080`                  |

| **Test**   | `pytest tests/integration/test_mcp.py`                   |

| **Debug**  | `sage serve --debug` · `SAGE_LOG_LEVEL=DEBUG sage serve` |

| **Client** | `mcp dev sage serve` · `npx @anthropic/mcp-cli`          |

---

## Configuration Reference

### Server Configuration

```yaml

# config/services/mcp.yaml

mcp:

  server:

    name: knowledge-base

    version: "0.1.0"

    description: "AI Collaboration Knowledge Base MCP Server"

  transport:

    type: stdio  # stdio, sse, websocket

    # SSE options

    host: "0.0.0.0"

    port: 8080

  tools:

    sage_get:

      enabled: true

      timeout_level: T3

    sage_search:

      enabled: true

      timeout_level: T2

      max_results: 20

    sage_info:

      enabled: true

      timeout_level: T1

  rate_limit:

    enabled: true

    requests_per_minute: 60

    burst: 10

```

### Client Configuration

```json

{

  "mcpServers": {

    "sage": {

      "command": "sage",

      "args": [

        "serve"

      ],

      "env": {

        "SAGE_LOG_LEVEL": "INFO"

      }

    }

  }

}

```

---

## Troubleshooting

| Issue              | Cause               | Solution                      |

|--------------------|---------------------|-------------------------------|

| Connection refused | Server not running  | Start with `sage serve`       |

| Tool not found     | Tool not registered | Check `@mcp.tool()` decorator |

| Timeout errors     | Slow operations     | Increase timeout or optimize  |

| Invalid params     | Type mismatch       | Verify parameter types        |

| Auth failed        | Missing credentials | Configure authentication      |

---

## Related

- `docs/api/mcp.md` — MCP API documentation

- `.knowledge/practices/engineering/api_design.md` — API design patterns

- `.knowledge/frameworks/resilience/timeout_patterns.md` — Timeout handling

- `.knowledge/practices/engineering/error_handling.md` — Error handling

---

*AI Collaboration Knowledge Base*

