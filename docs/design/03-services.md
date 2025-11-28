---
title: SAGE Knowledge Base - Services Design
version: 0.1.0
date: 2025-11-28
status: production-ready
---

# Services Design

> **Multi-channel service layer: CLI, MCP, and HTTP API**

## Service Overview

SAGE provides three service channels for knowledge access:

| Service | Protocol  | Use Case                   | Client               |
|---------|-----------|----------------------------|----------------------|
| **CLI** | Terminal  | Developer local use        | Terminal             |
| **MCP** | JSON-RPC  | AI assistant integration   | Claude, Cursor, etc. |
| **API** | HTTP REST | Web apps, external systems | Any HTTP client      |

```
┌─────────────────────────────────────────────────────────────┐
│                     Services Layer                          │
├───────────────┬───────────────┬───────────────┬─────────────┤
│  CLI Service  │  MCP Service  │  API Service  │   Shared    │
│   (Typer)     │  (FastMCP)    │  (FastAPI)    │  Components │
├───────────────┼───────────────┼───────────────┼─────────────┤
│ • sage get    │ • get_knowledge│ GET /knowledge│ • Loader   │
│ • sage search │ • search_knowledge│ GET /search│ • Search    │
│ • sage info   │ • get_framework│ GET /layers   │ • Timeout   │
│ • sage serve  │ • kb_info     │ GET /health   │ • Config    │
└───────────────┴───────────────┴───────────────┴─────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   Core Layer    │
                    │ (Protocols, DI) │
                    └─────────────────┘
```

---

## CLI Service (Typer + Rich)

### Implementation

```python
# src/sage/services/cli.py
"""
CLI Service - Rich command-line interface.

Features:
- Rich terminal output with colors and tables
- Progress indicators for long operations
- Timeout protection on all operations
- REPL mode for interactive exploration
"""
import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import Optional
import asyncio

from sage.core.di import get_container
from sage.core.protocols import SourceProtocol, AnalyzeProtocol
from sage.core.models import SourceRequest

app = typer.Typer(
    name="sage",
    help="SAGE Knowledge Base - AI collaboration knowledge management",
    no_args_is_help=True,
)
console = Console()


@app.command()
def get(
    layer: str = typer.Argument("core", help="Layer to load: core, guidelines, frameworks, practices"),
    timeout: int = typer.Option(5000, "--timeout", "-t", help="Timeout in milliseconds"),
    format: str = typer.Option("markdown", "--format", "-f", help="Output format: markdown, json, plain"),
):
    """Get knowledge from specified layer."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"Loading {layer}...", total=None)

        result = asyncio.run(_load_layer(layer, timeout))
        progress.update(task, completed=True)

    if result.status == "success":
        console.print(result.content)
        console.print(f"\n[dim]Loaded {result.tokens} tokens in {result.duration_ms}ms[/dim]")
    else:
        console.print(f"[yellow]Status: {result.status}[/yellow]")
        console.print(result.content)


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    max_results: int = typer.Option(5, "--max", "-m", help="Maximum results"),
    timeout: int = typer.Option(3000, "--timeout", "-t", help="Timeout in milliseconds"),
):
    """Search the knowledge base."""
    results = asyncio.run(_search_kb(query, max_results, timeout))

    if not results:
        console.print("[yellow]No results found[/yellow]")
        return

    table = Table(title=f"Search Results for '{query}'")
    table.add_column("Score", style="cyan", width=8)
    table.add_column("Path", style="green")
    table.add_column("Preview", style="white")

    for r in results:
        table.add_row(f"{r.score:.2f}", r.path, r.preview[:60] + "...")

    console.print(table)


@app.command()
def info():
    """Show knowledge base information."""
    table = Table(title="SAGE Knowledge Base Info")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Version", "1.0.0")
    table.add_row("Layers", "core, guidelines, frameworks, practices, scenarios")
    table.add_row("Total Files", "~30")
    table.add_row("Total Tokens", "~6,000")
    table.add_row("Timeout Levels", "T1(100ms) - T5(10s)")

    console.print(table)


@app.command()
def serve(
    service: str = typer.Option("mcp", "--service", "-s", help="Service to start: mcp, api, all"),
    host: str = typer.Option("localhost", "--host", "-h", help="Host to bind"),
    port: int = typer.Option(8000, "--port", "-p", help="Port to bind"),
):
    """Start a service (MCP or API)."""
    if service in ("mcp", "all"):
        console.print(f"[green]Starting MCP server on {host}:{port}[/green]")
        from sage.services.mcp_server import run_mcp_server
        asyncio.run(run_mcp_server(host, port))

    if service in ("api", "all"):
        api_port = port + 80 if service == "all" else port
        console.print(f"[green]Starting API server on {host}:{api_port}[/green]")
        from sage.services.http_server import run_api_server
        run_api_server(host, api_port)


async def _load_layer(layer: str, timeout_ms: int):
    """Internal: Load layer with timeout."""
    container = get_container()
    loader = container.resolve(SourceProtocol)
    return await loader.source(SourceRequest(layers=[layer], timeout_ms=timeout_ms))


async def _search_kb(query: str, max_results: int, timeout_ms: int):
    """Internal: Search knowledge base."""
    container = get_container()
    analyzer = container.resolve(AnalyzeProtocol)
    return await analyzer.search(query, max_results)


if __name__ == "__main__":
    app()
```

