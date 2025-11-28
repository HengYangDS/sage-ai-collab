"""
MCP Server - Model Context Protocol service for AI Collaboration Knowledge Base.

This module provides:
- MCP tools for knowledge access with timeout protection
- Smart loading based on task description
- Search functionality
- Template retrieval
- Health monitoring

Author: AI Collaboration KB Team
Version: 2.0.0
"""

import logging
import time
from pathlib import Path
from typing import Any

# MCP imports
try:
    from mcp.server.fastmcp import FastMCP

    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    FastMCP = None

# Local imports
from .loader import (
    KnowledgeLoader,
    Layer,
)

logger = logging.getLogger(__name__)

# Initialize MCP app
if MCP_AVAILABLE:
    try:
        app = FastMCP(
            "ai-collab-kb",
            description="AI Collaboration Knowledge Base - Production-grade knowledge management with timeout protection",
        )
    except TypeError:
        # Fallback for older MCP versions without description parameter
        try:
            app = FastMCP("ai-collab-kb")
        except Exception as e:
            logger.warning(f"Failed to initialize MCP app: {e}")
            app = None
            MCP_AVAILABLE = False
else:
    app = None
    logger.warning("MCP not available. Install with: pip install mcp")


# Global loader instance
_loader: KnowledgeLoader | None = None


def get_loader() -> KnowledgeLoader:
    """Get or create the global knowledge loader."""
    global _loader
    if _loader is None:
        _loader = KnowledgeLoader()
    return _loader


# ============================================================================
# MCP Tools
# ============================================================================

