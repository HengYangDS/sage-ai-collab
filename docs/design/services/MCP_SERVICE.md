# MCP Service

> Model Context Protocol service for AI assistant integration

---

## 1. Overview

The MCP service enables AI assistants (Claude, Cursor, etc.) to access SAGE knowledge base through the Model Context Protocol using FastMCP framework.

---

## 2. Technology Stack

| Component | Library | Purpose |
|-----------|---------|---------|
| **MCP Framework** | FastMCP | Protocol implementation |
| **Transport** | stdio/SSE | Communication channels |
| **Serialization** | JSON | Data exchange format |
| **Validation** | Pydantic | Input/output validation |

---

## 3. Tools

### 3.1 Tool Registry

| Tool | Description | Input | Output |
|------|-------------|-------|--------|
| `get_knowledge` | Get knowledge content | query, layer | content, metadata |
| `search_knowledge` | Search knowledge base | query, options | results |
| `get_framework` | Get framework content | name, layer | content |
| `kb_info` | Get system information | — | status, stats |

### 3.2 Tool Definitions

```python
@mcp.tool()
def get_knowledge(
    query: str,
    layer: int | None = None,
    content_type: str | None = None
) -> KnowledgeResult:
    """
    Get knowledge content from SAGE knowledge base.
    
    Args:
        query: Search query or content path
        layer: Knowledge layer (1-4)
        content_type: Filter by content type
    
    Returns:
        Knowledge content with metadata
    """
    ...

@mcp.tool()
def search_knowledge(
    query: str,
    max_results: int = 10,
    fuzzy: bool = False
) -> list[SearchResult]:
    """
    Search the knowledge base.
    
    Args:
        query: Search query
        max_results: Maximum results to return
        fuzzy: Enable fuzzy matching
    
    Returns:
        List of matching results
    """
    ...
```

---

## 4. Implementation

### 4.1 Server Setup

```python
from fastmcp import FastMCP

mcp = FastMCP(
    name="sage-kb",
    version="1.0.0",
    description="SAGE Knowledge Base MCP Server"
)

@mcp.tool()
def get_knowledge(query: str, layer: int = None) -> dict:
    container = get_container()
    loader = container.resolve(SourceProtocol)
    
    result = loader.source(KnowledgeRequest(
        query=query,
        layer=layer
    ))
    
    return {
        "content": result.content,
        "layer": result.layer,
        "type": result.content_type,
        "tokens": result.token_count
    }

if __name__ == "__main__":
    mcp.run()
```

### 4.2 Resources

```python
@mcp.resource("knowledge://{path}")
def get_resource(path: str) -> Resource:
    """Expose knowledge files as MCP resources."""
    content = loader.load_file(path)
    return Resource(
        uri=f"knowledge://{path}",
        name=path,
        mimeType="text/markdown",
        text=content
    )
```

### 4.3 Prompts

```python
@mcp.prompt()
def knowledge_query(topic: str) -> list[Message]:
    """Generate a knowledge query prompt."""
    return [
        Message(
            role="user",
            content=f"Find information about: {topic}"
        )
    ]
```

---

## 5. Transport Configuration

### 5.1 stdio Transport

```json
{
  "mcpServers": {
    "sage-kb": {
      "command": "sage",
      "args": ["serve", "--mcp"],
      "env": {
        "SAGE_CONFIG": "/path/to/config.yaml"
      }
    }
  }
}
```

### 5.2 SSE Transport

```json
{
  "mcpServers": {
    "sage-kb": {
      "url": "http://localhost:8080/mcp/sse",
      "transport": "sse"
    }
  }
}
```

---

## 6. Error Handling

### 6.1 MCP Error Format

```python
from fastmcp import McpError

@mcp.tool()
def get_knowledge(query: str) -> dict:
    try:
        result = loader.source(request)
        return result.to_dict()
    except TimeoutError:
        raise McpError(
            code="SAGE-1001",
            message="Operation timed out",
            data={"timeout_ms": 5000}
        )
    except NotFoundError:
        raise McpError(
            code="SAGE-1002", 
            message=f"Content not found: {query}"
        )
```

### 6.2 Error Codes

| Code | Description | Recovery |
|------|-------------|----------|
| SAGE-1001 | Timeout | Retry with longer timeout |
| SAGE-1002 | Not found | Check query |
| SAGE-1003 | Invalid layer | Use 1-4 |
| SAGE-3001 | MCP protocol error | Check client |

---

## 7. Timeout Integration

### 7.1 Per-Tool Timeout

```python
@mcp.tool()
def get_knowledge(query: str, timeout_ms: int = 5000) -> dict:
    with timeout_context(timeout_ms):
        result = loader.source(request)
        return result.to_dict()
```

### 7.2 Graceful Degradation

```python
@mcp.tool()
def get_knowledge(query: str) -> dict:
    try:
        return loader.source_full(request)
    except TimeoutError:
        # Return cached or partial content
        return loader.source_cached(request)
```

---

## 8. Configuration

```yaml
services:
  mcp:
    transport: stdio
    timeout_ms: 5000
    max_results: 100
    enable_resources: true
    enable_prompts: true
    log_level: info
```

---

## 9. Testing

### 9.1 Tool Testing

```python
import pytest
from sage.services.mcp import mcp

def test_get_knowledge():
    result = mcp.call_tool("get_knowledge", {
        "query": "test",
        "layer": 1
    })
    assert "content" in result
    assert result["layer"] == 1

def test_search_knowledge():
    results = mcp.call_tool("search_knowledge", {
        "query": "architecture",
        "max_results": 5
    })
    assert len(results) <= 5
```

---

## Related

- `SERVICE_LAYER.md` — Service layer overview
- `CLI_SERVICE.md` — CLI service
- `API_SERVICE.md` — HTTP API service
- `../timeout_resilience/INDEX.md` — Timeout patterns

---

*AI Collaboration Knowledge Base*