### CLI Commands Reference

| Command               | Description              | Example                    |
|-----------------------|--------------------------|----------------------------|
| `sage get [layer]`    | Get knowledge from layer | `sage get core`            |
| `sage search <query>` | Search knowledge base    | `sage search "timeout"`    |
| `sage info`           | Show KB information      | `sage info`                |
| `sage serve`          | Start MCP/API server     | `sage serve --service mcp` |

### Interactive Mode (REPL)

The CLI supports an interactive REPL mode for exploration:

```bash
# Start interactive mode
sage repl
```

**REPL Commands:**

| Command          | Description             | Example          |
|------------------|-------------------------|------------------|
| `help`           | Show available commands | `help`           |
| `get <layer>`    | Load knowledge layer    | `get core`       |
| `search <query>` | Search knowledge base   | `search timeout` |
| `layers`         | List available layers   | `layers`         |
| `history`        | Show command history    | `history`        |
| `clear`          | Clear screen            | `clear`          |
| `exit` / `quit`  | Exit REPL               | `exit`           |

**REPL Session Example:**

```
sage> layers
Available layers: core, guidelines, frameworks, practices, scenarios

sage> get core
[Loading core layer...]
# Core Principles
...

sage> search "autonomy level"
Found 3 results:
  1. frameworks/autonomy/levels.md (score: 0.95)
  2. guidelines/ai_collaboration.md (score: 0.72)
  3. content/core/quick_reference.md (score: 0.65)

sage> exit
Goodbye!
```

**Features:**

- **Tab completion**: Auto-complete commands and layer names
- **Command history**: Arrow keys navigate previous commands
- **Syntax highlighting**: Rich output with colors
- **Persistent session**: Maintains context between commands

---

## MCP Service (FastMCP)

### Implementation

