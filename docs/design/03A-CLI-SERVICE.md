---
title: SAGE Knowledge Base - CLI Service Design
version: "0.1.0"
last_updated: "2025-11-30"
status: production-ready
tokens: ~800
---

# CLI Service Design

> **Rich command-line interface with Typer + Rich**

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Implementation](#2-implementation)
- [3. Commands Reference](#3-commands-reference)
- [4. Interactive Mode (REPL)](#4-interactive-mode-repl)

---

## 1. Overview

The CLI Service provides interactive terminal access to SAGE Knowledge Base.

| Feature            | Technology | Description                      |
|--------------------|------------|----------------------------------|
| Command framework  | Typer      | Type-safe CLI with auto-help     |
| Output formatting  | Rich       | Colors, tables, progress bars    |
| Async operations   | asyncio    | Non-blocking knowledge loading   |
| Timeout protection | Built-in   | All operations have timeouts     |

---

## 2. Implementation

```python
# src/sage/services/cli.py
"""
CLI Service - Rich command-line interface.
"""
import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
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
    layer: str = typer.Argument("core", help="Layer to load"),
    timeout: int = typer.Option(5000, "--timeout", "-t"),
    format: str = typer.Option("markdown", "--format", "-f"),
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
    max_results: int = typer.Option(5, "--max", "-m"),
    timeout: int = typer.Option(3000, "--timeout", "-t"),
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

    table.add_row("Version", "0.1.0")
    table.add_row("Layers", "core, guidelines, frameworks, practices")
    table.add_row("Timeout Levels", "T1(100ms) - T5(10s)")
    console.print(table)


@app.command()
def serve(
    service: str = typer.Option("mcp", "--service", "-s"),
    host: str = typer.Option("localhost", "--host", "-h"),
    port: int = typer.Option(8000, "--port", "-p"),
):
    """Start a service (MCP or API)."""
    if service in ("mcp", "all"):
        console.print(f"[green]Starting MCP server on {host}:{port}[/green]")
        from sage.services.mcp_server import run_mcp_server
        asyncio.run(run_mcp_server(host, port))


async def _load_layer(layer: str, timeout_ms: int):
    """Internal: Load layer with timeout."""
    container = get_container()
    loader = container.resolve(SourceProtocol)
    return await loader.source(SourceRequest(layers=[layer], timeout_ms=timeout_ms))


if __name__ == "__main__":
    app()
```

---

## 3. Commands Reference

| Command               | Description              | Example                    |
|-----------------------|--------------------------|----------------------------|
| `sage get [layer]`    | Get knowledge from layer | `sage get core`            |
| `sage search <query>` | Search knowledge base    | `sage search "timeout"`    |
| `sage info`           | Show KB information      | `sage info`                |
| `sage serve`          | Start MCP/API server     | `sage serve --service mcp` |

### Common Options

| Option               | Description     | Default |
|----------------------|-----------------|---------|
| `--timeout`, `-t`    | Timeout in ms   | 5000    |
| `--format`, `-f`     | Output format   | markdown|
| `--help`             | Show help       | -       |

---

## 4. Interactive Mode (REPL)

```bash
# Start interactive mode
sage repl
```

### REPL Commands

| Command          | Description             | Example          |
|------------------|-------------------------|------------------|
| `help`           | Show available commands | `help`           |
| `get <layer>`    | Load knowledge layer    | `get core`       |
| `search <query>` | Search knowledge base   | `search timeout` |
| `layers`         | List available layers   | `layers`         |
| `history`        | Show command history    | `history`        |
| `exit` / `quit`  | Exit REPL               | `exit`           |

### REPL Session Example

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
  3. .knowledge/core/quick_reference.md (score: 0.65)

sage> exit
Goodbye!
```

### REPL Features

| Feature            | Description                          |
|--------------------|--------------------------------------|
| Tab completion     | Auto-complete commands and layers    |
| Command history    | Arrow keys navigate previous commands|
| Syntax highlighting| Rich output with colors              |
| Persistent session | Maintains context between commands   |

---

## Related

- `docs/design/03-services.md` — Services overview
- `docs/design/03b-mcp-service.md` — MCP service design
- `docs/design/03c-api-service.md` — HTTP API design
- `docs/api/cli.md` — CLI API reference

---

*Part of SAGE Knowledge Base*
