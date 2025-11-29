# MCP Integration Scenario

> Context and guidelines for Model Context Protocol integration tasks

---

## Scenario Overview

| Aspect | Description |
|--------|-------------|
| **Domain** | AI agent integration via MCP |
| **Task Types** | Server setup, tool development, client configuration |
| **Autonomy Level** | L3 (Medium) for new integrations, L4 for maintenance |
| **Key Concerns** | Protocol compliance, timeout handling, error recovery |

---

## Common Tasks

### Server Setup

- Configuring MCP server settings
- Setting up authentication/authorization
- Configuring resource endpoints
- Testing server connectivity

### Tool Development

- Creating custom MCP tools
- Defining input/output schemas
- Implementing timeout handling
- Adding error responses

### Client Integration

- Configuring Claude Desktop
- Setting up other MCP clients
- Testing tool invocations
- Debugging connection issues

---

## MCP Fundamentals

### Protocol Overview

MCP (Model Context Protocol) enables AI agents to interact with external systems:

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│  AI Agent   │ ←───→ │ MCP Server  │ ←───→ │  Knowledge  │
│  (Claude)   │       │   (SAGE)    │       │    Base     │
└─────────────┘       └─────────────┘       └─────────────┘
```

### Core Concepts

| Concept | Description |
|---------|-------------|
| **Tools** | Functions the AI can call |
| **Resources** | Data the AI can access |
| **Prompts** | Pre-defined prompt templates |

---

## Best Practices

### Tool Design

1. **Clear naming**: Use descriptive tool names
2. **Schema validation**: Define strict input schemas
3. **Timeout awareness**: Respect timeout hierarchy
4. **Graceful degradation**: Return partial results on timeout

Example tool pattern:

```python
@mcp_server.tool()
async def sage_get_knowledge(
    layer: str,
    topic: str | None = None,
    timeout_ms: int = 2000
) -> dict:
    """
    Retrieve knowledge from the SAGE knowledge base.
    
    Args:
        layer: Knowledge layer (core, guidelines, frameworks, practices)
        topic: Optional specific topic within the layer
        timeout_ms: Timeout in milliseconds (default: 2000)
    
    Returns:
        Dictionary with content and metadata
    """
    try:
        result = await loader.load(layer, topic, timeout_ms)
        return {
            "content": result.content,
            "metadata": result.metadata.dict(),
            "complete": result.complete
        }
    except TimeoutError as e:
        return {
            "content": e.partial_result,
            "metadata": {"timeout": True},
            "complete": False
        }
```

### Resource Design

Use URI patterns for resources:

```python
@mcp_server.resource("knowledge://{layer}/{topic}")
async def knowledge_resource(layer: str, topic: str) -> str:
    """Provide knowledge content as a resource."""
    result = await loader.load(layer, topic)
    return result.content
```

### Error Handling

Always provide meaningful error responses:

```python
{
    "error": {
        "code": "TIMEOUT",
        "message": "Operation exceeded T3 timeout",
        "details": {
            "timeout_level": "T3",
            "elapsed_ms": 2150
        }
    },
    "fallback": {
        "content": "Partial content...",
        "complete": false
    }
}
```

---

## Configuration

### Server Configuration

`config/services/mcp.yaml`:

```yaml
mcp:
  host: localhost
  port: 8000
  timeout_ms: 5000
  
  capabilities:
    - knowledge_retrieval
    - search
    - context_management
  
  tools:
    sage_get_knowledge:
      enabled: true
      default_timeout: 2000
    sage_search:
      enabled: true
      max_results: 20
```

### Client Configuration

Claude Desktop (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "sage": {
      "command": "sage",
      "args": ["serve"],
      "env": {
        "SAGE_CONFIG": "/path/to/config/sage.yaml",
        "SAGE_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

---

## Timeout Strategy

### MCP-Specific Timeouts

| Operation | Timeout | Level |
|-----------|---------|-------|
| Tool invocation | 5000ms | T4 |
| Resource fetch | 2000ms | T3 |
| Search query | 2000ms | T3 |
| Health check | 500ms | T2 |

### Graceful Degradation

```python
async def load_with_fallback(layer: str, timeout_ms: int):
    try:
        return await loader.load(layer, timeout_ms=timeout_ms)
    except TimeoutError as e:
        # Return partial result
        return LoadResult(
            content=e.partial_result or get_fallback(layer),
            complete=False
        )
```

---

## Testing

### Unit Testing Tools

```python
import pytest
from sage.services.mcp_server import mcp_server

@pytest.mark.asyncio
async def test_get_knowledge_tool():
    result = await mcp_server.call_tool(
        "sage_get_knowledge",
        {"layer": "core"}
    )
    assert "content" in result
    assert result["complete"] is True
```

### Integration Testing

```python
@pytest.mark.asyncio
async def test_mcp_client_connection():
    async with MCPClient("localhost", 8000) as client:
        tools = await client.list_tools()
        assert "sage_get_knowledge" in [t.name for t in tools]
```

### Manual Testing

```bash
# Start server
sage serve --port 8000

# Test with curl (if REST endpoint enabled)
curl http://localhost:8000/health

# Test in Claude Desktop
# Ask: "Use sage_get_knowledge to load core principles"
```

---

## Debugging

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Connection refused | Server not running | Start server with `sage serve` |
| Tool not found | Tool not registered | Check tool registration |
| Timeout errors | Slow operations | Increase timeout or optimize |
| Empty response | Content not found | Verify content paths |

### Debug Logging

```bash
# Enable debug logging
SAGE_LOG_LEVEL=DEBUG sage serve

# Check logs
tail -f .logs/sage.log
```

### Health Check

```python
@mcp_server.tool()
async def sage_health() -> dict:
    """Check server health."""
    return {
        "status": "healthy",
        "version": __version__,
        "uptime": get_uptime()
    }
```

---

## Token Budget

For MCP integration tasks:

| Task | Budget | Layers |
|------|--------|--------|
| Tool development | 4000 | core, practices/engineering, api docs |
| Client setup | 2000 | core, guides |
| Debugging | 3000 | core, practices, api docs |
| Protocol design | 5000 | all relevant layers |

---

## Related Scenarios

- `python_backend/` — Python development context
- `plugin_development/` — Plugin development context
- `knowledge_management/` — Knowledge management context

---

## Related Content

- `docs/api/mcp.md` — MCP API reference
- `docs/guides/quickstart.md#mcp-setup` — MCP quick start
- `docs/guides/advanced.md#mcp-advanced` — Advanced MCP features
- `config/services/mcp.yaml` — MCP configuration
- `docs/design/02-sage-protocol.md` — Protocol design document

---

*SAGE Knowledge Base - MCP Integration Scenario*