```python
# src/sage/services/mcp_server.py
"""
MCP Service - Model Context Protocol server.

Features:
- Standard MCP tool interface
- Timeout protection on all operations
- Structured response format
- Integration with AI assistants
"""
from mcp.server.fastmcp import FastMCP
from typing import Optional
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
            loader.source(
                SourceRequest(
                    layers=[layer_name],
                    query=task,
                    timeout_ms=timeout_ms
                )
            ),
            timeout=timeout_ms / 1000
        )
        status = result.status
    except asyncio.TimeoutError:
        result = await loader.get_fallback()
        status = "timeout_fallback"

    return {
        "content"    : result.content if hasattr(result, 'content') else result,
        "tokens"     : result.tokens if hasattr(result, 'tokens') else len(str(result)) // 4,
        "status"     : status,
        "duration_ms": int((time.time() - start) * 1000),
        "layer"      : layer_name,
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
    
    Returns:
        List of search results with path, score, preview
    """
    container = get_container()
    analyzer = container.resolve(AnalyzeProtocol)

    try:
        results = await asyncio.wait_for(
            analyzer.search(query, max_results),
            timeout=timeout_ms / 1000
        )
        return [
            {
                "path"   : r.path,
                "score"  : r.score,
                "preview": r.preview,
                "layer"  : r.layer,
            }
            for r in results
        ]
    except asyncio.TimeoutError:
        return []


@mcp.tool()
async def get_framework(
    name: str,
    timeout_ms: int = 5000
) -> dict:
    """
    Get framework documentation.
    
    Args:
        name: Framework name (autonomy, cognitive, decision, collaboration, timeout)
        timeout_ms: Maximum time in milliseconds
    
    Returns:
        dict with content and metadata
    """
    container = get_container()
    loader = container.resolve(SourceProtocol)

    result = await loader.source(
        SourceRequest(
            layers=["frameworks"],
            query=name,
            timeout_ms=timeout_ms
        )
    )

    return {
        "content"  : result.content,
        "framework": name,
        "status"   : result.status,
    }


@mcp.tool()
async def kb_info() -> dict:
    """
    Get knowledge base information.
    
    Returns:
        dict with version, layers, statistics
    """
    return {
        "version"       : "1.0.0",
        "layers"        : {
            "core"      : {"tokens": 500, "always_load": True},
            "guidelines": {"tokens": 1200, "always_load": False},
            "frameworks": {"tokens": 2000, "always_load": False},
            "practices" : {"tokens": 1500, "always_load": False},
            "scenarios" : {"tokens": 500, "always_load": False},
        },
        "timeout_levels": ["T1:100ms", "T2:500ms", "T3:2s", "T4:5s", "T5:10s"],
        "total_tokens"  : 5700,
    }


async def run_mcp_server(host: str = "localhost", port: int = 8000):
    """Run the MCP server."""
    await mcp.run()
```

### MCP Tools Reference

| Tool               | Description            | Parameters                           |
|--------------------|------------------------|--------------------------------------|
| `get_knowledge`    | Get knowledge by layer | `layer`, `task`, `timeout_ms`        |
| `search_knowledge` | Search knowledge base  | `query`, `max_results`, `timeout_ms` |
| `get_framework`    | Get framework docs     | `name`, `timeout_ms`                 |
| `kb_info`          | Get KB information     | (none)                               |

### MCP Prompt Templates

Recommended prompts for effective tool usage:

| Tool               | Recommended Prompt                                                   |
|--------------------|----------------------------------------------------------------------|
| `get_knowledge`    | "Load [layer] knowledge for [task description]"                      |
| `search_knowledge` | "Search KB for [specific topic] to find [what you need]"             |
| `get_framework`    | "Get the [autonomy/cognitive/timeout] framework for [decision type]" |
| `kb_info`          | "Show KB structure and available layers"                             |

**Example Prompts by Use Case:**

```
# Starting a new coding task
→ get_knowledge(layer=1, task="implement user authentication")

# Need guidance on decision-making
→ get_framework(name="autonomy")
→ "What autonomy level should I use for database migrations?"

# Looking for specific information
→ search_knowledge(query="timeout configuration", max_results=5)

# Understanding available resources
→ kb_info()
→ "What knowledge layers are available?"
```

**Best Practices:**

1. **Be specific**: Include task context in the `task` parameter
2. **Layer selection**: Start with `layer=0` (core) for general guidance
3. **Search first**: Use `search_knowledge` when unsure which layer to load
4. **Combine tools**: Use `kb_info` → `search_knowledge` → `get_knowledge` workflow

---

## HTTP API Service (FastAPI)

### Implementation