if MCP_AVAILABLE and app is not None:

    @app.tool()
    async def get_knowledge(
        layer: int = 0,
        task: str = "",
        timeout_ms: int = 5000,
    ) -> dict[str, Any]:
        """
        Get AI collaboration knowledge with timeout guarantee.

        Args:
            layer: Knowledge layer (0=core, 1=guidelines, 2=frameworks, 3=practices)
            task: Task description for smart loading (e.g., "implement authentication")
            timeout_ms: Maximum time in milliseconds (default: 5000)

        Returns:
            Dictionary with:
            - content: Knowledge content (markdown)
            - tokens: Estimated token count
            - status: "success", "partial", or "fallback"
            - complete: Whether all requested content was loaded
            - duration_ms: Actual loading time
            - files_loaded: List of loaded files

        Examples:
            - get_knowledge(layer=0) -> Core principles only
            - get_knowledge(task="fix bug") -> Code-related guidelines
            - get_knowledge(task="design architecture") -> Design guidelines + frameworks
        """
        start_time = time.time()
        loader = get_loader()

        try:
            # Map layer number to Layer enum
            layer_map = {
                0: Layer.L1_CORE,
                1: Layer.L2_GUIDELINES,
                2: Layer.L3_FRAMEWORKS,
                3: Layer.L4_PRACTICES,
            }
            layer_enum = layer_map.get(layer)

            # Load knowledge
            if task:
                result = await loader.load_for_task(task, timeout_ms=timeout_ms)
            elif layer_enum:
                result = await loader.load(layer=layer_enum, timeout_ms=timeout_ms)
            else:
                result = await loader.load_core(timeout_ms=timeout_ms)

            return {
                "content": result.content,
                "tokens": result.tokens_estimate,
                "status": result.status,
                "complete": result.complete,
                "duration_ms": int((time.time() - start_time) * 1000),
                "timeout_ms": timeout_ms,
                "files_loaded": result.files_loaded,
                "layers": [l.name for l in result.layers_loaded],
            }

        except Exception as e:
            logger.error(f"Error in get_knowledge: {e}")
            return {
                "content": "Error loading knowledge. Using emergency fallback.",
                "tokens": 100,
                "status": "error",
                "complete": False,
                "duration_ms": int((time.time() - start_time) * 1000),
                "timeout_ms": timeout_ms,
                "error": str(e),
            }

    @app.tool()
    async def get_guidelines(
        section: str = "overview",
        timeout_ms: int = 3000,
    ) -> dict[str, Any]:
        """
        Get engineering guidelines by section.

        Args:
            section: Section name or keyword. Options:
                - "quick_start" or "00" - 3-minute primer
                - "planning" or "01" - Planning & Architecture
                - "code_style" or "02" - Code style standards
                - "engineering" or "03" - Config/Test/Perf/Change/Maintain
                - "documentation" or "04" - Documentation standards
                - "python" or "05" - Python + Decorators
                - "ai_collaboration" or "06" - AI collaboration + autonomy
                - "cognitive" or "07" - Cognitive enhancement
                - "quality" or "08" - Quality framework
                - "success" or "09" - Success principles
            timeout_ms: Maximum time in milliseconds (default: 3000)

        Returns:
            Dictionary with content, tokens, status, and metadata
        """
        start_time = time.time()
        loader = get_loader()

        # Map section names to file names
        section_map = {
            "quick_start": "00_quick_start",
            "00": "00_quick_start",
            "planning": "01_planning_design",
            "01": "01_planning_design",
            "code_style": "02_code_style",
            "02": "02_code_style",
            "engineering": "03_engineering",
            "03": "03_engineering",
            "documentation": "04_documentation",
            "04": "04_documentation",
            "python": "05_python",
            "05": "05_python",
            "ai_collaboration": "06_ai_collaboration",
            "06": "06_ai_collaboration",
            "cognitive": "07_cognitive",
            "07": "07_cognitive",
            "quality": "08_quality",
            "08": "08_quality",
            "success": "09_success",
            "09": "09_success",
            "overview": "00_quick_start",
        }

        chapter = section_map.get(section.lower(), section)

        try:
            result = await loader.load_guidelines(chapter, timeout_ms=timeout_ms)

            return {
                "content": result.content,
                "tokens": result.tokens_estimate,
                "status": result.status,
                "section": chapter,
                "duration_ms": int((time.time() - start_time) * 1000),
                "timeout_ms": timeout_ms,
            }

        except Exception as e:
            logger.error(f"Error in get_guidelines: {e}")
            return {
                "content": f"Error loading section '{section}'.",
                "tokens": 10,
                "status": "error",
                "error": str(e),
            }

    @app.tool()
    async def get_framework(
        name: str,
        timeout_ms: int = 5000,
    ) -> dict[str, Any]:
        """
        Get framework documentation.

        Args:
            name: Framework name. Options:
                - "autonomy" - 6-level autonomy spectrum
                - "cognitive" - CoT, expert committee, iteration
                - "decision" - Quality angles, expert roles
                - "collaboration" - Patterns, instruction engineering
                - "timeout" - Timeout principles and strategies
            timeout_ms: Maximum time in milliseconds (default: 5000)

        Returns:
            Dictionary with content, tokens, status, and metadata
        """
        start_time = time.time()
        loader = get_loader()

        try:
            result = await loader.load_framework(name, timeout_ms=timeout_ms)

            return {
                "content": result.content,
                "tokens": result.tokens_estimate,
                "status": result.status,
                "framework": name,
                "files_loaded": result.files_loaded,
                "duration_ms": int((time.time() - start_time) * 1000),
                "timeout_ms": timeout_ms,
            }

        except Exception as e:
            logger.error(f"Error in get_framework: {e}")
            return {
                "content": f"Error loading framework '{name}'.",
                "tokens": 10,
                "status": "error",
                "error": str(e),
            }

    @app.tool()
    async def search_kb(
        query: str,
        max_results: int = 5,
        timeout_ms: int = 3000,
    ) -> dict[str, Any]:
        """
        Search the knowledge base.

        Args:
            query: Search query (e.g., "autonomy levels", "testing strategy")
            max_results: Maximum number of results (default: 5, max: 20)
            timeout_ms: Maximum time in milliseconds (default: 3000)

        Returns:
            Dictionary with:
            - results: List of matches with path, score, and preview
            - count: Number of results found
            - query: Original query
            - duration_ms: Search time
        """
        start_time = time.time()
        loader = get_loader()

        # Limit max results
        max_results = min(max_results, 20)

        try:
            results = await loader.search(
                query,
                max_results=max_results,
                timeout_ms=timeout_ms,
            )

            return {
                "results": results,
                "count": len(results),
                "query": query,
                "duration_ms": int((time.time() - start_time) * 1000),
                "timeout_ms": timeout_ms,
            }

        except Exception as e:
            logger.error(f"Error in search_kb: {e}")
            return {
                "results": [],
                "count": 0,
                "query": query,
                "status": "error",
                "error": str(e),
            }

    @app.tool()
    async def get_template(
        name: str,
    ) -> dict[str, Any]:
        """
        Get a template from the knowledge base.

        Args:
            name: Template name. Options:
                - "project_guidelines" - Project-specific guidelines template
                - "session_log" - Session logging template
                - "delivery_report" - Delivery report template
                - "expert_committee" - Expert committee template
                - "health_check" - Health check template

        Returns:
            Dictionary with template content and metadata
        """
        loader = get_loader()
        template_path = f"06_templates/{name}.md"

        try:
            result = await loader.load(
                files=[template_path],
                timeout_ms=2000,
            )

            if result.status == "error" or not result.content:
                # Return a basic template structure
                return {
                    "content": f"# {name.replace('_', ' ').title()}\n\n[Template not found. Create at {template_path}]",
                    "status": "not_found",
                    "template": name,
                }

            return {
                "content": result.content,
                "status": "success",
                "template": name,
                "tokens": result.tokens_estimate,
            }

        except Exception as e:
            logger.error(f"Error in get_template: {e}")
            return {
                "content": "",
                "status": "error",
                "error": str(e),
            }

    @app.tool()
    async def kb_info() -> dict[str, Any]:
        """
        Get information about the knowledge base.

        Returns:
            Dictionary with:
            - version: KB version
            - layers: Available layers
            - guidelines_chapters: Available guideline chapters
            - frameworks: Available frameworks
            - cache_stats: Current cache statistics
            - timeout_config: Current timeout configuration
        """
        loader = get_loader()

        # Count files in each layer
        kb_path = loader.kb_path

        def count_md_files(path: Path) -> int:
            if not path.exists():
                return 0
            return len(list(path.glob("*.md")))

        return {
            "version": "2.0.0",
            "status": "operational",
            "layers": {
                "L0_INDEX": "Navigation index",
                "L1_CORE": "Core principles",
                "L2_GUIDELINES": "Engineering guidelines (10 chapters)",
                "L3_FRAMEWORKS": "Deep frameworks",
                "L4_PRACTICES": "Best practices",
            },
            "content_stats": {
                "core_files": count_md_files(kb_path / "01_core"),
                "guidelines_files": count_md_files(kb_path / "02_guidelines"),
                "frameworks_dirs": (
                    len(list((kb_path / "03_frameworks").glob("*")))
                    if (kb_path / "03_frameworks").exists()
                    else 0
                ),
                "practices_dirs": (
                    len(list((kb_path / "04_practices").glob("*")))
                    if (kb_path / "04_practices").exists()
                    else 0
                ),
                "templates": count_md_files(kb_path / "06_templates"),
            },
            "timeout_config": {
                "cache_ms": 100,
                "file_ms": 500,
                "layer_ms": 2000,
                "full_ms": 5000,
                "analysis_ms": 10000,
            },
            "cache_stats": loader.get_cache_stats(),
            "features": [
                "5-level timeout hierarchy",
                "Circuit breaker pattern",
                "Smart task-based loading",
                "In-memory caching",
                "Graceful degradation",
            ],
        }


