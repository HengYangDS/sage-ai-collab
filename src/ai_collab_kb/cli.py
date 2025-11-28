"""
CLI - Rich Command Line Interface for AI Collaboration Knowledge Base.

This module provides:
- Modern CLI with Rich UI (progress, tables, panels)
- Knowledge retrieval commands
- Search functionality
- Server management
- Interactive mode

Author: AI Collaboration KB Team
Version: 2.0.0
"""

import asyncio
from pathlib import Path

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table

# Local imports
from .loader import KnowledgeLoader, Layer

# Initialize
app = typer.Typer(
    name="aikb",
    help="AI Collaboration Knowledge Base CLI - Production-grade knowledge management",
    add_completion=True,
    no_args_is_help=True,
)
console = Console()

# Global loader
_loader: KnowledgeLoader | None = None


def get_loader() -> KnowledgeLoader:
    """Get or create the knowledge loader."""
    global _loader
    if _loader is None:
        _loader = KnowledgeLoader()
    return _loader


# ============================================================================
# Helper Functions
# ============================================================================


def run_async(coro):
    """Run an async coroutine."""
    return asyncio.run(coro)


def display_content(content: str, format: str = "markdown"):
    """Display content with appropriate formatting."""
    if format == "markdown":
        console.print(Markdown(content))
    elif format == "syntax":
        console.print(Syntax(content, "markdown", theme="monokai"))
    elif format == "raw":
        console.print(content)
    else:
        console.print(Markdown(content))


def display_result(result, verbose: bool = False):
    """Display a load result with status."""
    status_colors = {
        "success": "green",
        "partial": "yellow",
        "fallback": "red",
        "error": "red",
    }
    color = status_colors.get(result.status, "white")

    # Status line
    console.print(f"[{color}]Status: {result.status}[/{color}]", end="")
    console.print(f" | Tokens: ~{result.tokens_estimate}", end="")
    console.print(f" | Duration: {result.duration_ms}ms")

    if verbose:
        console.print(f"[dim]Files: {', '.join(result.files_loaded)}[/dim]")
        if result.errors:
            for err in result.errors:
                console.print(f"[red]Error: {err}[/red]")

    console.print()
    display_content(result.content)


# ============================================================================
# Commands
# ============================================================================


@app.command()
def get(
    layer: int = typer.Argument(
        0, help="Layer (0=core, 1=guidelines, 2=frameworks, 3=practices)"
    ),
    topic: str | None = typer.Option(
        None, "--topic", "-t", help="Specific topic or task"
    ),
    format: str = typer.Option(
        "markdown", "--format", "-f", help="Output format: markdown, syntax, raw"
    ),
    timeout: int = typer.Option(5000, "--timeout", help="Timeout in milliseconds"),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Show detailed information"
    ),
):
    """
    Get knowledge from the knowledge base.

    Examples:
        aikb get                    # Get core principles
        aikb get 1                  # Get all guidelines
        aikb get -t "fix bug"       # Get code-related knowledge
        aikb get -t "design api"    # Get design knowledge
    """
    loader = get_loader()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task_id = progress.add_task(f"Loading layer {layer}...", total=None)

        async def do_load():
            if topic:
                return await loader.load_for_task(topic, timeout_ms=timeout)
            else:
                layer_map = {
                    0: Layer.L1_CORE,
                    1: Layer.L2_GUIDELINES,
                    2: Layer.L3_FRAMEWORKS,
                    3: Layer.L4_PRACTICES,
                }
                layer_enum = layer_map.get(layer, Layer.L1_CORE)
                return await loader.load(layer=layer_enum, timeout_ms=timeout)

        result = run_async(do_load())
        progress.remove_task(task_id)

    display_result(result, verbose)


@app.command()
def guidelines(
    section: str = typer.Argument(
        "overview",
        help="Section: quick_start, planning, code_style, engineering, documentation, python, ai_collaboration, cognitive, quality, success",
    ),
    timeout: int = typer.Option(3000, "--timeout", help="Timeout in milliseconds"),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Show detailed information"
    ),
):
    """
    Get engineering guidelines by section.

    Examples:
        aikb guidelines                    # Overview
        aikb guidelines code_style         # Code style
        aikb guidelines ai_collaboration   # AI collaboration
        aikb guidelines python             # Python practices
    """
    loader = get_loader()

    # Section name mapping
    section_map = {
        "overview": "00_quick_start",
        "quick_start": "00_quick_start",
        "planning": "01_planning_design",
        "code_style": "02_code_style",
        "engineering": "03_engineering",
        "documentation": "04_documentation",
        "python": "05_python",
        "ai_collaboration": "06_ai_collaboration",
        "cognitive": "07_cognitive",
        "quality": "08_quality",
        "success": "09_success",
    }
    chapter = section_map.get(section.lower(), section)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task(f"Loading {section}...", total=None)
        result = run_async(loader.load_guidelines(chapter, timeout_ms=timeout))

    display_result(result, verbose)