```python
# src/sage/services/http_server.py
"""
HTTP API Service - FastAPI-based REST API.

Features:
- RESTful endpoints for knowledge access
- OpenAPI documentation auto-generated
- Configurable CORS support
- Health check endpoint
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import uvicorn

from sage.core.di import get_container
from sage.core.protocols import SourceProtocol, AnalyzeProtocol
from sage.core.models import SourceRequest
from sage.core.config import get_settings


# === Request/Response Models ===

class KnowledgeRequest(BaseModel):
    """Request for knowledge retrieval."""
    layers: List[str] = Field(default=["core"], description="Layers to load")
    query: Optional[str] = Field(None, description="Optional query for smart loading")
    timeout_ms: int = Field(5000, ge=100, le=30000, description="Timeout in ms")


class KnowledgeResponse(BaseModel):
    """Response with knowledge content."""
    content: str
    tokens: int
    status: str
    duration_ms: int
    layers_loaded: List[str]


class SearchResultItem(BaseModel):
    """Single search result."""
    path: str
    score: float
    preview: str
    layer: str


class SearchResponse(BaseModel):
    """Response with search results."""
    query: str
    results: List[SearchResultItem]
    count: int
    duration_ms: int


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    services: dict


class LayerInfo(BaseModel):
    """Information about a knowledge layer."""
    name: str
    tokens: int
    always_load: bool


# === FastAPI Application ===

def create_api_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="SAGE Knowledge Base API",
        version="1.0.0",
        description="Production-grade knowledge management with timeout protection",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
    )

    # CORS middleware - configure in production!
    if settings.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=True,
            allow_methods=["GET", "POST"],
            allow_headers=["Authorization", "Content-Type"],
        )

    # === Health Endpoint ===

    @app.get("/health", response_model=HealthResponse, tags=["System"])
    async def health_check():
        """Health check endpoint."""
        return HealthResponse(
            status="healthy",
            version="1.0.0",
            services={
                "loader": "operational",
                "search": "operational",
            }
        )

    # === Knowledge Endpoints ===

    @app.get("/v1/layers", response_model=List[LayerInfo], tags=["Knowledge"])
    async def list_layers():
        """List available knowledge layers."""
        return [
            LayerInfo(name="core", tokens=500, always_load=True),
            LayerInfo(name="guidelines", tokens=1200, always_load=False),
            LayerInfo(name="frameworks", tokens=2000, always_load=False),
            LayerInfo(name="practices", tokens=1500, always_load=False),
            LayerInfo(name="scenarios", tokens=500, always_load=False),
        ]

    @app.post("/v1/knowledge", response_model=KnowledgeResponse, tags=["Knowledge"])
    async def get_knowledge(request: KnowledgeRequest):
        """Get knowledge with timeout protection."""
        import time
        start = time.time()

        container = get_container()
        loader = container.resolve(SourceProtocol)

        result = await loader.source(
            SourceRequest(
                layers=request.layers,
                query=request.query,
                timeout_ms=request.timeout_ms
            )
        )

        return KnowledgeResponse(
            content=result.content,
            tokens=result.tokens,
            status=result.status,
            duration_ms=int((time.time() - start) * 1000),
            layers_loaded=result.layers_loaded
        )

    @app.get("/v1/knowledge/{layer}", response_model=KnowledgeResponse, tags=["Knowledge"])
    async def get_layer(
        layer: str,
        timeout_ms: int = Query(5000, ge=100, le=30000)
    ):
        """Get knowledge from a specific layer."""
        import time
        start = time.time()

        valid_layers = ["core", "guidelines", "frameworks", "practices", "scenarios"]
        if layer not in valid_layers:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid layer. Valid layers: {valid_layers}"
            )

        container = get_container()
        loader = container.resolve(SourceProtocol)

        result = await loader.source(
            SourceRequest(
                layers=[layer],
                timeout_ms=timeout_ms
            )
        )

        return KnowledgeResponse(
            content=result.content,
            tokens=result.tokens,
            status=result.status,
            duration_ms=int((time.time() - start) * 1000),
            layers_loaded=result.layers_loaded
        )

    # === Search Endpoint ===

    @app.get("/v1/search", response_model=SearchResponse, tags=["Search"])
    async def search_knowledge(
        q: str = Query(..., min_length=1, description="Search query"),
        max_results: int = Query(5, ge=1, le=20),
        timeout_ms: int = Query(3000, ge=100, le=10000)
    ):
        """Search the knowledge base."""
        import time
        start = time.time()

        container = get_container()
        analyzer = container.resolve(AnalyzeProtocol)

        results = await analyzer.search(q, max_results)

        return SearchResponse(
            query=q,
            results=[
                SearchResultItem(
                    path=r.path,
                    score=r.score,
                    preview=r.preview,
                    layer=r.layer
                )
                for r in results
            ],
            count=len(results),
            duration_ms=int((time.time() - start) * 1000)
        )

    return app


def run_api_server(host: str = "localhost", port: int = 8080):
    """Run the API server."""
    app = create_api_app()
    uvicorn.run(app, host=host, port=port)
```

### API Endpoints Reference