# ============================================================================
# Runtime Capabilities (from capabilities/ module)
# ============================================================================

# Import capabilities directly (Plan D architecture)
from .capabilities import (
    ContentAnalyzer,
    HealthMonitor,
    LinkChecker,
    QualityAnalyzer,
    StructureChecker,
)

if MCP_AVAILABLE and app is not None:

    @app.tool()
    async def analyze_quality(
        path: str = ".",
        extensions: str = "",
    ) -> dict[str, Any]:
        """
        Analyze code or document quality, returning a score (0-100) and grade (A-F).

        Supports Python (.py) and Markdown (.md) files.

        Args:
            path: Path to file or directory to analyze (default: current directory)
            extensions: Comma-separated file extensions to include (e.g., ".py,.md")

        Returns:
            Dictionary with:
            - overall: Quality score (0-100)
            - grade: Letter grade (A-F)
            - metrics: Detailed quality metrics

        Examples:
            - analyze_quality(path="src/ai_collab_kb/loader.py")
            - analyze_quality(path="content", extensions=".md")
        """
        try:
            analyzer = QualityAnalyzer()
            target_path = Path(path)
            ext_list = [e.strip() for e in extensions.split(",") if e.strip()] or None

            if target_path.is_file():
                score = analyzer.analyze_file(target_path)
                return {
                    "success": True,
                    "result": (
                        score.to_dict()
                        if score
                        else {"error": "Could not analyze file"}
                    ),
                }
            else:
                results = analyzer.analyze_directory(target_path, extensions=ext_list)
                return {
                    "success": True,
                    "result": {
                        "files_analyzed": len(results),
                        "results": [r.to_dict() for r in results if r],
                    },
                }
        except Exception as e:
            logger.error(f"Error in analyze_quality: {e}")
            return {"success": False, "error": str(e)}

    @app.tool()
    async def analyze_content(
        path: str = ".",
        extensions: str = ".md",
    ) -> dict[str, Any]:
        """
        Analyze content metrics including token count, line count, and structure.

        Useful for understanding content size and complexity.

        Args:
            path: Path to file or directory to analyze
            extensions: Comma-separated file extensions (default: ".md")

        Returns:
            Dictionary with:
            - tokens: Estimated token count
            - lines: Line count
            - sections: Number of sections
            - efficiency_score: Content efficiency metric

        Examples:
            - analyze_content(path="content/core/principles.md")
            - analyze_content(path="content")
        """
        try:
            analyzer = ContentAnalyzer()
            target_path = Path(path)
            ext_list = [e.strip() for e in extensions.split(",") if e.strip()] or [
                ".md"
            ]

            if target_path.is_file():
                metrics = analyzer.analyze_file(target_path)
                return {
                    "success": True,
                    "result": (
                        metrics.to_dict()
                        if metrics
                        else {"error": "Could not analyze file"}
                    ),
                }
            else:
                results = analyzer.analyze_directory(target_path, extensions=ext_list)
                summary = analyzer.get_summary(
                    list(results.values()) if isinstance(results, dict) else results
                )
                return {"success": True, "result": summary}
        except Exception as e:
            logger.error(f"Error in analyze_content: {e}")
            return {"success": False, "error": str(e)}

    @app.tool()
    async def build_knowledge_graph(
        path: str = ".",
        include_content: bool = False,
        output_file: str = "",
    ) -> dict[str, Any]:
        """
        Build a knowledge graph showing relationships between files and concepts.

        Args:
            path: Root path of knowledge base
            include_content: Whether to include content in nodes
            output_file: Optional path to export graph as JSON

        Returns:
            Dictionary with:
            - total_nodes: Number of nodes in graph
            - total_edges: Number of relationships
            - node_types: Breakdown by node type
            - edge_types: Breakdown by relationship type

        Examples:
            - build_knowledge_graph(path="content")
            - build_knowledge_graph(output_file="graph.json")
        """
        try:
            # Dev tool: import from tools/ directory
            import sys

            tools_path = Path(__file__).parent.parent.parent.parent / "tools"
            if str(tools_path) not in sys.path:
                sys.path.insert(0, str(tools_path))
            from tools.knowledge_graph.knowledge_graph_builder import (
                KnowledgeGraphBuilder,
            )

            builder = KnowledgeGraphBuilder(kb_path=Path(path))
            graph = builder.build_from_directory(include_content=include_content)

            if output_file:
                builder.export_to_json(Path(output_file))

            return {"success": True, "result": builder.get_statistics()}
        except Exception as e:
            logger.error(f"Error in build_knowledge_graph: {e}")
            return {"success": False, "error": str(e)}

    @app.tool()
    async def check_links(
        path: str = ".",
        check_external: bool = False,
        pattern: str = "**/*.md",
    ) -> dict[str, Any]:
        """
        Check all links in Markdown files for validity.

        Detects broken internal links, invalid anchors, and optionally external URLs.

        Args:
            path: Root path to check
            check_external: Whether to also check external URLs (slower)
            pattern: Glob pattern for files to check

        Returns:
            Dictionary with:
            - total_links: Total number of links found
            - broken_links: List of broken links with details
            - broken_rate: Percentage of broken links

        Examples:
            - check_links(path="docs")
            - check_links(check_external=True)
        """
        try:
            checker = LinkChecker(kb_path=Path(path), check_external=check_external)
            report = checker.check_all(pattern=pattern)
            return {"success": True, "result": report.to_dict()}
        except Exception as e:
            logger.error(f"Error in check_links: {e}")
            return {"success": False, "error": str(e)}

    @app.tool()
    async def check_structure(
        path: str = ".",
        fix: bool = False,
        dry_run: bool = True,
    ) -> dict[str, Any]:
        """
        Validate project directory structure against expected conventions.

        Checks for required directories, files, and naming conventions.

        Args:
            path: Root path to check
            fix: Whether to attempt fixing issues
            dry_run: If fix=True, preview changes without applying

        Returns:
            Dictionary with:
            - issues: List of structural issues found
            - error_count: Number of errors
            - warning_count: Number of warnings

        Examples:
            - check_structure()
            - check_structure(fix=True, dry_run=True)
        """
        try:
            checker = StructureChecker(root_path=Path(path))
            report = checker.check()

            if fix:
                checker.fix_issues(report, dry_run=dry_run)

            return {"success": True, "result": report.to_dict()}
        except Exception as e:
            logger.error(f"Error in check_structure: {e}")
            return {"success": False, "error": str(e)}

    @app.tool()
    async def check_health(
        path: str = ".",
    ) -> dict[str, Any]:
        """
        Check overall health of the knowledge base system.

        Validates filesystem, configuration, and loader functionality.

        Args:
            path: Root path of knowledge base

        Returns:
            Dictionary with:
            - status: Overall status (HEALTHY, DEGRADED, UNHEALTHY)
            - checks: Individual check results
            - timestamp: Check timestamp

        Examples:
            - check_health()
            - check_health(path="/path/to/kb")
        """
        try:
            monitor = HealthMonitor(kb_path=Path(path))
            report = await monitor.check_all()
            return {"success": True, "result": report.to_dict()}
        except Exception as e:
            logger.error(f"Error in check_health: {e}")
            return {"success": False, "error": str(e)}

    @app.tool()
    async def get_timeout_stats(
        minutes: int = 60,
    ) -> dict[str, Any]:
        """
        Get timeout statistics and performance metrics.

        Shows timeout rates, near-timeout rates, and optimization recommendations.

        Args:
            minutes: Time window in minutes to analyze (default: 60)

        Returns:
            Dictionary with:
            - timeout_rate: Percentage of timed-out operations
            - near_timeout_rate: Percentage of operations near timeout
            - recommendations: List of optimization suggestions

        Examples:
            - get_timeout_stats()
            - get_timeout_stats(minutes=30)
        """
        try:
            # Dev tool: import from tools/ directory
            import sys

            tools_path = Path(__file__).parent.parent.parent.parent / "tools"
            if str(tools_path) not in sys.path:
                sys.path.insert(0, str(tools_path))
            from tools.monitors.timeout_monitor import get_timeout_monitor

            monitor = get_timeout_monitor()
            stats = monitor.get_stats(minutes=minutes)
            recommendations = monitor.get_recommendations()
            return {
                "success": True,
                "result": {**stats.to_dict(), "recommendations": recommendations},
            }
        except Exception as e:
            logger.error(f"Error in get_timeout_stats: {e}")
            return {"success": False, "error": str(e)}

    @app.tool()
    async def create_backup(
        path: str = ".",
        name: str = "",
    ) -> dict[str, Any]:
        """
        Create a backup of the knowledge base before making changes.

        Backups can be restored if needed using the migration toolkit.

        Args:
            path: Root path to backup
            name: Optional backup name/label for identification

        Returns:
            Dictionary with:
            - success: Whether backup was created
            - backup_path: Path to the created backup
            - timestamp: Backup creation time

        Examples:
            - create_backup(name="before_migration")
            - create_backup(path="content", name="content_backup")
        """
        try:
            # Dev tool: import from tools/ directory
            import sys

            tools_path = Path(__file__).parent.parent.parent.parent / "tools"
            if str(tools_path) not in sys.path:
                sys.path.insert(0, str(tools_path))
            from tools.migration_toolkit import MigrationToolkit

            toolkit = MigrationToolkit(kb_path=Path(path))
            backup_path = toolkit.create_backup(name=name)
            return {
                "success": True,
                "result": {"backup_path": str(backup_path), "name": name or "auto"},
            }
        except Exception as e:
            logger.error(f"Error in create_backup: {e}")
            return {"success": False, "error": str(e)}

    @app.tool()
    async def list_backups(
        path: str = ".backups",
    ) -> dict[str, Any]:
        """
        List all available backups with their timestamps and sizes.

        Args:
            path: Directory containing backups (default: .backups)

        Returns:
            Dictionary with:
            - backups: List of backup info (name, timestamp, size)
            - total_count: Number of backups
            - total_size: Combined size of all backups

        Examples:
            - list_backups()
            - list_backups(path="/custom/backup/dir")
        """
        try:
            # Dev tool: import from tools/ directory
            import sys

            tools_path = Path(__file__).parent.parent.parent.parent / "tools"
            if str(tools_path) not in sys.path:
                sys.path.insert(0, str(tools_path))
            from tools.migration_toolkit import MigrationToolkit

            toolkit = MigrationToolkit(backup_dir=Path(path))
            backups = toolkit.list_backups()
            return {
                "success": True,
                "result": {"backups": backups, "count": len(backups)},
            }
        except Exception as e:
            logger.error(f"Error in list_backups: {e}")
            return {"success": False, "error": str(e)}

    @app.tool()
    async def list_tools() -> dict[str, Any]:
        """
        List all available MCP tools organized by category.

        Tools are organized into two categories:
        - Runtime Capabilities: Core analysis and monitoring (from capabilities/)
        - Dev Tools: Development utilities (from tools/)

        Returns:
            Dictionary with:
            - capabilities: Runtime capability tools
            - dev_tools: Development-only tools
            - knowledge_tools: Knowledge access tools

        Examples:
            - list_tools()
        """
        return {
            "success": True,
            "knowledge_tools": [
                {
                    "name": "get_knowledge",
                    "description": "Get AI collaboration knowledge with timeout guarantee",
                },
                {
                    "name": "get_guidelines",
                    "description": "Get engineering guidelines by section",
                },
                {"name": "get_framework", "description": "Get framework documentation"},
                {"name": "search_kb", "description": "Search the knowledge base"},
                {
                    "name": "get_template",
                    "description": "Get a template from the knowledge base",
                },
                {
                    "name": "kb_info",
                    "description": "Get information about the knowledge base",
                },
            ],
            "capabilities": [
                {
                    "name": "analyze_quality",
                    "description": "Analyze code or document quality (0-100 score)",
                },
                {
                    "name": "analyze_content",
                    "description": "Analyze content metrics (tokens, lines, structure)",
                },
                {
                    "name": "check_links",
                    "description": "Check all links in Markdown files for validity",
                },
                {
                    "name": "check_structure",
                    "description": "Validate project directory structure",
                },
                {
                    "name": "check_health",
                    "description": "Check overall health of the knowledge base",
                },
            ],
            "dev_tools": [
                {
                    "name": "build_knowledge_graph",
                    "description": "Build a knowledge graph from files",
                },
                {
                    "name": "get_timeout_stats",
                    "description": "Get timeout statistics and performance metrics",
                },
                {
                    "name": "create_backup",
                    "description": "Create a backup of the knowledge base",
                },
                {"name": "list_backups", "description": "List all available backups"},
            ],
        }