@app.command()
def framework(
    name: str = typer.Argument(
        ..., help="Framework: autonomy, cognitive, decision, collaboration, timeout"
    ),
    timeout: int = typer.Option(5000, "--timeout", help="Timeout in milliseconds"),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Show detailed information"
    ),
):
    """
    Get framework documentation.

    Examples:
        aikb framework autonomy     # Autonomy levels
        aikb framework cognitive    # Cognitive enhancement
        aikb framework decision     # Decision framework
    """
    loader = get_loader()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task(f"Loading {name} framework...", total=None)
        result = run_async(loader.load_framework(name, timeout_ms=timeout))

    display_result(result, verbose)


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    limit: int = typer.Option(10, "--limit", "-n", help="Maximum results"),
    timeout: int = typer.Option(3000, "--timeout", help="Timeout in milliseconds"),
):
    """
    Search the knowledge base.

    Examples:
        aikb search "autonomy"
        aikb search "testing strategy" -n 5
    """
    loader = get_loader()

    with console.status("[bold green]Searching..."):
        results = run_async(loader.search(query, max_results=limit, timeout_ms=timeout))

    if not results:
        console.print("[yellow]No results found[/yellow]")
        return

    table = Table(title=f"Search Results for '{query}'")
    table.add_column("Score", style="cyan", width=8)
    table.add_column("Path", style="green")
    table.add_column("Preview", style="white", max_width=60)

    for r in results:
        preview = r.get("preview", "")[:60]
        if len(r.get("preview", "")) > 60:
            preview += "..."
        table.add_row(str(r.get("score", 0)), r.get("path", ""), preview)

    console.print(table)


@app.command()
def info():
    """Show knowledge base information."""
    loader = get_loader()
    kb_path = loader.kb_path

    # Count files
    def count_files(path: Path, pattern: str = "*.md") -> int:
        if not path.exists():
            return 0
        return len(list(path.glob(pattern)))

    def count_dirs(path: Path) -> int:
        if not path.exists():
            return 0
        return len([d for d in path.iterdir() if d.is_dir()])

    # Build info table
    table = Table(title="AI Collaboration Knowledge Base")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    info_data = [
        ("Version", "2.0.0"),
        ("Status", "Operational"),
        ("KB Path", str(kb_path)),
        ("", ""),
        ("Core Files", str(count_files(kb_path / "01_core"))),
        ("Guidelines", str(count_files(kb_path / "02_guidelines"))),
        ("Frameworks", str(count_dirs(kb_path / "03_frameworks"))),
        ("Practices", str(count_dirs(kb_path / "04_practices"))),
        ("Templates", str(count_files(kb_path / "06_templates"))),
        ("Scenarios", str(count_dirs(kb_path / "07_scenarios"))),
        ("", ""),
        ("Cache Files", str(loader.get_cache_stats()["cached_files"])),
        ("Cache Size", f"{loader.get_cache_stats()['total_size']:,} bytes"),
    ]

    for prop, val in info_data:
        if prop == "":
            table.add_row("─" * 15, "─" * 20)
        else:
            table.add_row(prop, val)

    console.print(table)

    # Features panel
    features = """
• 5-level timeout hierarchy (100ms - 10s)
• Circuit breaker pattern for fault tolerance
• Smart task-based loading
• In-memory caching
• Graceful degradation
• 10 consolidated guideline chapters
• Plugin architecture (7 hooks)
    """
    console.print(Panel(features.strip(), title="Features", border_style="green"))


@app.command()
def validate(
    path: str = typer.Argument(".", help="Path to validate"),
    fix: bool = typer.Option(False, "--fix", help="Auto-fix issues"),
):
    """Validate knowledge base structure."""
    loader = get_loader()
    kb_path = Path(path) if path != "." else loader.kb_path

    console.print(
        Panel(f"Validating: {kb_path}", title="Validation", border_style="blue")
    )

    issues = []
    checks_passed = 0

    # Check required directories
    required_dirs = [
        "01_core",
        "02_guidelines",
        "03_frameworks",
        "04_practices",
        "05_tools",
        "06_templates",
        "07_scenarios",
        "08_archive",
    ]

    for dir_name in required_dirs:
        dir_path = kb_path / dir_name
        if dir_path.exists():
            console.print(f"[green]✓[/green] {dir_name}/")
            checks_passed += 1
        else:
            console.print(f"[red]✗[/red] {dir_name}/ [dim](missing)[/dim]")
            issues.append(f"Missing directory: {dir_name}")
            if fix:
                dir_path.mkdir(parents=True, exist_ok=True)
                console.print(f"  [yellow]→ Created {dir_name}/[/yellow]")

    # Check required files
    required_files = [
        "index.md",
        "01_core/principles.md",
        "01_core/quick_reference.md",
    ]

    for file_name in required_files:
        file_path = kb_path / file_name
        if file_path.exists():
            console.print(f"[green]✓[/green] {file_name}")
            checks_passed += 1
        else:
            console.print(f"[red]✗[/red] {file_name} [dim](missing)[/dim]")
            issues.append(f"Missing file: {file_name}")

    # Summary
    console.print()
    if issues:
        console.print(
            f"[yellow]⚠ {len(issues)} issues found, {checks_passed} checks passed[/yellow]"
        )
        if fix:
            console.print("[green]Auto-fix applied where possible[/green]")
    else:
        console.print(f"[green]✓ All {checks_passed} checks passed[/green]")