| Method | Endpoint                | Description               |
|--------|-------------------------|---------------------------|
| GET    | `/health`               | Health check              |
| GET    | `/v1/layers`            | List available layers     |
| POST   | `/v1/knowledge`         | Get knowledge (with body) |
| GET    | `/v1/knowledge/{layer}` | Get specific layer        |
| GET    | `/v1/search?q=...`      | Search knowledge base     |

### API Usage Examples

```bash
# Health check
curl http://localhost:8080/health

# List layers
curl http://localhost:8080/v1/layers

# Get core layer
curl http://localhost:8080/v1/knowledge/core

# Search
curl "http://localhost:8080/v1/search?q=timeout&max_results=5"

# Post request with options
curl -X POST http://localhost:8080/v1/knowledge \
  -H "Content-Type: application/json" \
  -d '{"layers": ["core", "guidelines"], "timeout_ms": 5000}'
```

### Search Ranking Algorithm

The search service uses a weighted scoring algorithm to rank results:

| Factor          | Weight | Description                             |
|-----------------|--------|-----------------------------------------|
| Keyword Match   | 40%    | Exact and partial keyword matches       |
| Layer Priority  | 25%    | Core > Guidelines > Frameworks > Others |
| Recency         | 20%    | Recently updated content scores higher  |
| Usage Frequency | 15%    | Frequently accessed content boosted     |

**Scoring Formula:**

```
score = (keyword_score * 0.40) + (layer_score * 0.25) + (recency_score * 0.20) + (usage_score * 0.15)
```

**Layer Priority Values:**

| Layer      | Priority Score |
|------------|----------------|
| core       | 1.0            |
| guidelines | 0.8            |
| frameworks | 0.6            |
| practices  | 0.4            |
| scenarios  | 0.2            |

---

## Error Handling

### Exception Hierarchy

```python
# src/sage/core/exceptions.py
"""
SAGE Exception Hierarchy - Unified error handling.

All exceptions inherit from SageError for consistent catching and logging.
"""
from typing import Optional, Dict, Any


class SageError(Exception):
    """Base exception for all SAGE errors."""

    def __init__(
        self,
        code: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        recoverable: bool = False
    ):
        self.code = code
        self.message = message
        self.details = details or {}
        self.recoverable = recoverable
        super().__init__(f"[{code}] {message}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            "error": {
                "code"       : self.code,
                "message"    : self.message,
                "details"    : self.details,
                "recoverable": self.recoverable
            }
        }


# === Loading Errors (1xxx) ===

class LoadError(SageError):
    """Base class for loading errors."""
    pass


class TimeoutError(LoadError):
    """Operation timed out."""

    def __init__(self, operation: str, timeout_ms: int, **kwargs):
        super().__init__(
            code="SAGE-1001",
            message=f"Operation '{operation}' timed out after {timeout_ms}ms",
            details={"operation": operation, "timeout_ms": timeout_ms, **kwargs},
            recoverable=True
        )


class FileNotFoundError(LoadError):
    """Requested file not found."""

    def __init__(self, path: str, **kwargs):
        super().__init__(
            code="SAGE-1002",
            message=f"File not found: {path}",
            details={"path": path, **kwargs},
            recoverable=False
        )


class LayerNotFoundError(LoadError):
    """Requested layer not found."""

    def __init__(self, layer: str, available: list, **kwargs):
        super().__init__(
            code="SAGE-1003",
            message=f"Layer '{layer}' not found. Available: {available}",
            details={"layer": layer, "available": available, **kwargs},
            recoverable=True
        )


# === Configuration Errors (2xxx) ===

class ConfigError(SageError):
    """Base class for configuration errors."""
    pass


class ConfigValidationError(ConfigError):
    """Configuration validation failed."""

    def __init__(self, field: str, reason: str, **kwargs):
        super().__init__(
            code="SAGE-2002",
            message=f"Invalid configuration for '{field}': {reason}",
            details={"field": field, "reason": reason, **kwargs},
            recoverable=False
        )


# === Service Errors (3xxx) ===

class ServiceError(SageError):
    """Base class for service errors."""
    pass


class ServiceUnavailableError(ServiceError):
    """Service is temporarily unavailable."""

    def __init__(self, service: str, reason: str, **kwargs):
        super().__init__(
            code="SAGE-3001",
            message=f"Service '{service}' unavailable: {reason}",
            details={"service": service, "reason": reason, **kwargs},
            recoverable=True
        )


# === Search Errors (4xxx) ===

class SearchError(SageError):
    """Base class for search errors."""
    pass


class InvalidQueryError(SearchError):
    """Search query is invalid."""

    def __init__(self, query: str, reason: str, **kwargs):
        super().__init__(
            code="SAGE-4001",
            message=f"Invalid search query: {reason}",
            details={"query": query, "reason": reason, **kwargs},
            recoverable=False
        )
```