# ============================================================================
# Server Management
# ============================================================================


def create_app() -> Any:
    """Create and configure the MCP application."""
    if not MCP_AVAILABLE:
        raise ImportError("MCP not available. Install with: pip install mcp")
    return app


def run_server(host: str = "localhost", port: int = 8000) -> None:
    """Run the MCP server."""
    if not MCP_AVAILABLE:
        raise ImportError("MCP not available. Install with: pip install mcp")

    logger.info(f"Starting AI Collaboration KB MCP server on {host}:{port}")
    # Note: Actual server startup depends on MCP framework version
    # This is a placeholder for the actual implementation
    print(f"MCP Server ready at {host}:{port}")
    print("\nKnowledge Tools:")
    print(
        "  get_knowledge, get_guidelines, get_framework, search_kb, get_template, kb_info"
    )
    print("\nRuntime Capabilities (from capabilities/):")
    print(
        "  analyze_quality, analyze_content, check_links, check_structure, check_health"
    )
    print("\nDev Tools (from tools/):")
    print("  build_knowledge_graph, get_timeout_stats, create_backup, list_backups")
    print("\nMeta:")
    print("  list_tools")


# ============================================================================
# CLI Entry Point
# ============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AI Collaboration KB MCP Server")
    parser.add_argument("--host", default="localhost", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    run_server(args.host, args.port)
