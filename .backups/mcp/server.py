"""
Minimal MCP server using FastMCP, compatible with the latest mcp Python SDK.

Tools:
- echo(message: str) → str
- time_now() → str

Run mode: stdio (for JetBrains Junie MCP Command/Process integration)
"""

from mcp.server.fastmcp import FastMCP

app = FastMCP("test-mcp-python")


@app.tool()
def echo(message: str) -> str:
    """Echo a message back."""
    return str(message)


@app.tool()
def time_now() -> str:
    """Return current local time in ISO format."""
    import datetime

    return datetime.datetime.now().isoformat()


if __name__ == "__main__":
    # FastMCP handles the stdio transport and protocol details internally
    import asyncio
    asyncio.run(app.run_stdio_async())