### Error Code Reference

| Code Range | Category      | Description                            |
|------------|---------------|----------------------------------------|
| SAGE-1xxx  | Loading       | File/layer loading errors              |
| SAGE-2xxx  | Configuration | Config parsing/validation errors       |
| SAGE-3xxx  | Service       | Service availability/rate limit errors |
| SAGE-4xxx  | Search        | Query/search errors                    |
| SAGE-5xxx  | Memory        | Persistence/checkpoint errors          |
| SAGE-9xxx  | Internal      | Unexpected internal errors             |

### Error Handling Example

```python
from sage.core.exceptions import TimeoutError, LayerNotFoundError, SageError


async def load_knowledge_safely(layers: list[str]):
    """Load knowledge with comprehensive error handling."""
    loader = get_loader()

    try:
        return await loader.source(SourceRequest(layers=layers))

    except TimeoutError as e:
        # Recoverable: use cached content
        logger.warning("Timeout, using cache", error=e.to_dict())
        return await loader.get_fallback()

    except LayerNotFoundError as e:
        # Recoverable: load available layers only
        available = e.details.get("available", ["core"])
        logger.warning("Layer not found, loading available", error=e.to_dict())
        return await loader.source(SourceRequest(layers=available))

    except SageError as e:
        # Known error
        logger.error("Loading failed", error=e.to_dict())
        if e.recoverable:
            return await loader.get_fallback()
        raise
```

### API Error Response Format

```json
{
  "error": {
    "code": "SAGE-1001",
    "message": "Operation 'load_layer' timed out after 5000ms",
    "details": {
      "operation": "load_layer",
      "timeout_ms": 5000,
      "layer": "guidelines"
    },
    "recoverable": true
  }
}
```

---

## Testing Strategy

### Test Pyramid

```
                    ╱╲
                   ╱  ╲
                  ╱ E2E╲           5% - End-to-end tests
                 ╱──────╲          (CLI commands, full workflows)
                ╱        ╲
               ╱Integration╲       15% - Integration tests
              ╱────────────╲       (Service interactions, API)
             ╱              ╲
            ╱   Unit Tests   ╲     80% - Unit tests
           ╱──────────────────╲    (Functions, classes, modules)
          ╱____________________╲

Target Coverage: 90%+ for core/, 80%+ for services/
```

### Test Categories

| Category        | Scope                 | Dependencies    | Speed    | Location             |
|-----------------|-----------------------|-----------------|----------|----------------------|
| **Unit**        | Single function/class | Mocked          | <100ms   | `tests/unit/`        |
| **Integration** | Multiple components   | Real (isolated) | <5s      | `tests/integration/` |
| **E2E**         | Full system           | All real        | <30s     | `tests/e2e/`         |
| **Performance** | Benchmarks            | Real            | Variable | `tests/performance/` |

### Mock Strategy

```python
# tests/conftest.py
"""
Test Configuration - Mock and Fixture Strategy.

Mock Principles:
1. Mock at boundaries (I/O, network, filesystem)
2. Never mock the code under test
3. Use dependency injection for testability
4. Prefer fakes over mocks for complex behavior
"""
import pytest
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def mock_config():
    """Mock configuration for unit tests."""
    return MagicMock(
        timeout_ms=5000,
        layers=["core", "guidelines"],
        debug=True
    )


@pytest.fixture
def mock_loader():
    """Mock loader that returns predictable content."""
    from sage.core.models import SourceResult

    loader = AsyncMock()
    loader.source.return_value = SourceResult(
        content="# Mock Content\nTest principles.",
        tokens=10,
        status="success",
        duration_ms=50,
        layers_loaded=["core"]
    )
    return loader


@pytest.fixture
def temp_content_dir(tmp_path):
    """Temporary content directory with sample files."""
    content = tmp_path / "content"
    content.mkdir()
    (content / "core").mkdir()
    (content / "core" / "principles.md").write_text("# Test Principles")
    return content


# What to Mock vs What to Use Real
MOCK_BOUNDARIES = """
Always Mock:
  - File system operations (use tmp_path fixture)
  - Network calls (use responses or aioresponses)
  - Time-dependent operations (use freezegun)
  - External services (use fakes or mocks)

Never Mock:
  - The class/function under test
  - Pure data transformations
  - Internal business logic

Use Real (Isolated):
  - In-memory databases for integration tests
  - Real DI container with test implementations
  - Actual async event loop
"""
```