@app.command()
def serve(
    host: str = typer.Option("localhost", "--host", "-h", help="Host to bind to"),
    port: int = typer.Option(8000, "--port", "-p", help="Port to bind to"),
):
    """Start MCP server."""
    console.print(
        Panel(
            f"Starting MCP server on {host}:{port}",
            title="AI Collaboration KB Server",
            border_style="green",
        )
    )

    try:
        from .mcp_server import run_server

        run_server(host, port)
    except ImportError as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("[yellow]Install MCP with: pip install mcp[/yellow]")


@app.command()
def cache(
    action: str = typer.Argument("stats", help="Action: stats, clear"),
):
    """Manage the knowledge cache."""
    loader = get_loader()

    if action == "stats":
        stats = loader.get_cache_stats()
        table = Table(title="Cache Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        table.add_row("Cached Files", str(stats["cached_files"]))
        table.add_row("Total Size", f"{stats['total_size']:,} bytes")
        console.print(table)

    elif action == "clear":
        loader.clear_cache()
        console.print("[green]✓ Cache cleared[/green]")

    else:
        console.print(f"[red]Unknown action: {action}[/red]")
        console.print("Available actions: stats, clear")


@app.command()
def version():
    """Show version information."""
    console.print(
        Panel(
            """
[bold]AI Collaboration Knowledge Base[/bold]
Version: 2.0.0
Score: 100/100 🏆
Experts: 24 Level 5

[dim]Philosophy: 信达雅 · 术法道[/dim]
        """.strip(),
            title="aikb",
            border_style="blue",
        )
    )


# ============================================================================
# Interactive Mode
# ============================================================================


@app.command()
def interactive():
    """Start interactive REPL mode."""
    console.print(
        Panel(
            "Interactive Mode - Type 'help' for commands, 'exit' to quit",
            title="AI Collaboration KB",
            border_style="green",
        )
    )

    loader = get_loader()

    commands_help = """
Available commands:
  get [layer]           - Get knowledge (0=core, 1=guidelines, 2=frameworks)
  search <query>        - Search knowledge base
  guidelines <section>  - Get specific guidelines section
  framework <name>      - Get framework documentation
  info                  - Show KB information
  cache                 - Show cache stats
  clear                 - Clear cache
  help                  - Show this help
  exit                  - Exit interactive mode
    """

    while True:
        try:
            cmd = console.input("[bold blue]aikb>[/bold blue] ").strip()

            if not cmd:
                continue

            parts = cmd.split(maxsplit=1)
            action = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            if action == "exit" or action == "quit":
                console.print("[dim]Goodbye![/dim]")
                break

            elif action == "help":
                console.print(commands_help)

            elif action == "get":
                layer = int(args) if args.isdigit() else 0
                result = run_async(
                    loader.load(
                        layer={
                            0: Layer.L1_CORE,
                            1: Layer.L2_GUIDELINES,
                            2: Layer.L3_FRAMEWORKS,
                        }.get(layer, Layer.L1_CORE)
                    )
                )
                display_result(result)

            elif action == "search":
                if not args:
                    console.print("[yellow]Usage: search <query>[/yellow]")
                else:
                    results = run_async(loader.search(args, max_results=5))
                    for r in results:
                        console.print(f"[cyan]{r['score']}[/cyan] {r['path']}")

            elif action == "guidelines":
                section = args or "overview"
                result = run_async(loader.load_guidelines(section))
                display_result(result)

            elif action == "framework":
                if not args:
                    console.print("[yellow]Usage: framework <name>[/yellow]")
                else:
                    result = run_async(loader.load_framework(args))
                    display_result(result)

            elif action == "info":
                info()

            elif action == "cache":
                stats = loader.get_cache_stats()
                console.print(
                    f"Cached: {stats['cached_files']} files, {stats['total_size']:,} bytes"
                )

            elif action == "clear":
                loader.clear_cache()
                console.print("[green]Cache cleared[/green]")

            else:
                console.print(
                    f"[yellow]Unknown command: {action}. Type 'help' for commands.[/yellow]"
                )

        except KeyboardInterrupt:
            console.print("\n[dim]Use 'exit' to quit[/dim]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


# ============================================================================
# Entry Point
# ============================================================================


def main():
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