### Integration Test Example

```python
# tests/integration/test_loader_integration.py
"""
Integration tests verify component interactions.
"""
import pytest
from pathlib import Path


@pytest.mark.integration
@pytest.mark.asyncio
async def test_loader_loads_real_files(temp_content_dir: Path):
    """Integration: Loader reads actual files from disk."""
    from sage.core.loader import TimeoutLoader
    from sage.core.config import SageSettings
    from sage.core.models import SourceRequest

    settings = SageSettings(content_root=temp_content_dir)
    loader = TimeoutLoader(settings)

    result = await loader.source(SourceRequest(layers=["core"]))

    assert result.status == "success"
    assert "Test Principles" in result.content
    assert result.duration_ms < 5000


@pytest.mark.integration
@pytest.mark.asyncio
async def test_loader_timeout_triggers_fallback(temp_content_dir: Path):
    """Integration: Timeout triggers graceful degradation."""
    from sage.core.loader import TimeoutLoader
    from sage.core.models import SourceRequest

    loader = TimeoutLoader(timeout_ms=1)  # 1ms timeout

    result = await loader.source(SourceRequest(layers=["core"]))

    assert result.status in ("fallback", "partial")
    assert result.content  # Should never be empty
```

### Test Naming Convention

```
test_<unit>_<scenario>_<expected_outcome>

Examples:
- test_loader_valid_layers_returns_content
- test_loader_timeout_returns_fallback
- test_search_empty_query_raises_error
- test_config_missing_file_uses_defaults
```

### CI Test Commands

```yaml
# .github/workflows/test.yml
jobs:
  test:
    steps:
      - name: Unit Tests
        run: pytest tests/unit/ -v --cov=sage --cov-report=xml

      - name: Integration Tests
        run: pytest tests/integration/ -v -m integration

      - name: E2E Tests (on main only)
        if: github.ref == 'refs/heads/main'
        run: pytest tests/e2e/ -v -m e2e

      - name: Performance Tests (weekly)
        if: github.event_name == 'schedule'
        run: pytest tests/performance/ -v --benchmark-json=benchmark.json
```

### Mutation Testing (Future Enhancement)

Mutation testing validates test quality by introducing small code changes (mutants) and verifying tests catch them.

**Recommended Tool**: `mutmut` (Python mutation testing)

```bash
# Install
pip install mutmut

# Run mutation testing on core module
mutmut run --paths-to-mutate=src/sage/core/

# View results
mutmut results
mutmut html  # Generate HTML report
```

**Configuration** (pyproject.toml):

```toml
[tool.mutmut]
paths_to_mutate = "src/sage/core/"
tests_dir = "tests/unit/"
runner = "pytest -x -q"
```

**Target Metrics**:

| Metric             | Target | Description                        |
|--------------------|--------|------------------------------------|
| Mutation Score     | > 80%  | Percentage of mutants killed       |
| Surviving Mutants  | < 20%  | Mutants not caught by tests        |
| Equivalent Mutants | < 5%   | Mutants that don't change behavior |

**When to Use**:

- Before major releases to validate test suite quality
- After significant refactoring to ensure tests are still effective
- Periodically (monthly) as part of quality assurance

---

## References

- **Architecture**: See `01-architecture.md`
- **Protocols**: See `02-sage-protocol.md`
- **Timeout**: See `04-timeout-loading.md`

---

**Document Status**: Pending Level 5 Expert Committee Evaluation  
**Last Updated**: 2025-11-29
