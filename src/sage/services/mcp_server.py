"""
MCP Server - Model Context Protocol service for AI Collaboration Knowledge Base.

This module provides:
- MCP tools for knowledge access with timeout protection
- Smart loading based on task description
- Search functionality
- Template retrieval
- Health monitoring

Author: SAGE AI Collab Team
Version: 0.1.0
"""

import time
from datetime import datetime
from pathlib import Path
from typing import Any

# MCP imports
try:
    from mcp.server.fastmcp import FastMCP

    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    FastMCP = None  # type: ignore[misc, assignment]

# Local imports
from sage.core.loader import (
    KnowledgeLoader,
    Layer,
)
from sage.core.logging import get_logger

# Configuration cache
_config_cache: dict[str, Any] | None = None


def _load_config() -> dict[str, Any]:
    """Load configuration using the unified config system.

    This function uses the config module's load_config() which supports:
    - Modular config files in config/ directory
    - Main sage.yaml configuration
    - Includes from sage.yaml
    - Environment variable overrides

    Returns:
        Merged configuration dictionary from all sources.
    """
    global _config_cache
    if _config_cache is not None:
        return _config_cache

    try:
        from sage.core.config import load_config as load_unified_config

        _config_cache = load_unified_config()
    except Exception:
        _config_cache = {}

    return _config_cache


def _get_guidelines_section_map() -> dict[str, str]:
    """Get guidelines section mapping from configuration."""
    config = _load_config()
    guidelines_config = config.get("guidelines", {})
    sections = guidelines_config.get("sections", {})

    # Convert all keys to lowercase strings for case-insensitive lookup
    return {str(k).lower(): str(v) for k, v in sections.items()}


def _parse_timeout_str(timeout_str: str | int) -> int:
    """
    Parse timeout string (e.g., '5s', '500ms', '2s') to milliseconds.

    Args:
        timeout_str: Timeout value as string (e.g., '5s', '500ms') or int (ms).

    Returns:
        Timeout in milliseconds.
    """
    if isinstance(timeout_str, int):
        return timeout_str

    timeout_str = str(timeout_str).strip().lower()

    if timeout_str.endswith("ms"):
        return int(timeout_str[:-2])
    elif timeout_str.endswith("s"):
        return int(float(timeout_str[:-1]) * 1000)
    else:
        # Assume milliseconds if no unit
        return int(timeout_str)


def _get_timeout_from_config(operation: str, default_ms: int) -> int:
    """
    Get timeout value for a specific operation from the sage.yaml configuration.

    Args:
        operation: Operation name (e.g., 'full_load', 'layer_load', 'file_read', 'search').
        default_ms: Default timeout in milliseconds if not found in config.

    Returns:
        Timeout in milliseconds.
    """
    config = _load_config()
    timeout_config = config.get("timeout", {})
    operations = timeout_config.get("operations", {})

    if operation in operations:
        return _parse_timeout_str(operations[operation])

    # Fallback to default timeout from config
    if "default" in timeout_config:
        return _parse_timeout_str(timeout_config["default"])

    return default_ms


def _get_timeout_config_dict() -> dict[str, int]:
    """
    Get the complete timeout configuration as a dictionary.

    Returns:
        Dictionary with timeout values in milliseconds.
    """
    config = _load_config()
    timeout_config = config.get("timeout", {})
    operations = timeout_config.get("operations", {})

    return {
        "cache_ms": _parse_timeout_str(operations.get("cache_lookup", 100)),
        "file_ms": _parse_timeout_str(operations.get("file_read", 500)),
        "layer_ms": _parse_timeout_str(operations.get("layer_load", 2000)),
        "full_ms": _parse_timeout_str(operations.get("full_load", 5000)),
        "analysis_ms": _parse_timeout_str(operations.get("analysis", 10000)),
    }


logger = get_logger(__name__)


def _get_mcp_metadata() -> tuple[str, str]:
    """Get MCP server name and description from configuration.

    Uses top-level Metadata from sage.yaml as Single Source of Truth.

    Returns:
        Tuple of (name, description).
    """
    config = _load_config()
    name = config.get("name", "sage-kb")
    description = config.get(
        "description", "SAGE Knowledge Base - Production-grade knowledge management"
    )
    return name, description


# Initialize MCP app
if MCP_AVAILABLE:
    _mcp_name, _mcp_description = _get_mcp_metadata()
    try:
        app = FastMCP(  # type: ignore[call-arg]
            _mcp_name,
            description=_mcp_description,
        )
        logger.debug("mcp_app_initialized", app_name=_mcp_name)
    except TypeError:
        # Fallback for older MCP versions without description parameter
        try:
            app = FastMCP(_mcp_name)
            logger.debug("mcp_app_initialized", app_name=_mcp_name, fallback=True)
        except Exception as e:
            logger.warning("mcp_init_failed", error=str(e))
            app = None  # type: ignore[assignment]
            MCP_AVAILABLE = False
else:
    app = None  # type: ignore[assignment]
    logger.warning("mcp_not_available", hint="Install with: pip install mcp")


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

        # Get section mapping from configuration
        section_map = _get_guidelines_section_map()

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
    async def search_knowledge(
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
            logger.error(f"Error in search_knowledge: {e}")
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
            "version": "0.1.0",
            "status": "operational",
            "layers": {
                "L0_INDEX": "Navigation index",
                "L1_CORE": "Core principles",
                "L2_GUIDELINES": "Engineering guidelines (10 chapters)",
                "L3_FRAMEWORKS": "Deep frameworks",
                "L4_PRACTICES": "Best practices",
            },
            "content_stats": {
                "core_files": count_md_files(kb_path / "content" / "core"),
                "guidelines_files": count_md_files(kb_path / "content" / "guidelines"),
                "frameworks_dirs": (
                    len(list((kb_path / "content" / "frameworks").glob("*")))
                    if (kb_path / "content" / "frameworks").exists()
                    else 0
                ),
                "practices_dirs": (
                    len(list((kb_path / "content" / "practices").glob("*")))
                    if (kb_path / "content" / "practices").exists()
                    else 0
                ),
                "templates": count_md_files(kb_path / "content" / "templates"),
            },
            "timeout_config": _get_timeout_config_dict(),
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
from sage.capabilities import (
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
            - analyze_quality(path="src/sage/core/loader.py")
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
            output_file: Optional filename to export graph as JSON (saved to .outputs/)

        Returns:
            Dictionary with:
            - total_nodes: Number of nodes in graph
            - total_edges: Number of relationships
            - node_types: Breakdown by node type
            - edge_types: Breakdown by relationship type

        Examples:
            - build_knowledge_graph(path="content")
            - build_knowledge_graph(output_file="graph.json")  # Saved to .outputs/graph.json
        """
        try:
            # Dev tool: import from tools/ directory
            import sys

            tools_path = Path(__file__).parent.parent.parent.parent / "tools"
            if str(tools_path) not in sys.path:
                sys.path.insert(0, str(tools_path))
            from tools.knowledge_graph.knowledge_graph_builder import (  # type: ignore[import-not-found]
                KnowledgeGraphBuilder,
            )

            builder = KnowledgeGraphBuilder(kb_path=Path(path))
            graph = builder.build_from_directory(include_content=include_content)

            if output_file:
                # Ensure output files go to .outputs/ directory
                project_root = Path(__file__).parent.parent.parent.parent
                outputs_dir = project_root / ".outputs"
                outputs_dir.mkdir(parents=True, exist_ok=True)

                # Use just the filename if a path is provided
                output_filename = Path(output_file).name
                output_path = outputs_dir / output_filename
                builder.export_to_json(output_path)

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
            from tools.monitors.timeout_monitor import (
                get_timeout_monitor,  # type: ignore[import-not-found]
            )

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
            from tools.migration_toolkit import (
                MigrationToolkit,  # type: ignore[import-not-found]
            )

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

    # ========================================================================
    # Session Management Tools
    # ========================================================================

    @app.tool()
    async def session_start(
        task: str,
        description: str = "",
        autonomy_level: str = "L4",
    ) -> dict[str, Any]:
        """
        Start a new AI collaboration session with tracking.

        Creates a session state file in .history/current/ to track the session.
        Call this at the beginning of significant work sessions.

        Args:
            task: Brief task name (e.g., "Implement authentication")
            description: Detailed description of the task objective
            autonomy_level: Autonomy level L1-L6 (default: L4)

        Returns:
            Dictionary with:
            - session_id: Unique session identifier
            - session_file: Path to session state file
            - started_at: Session start timestamp

        Examples:
            - session_start(task="Fix timeout bug", description="Resolve T2 timeout in loader")
            - session_start(task="Documentation update", autonomy_level="L5")
        """
        try:
            from datetime import datetime

            # Generate session ID
            now = datetime.now()
            session_id = f"session-{now.strftime('%Y%m%d-%H%M')}"

            # Determine project root and history path
            project_root = Path.cwd()
            history_current = project_root / ".history" / "current"
            history_current.mkdir(parents=True, exist_ok=True)

            session_file = history_current / f"{session_id}.md"

            # Create session state content
            content = f"""# Session State: {task}

> **Session ID**: {session_id}
> **Started**: {now.strftime('%Y-%m-%d %H:%M')}
> **Last Updated**: {now.strftime('%Y-%m-%d %H:%M')}
> **Status**: Active
> **Autonomy Level**: {autonomy_level}

---

## Current Task

### Objective

{description if description else task}

### Progress

- [ ] Task in progress

### Files Modified

| File | Changes | Status |
|------|---------|--------|
| (none yet) | | |

### Decisions

(No decisions recorded yet)

### Blockers

- None currently

---

## Quick Resume

To continue: Review objective and progress above, then proceed with task.

---

*Session state from SAGE Knowledge Base*
"""

            session_file.write_text(content, encoding="utf-8")
            logger.info("session_started", session_id=session_id, task=task)

            return {
                "success": True,
                "result": {
                    "session_id": session_id,
                    "session_file": str(session_file),
                    "started_at": now.isoformat(),
                    "task": task,
                    "autonomy_level": autonomy_level,
                },
            }
        except Exception as e:
            logger.error(f"Error in session_start: {e}")
            return {"success": False, "error": str(e)}

    @app.tool()
    async def session_end(
        summary: str,
        next_steps: str = "",
        record_type: str = "auto",
    ) -> dict[str, Any]:
        """
        End the current session and create appropriate records.

        Finalizes the active session, creates conversation record or handoff
        document based on session outcome.

        Args:
            summary: Brief summary of what was accomplished
            next_steps: Remaining tasks or follow-up items (triggers handoff if provided)
            record_type: "conversation", "handoff", or "auto" (auto-detect)

        Returns:
            Dictionary with:
            - session_id: Ended session ID
            - record_created: Type of record created
            - record_file: Path to created record

        Examples:
            - session_end(summary="Completed timeout refactoring")
            - session_end(summary="Partial completion", next_steps="Finish tests", record_type="handoff")
        """
        try:
            from datetime import datetime

            now = datetime.now()
            project_root = Path.cwd()
            history_current = project_root / ".history" / "current"

            # Find active session
            active_sessions = list(history_current.glob("session-*.md"))
            if not active_sessions:
                return {
                    "success": False,
                    "error": "No active session found in .history/current/",
                }

            # Use most recent session
            active_session = max(active_sessions, key=lambda p: p.stat().st_mtime)
            session_id = active_session.stem

            # Determine record type
            if record_type == "auto":
                record_type = "handoff" if next_steps else "conversation"

            # Create appropriate record
            if record_type == "handoff":
                record_dir = project_root / ".history" / "handoffs"
                record_dir.mkdir(parents=True, exist_ok=True)
                record_file = record_dir / f"{now.strftime('%Y-%m-%d')}-handoff.md"

                content = f"""# Task Handoff: {summary[:50]}

> **From**: {session_id}
> **Date**: {now.strftime('%Y-%m-%d')}
> **Status**: Partial completion

---

## Summary

{summary}

## Completed Work

(Refer to session for details)

## Pending Items

{next_steps}

## Recommended Next Steps

1. Review pending items above
2. Continue from where session left off

---

*Handoff from SAGE Knowledge Base*
"""
            else:
                record_dir = project_root / ".history" / "conversations"
                record_dir.mkdir(parents=True, exist_ok=True)
                record_file = record_dir / f"{now.strftime('%Y-%m-%d')}-session.md"

                content = f"""# Session Record: {summary[:50]}

> **Date**: {now.strftime('%Y-%m-%d')}
> **Session**: {session_id}
> **Status**: Completed

---

## Summary

{summary}

## Key Outcomes

(Add specific outcomes)

## Decisions Made

(Add decisions if any)

## Learnings

(Add learnings if any)

---

*Conversation record from SAGE Knowledge Base*
"""

            record_file.write_text(content, encoding="utf-8")

            # Archive the session state (move to indicate completion)
            active_session.unlink()

            logger.info("session_ended", session_id=session_id, record_type=record_type)

            return {
                "success": True,
                "result": {
                    "session_id": session_id,
                    "record_type": record_type,
                    "record_file": str(record_file),
                    "ended_at": now.isoformat(),
                    "summary": summary,
                },
            }
        except Exception as e:
            logger.error(f"Error in session_end: {e}")
            return {"success": False, "error": str(e)}

    @app.tool()
    async def session_status() -> dict[str, Any]:
        """
        Get current session status and active sessions.

        Checks .history/current/ for active sessions and returns their status.

        Returns:
            Dictionary with:
            - active: Whether there's an active session
            - sessions: List of active session details
            - recent_records: Recent conversation/handoff records

        Examples:
            - session_status()
        """
        try:
            project_root = Path.cwd()
            history_path = project_root / ".history"
            current_path = history_path / "current"
            conversations_path = history_path / "conversations"
            handoffs_path = history_path / "handoffs"

            # Get active sessions
            active_sessions = []
            if current_path.exists():
                for session_file in current_path.glob("session-*.md"):
                    stat = session_file.stat()
                    active_sessions.append(
                        {
                            "session_id": session_file.stem,
                            "file": str(session_file),
                            "modified": datetime.fromtimestamp(
                                stat.st_mtime
                            ).isoformat(),
                            "size_bytes": stat.st_size,
                        }
                    )

            # Get recent records (last 5)
            recent_records = []
            for record_path in [conversations_path, handoffs_path]:
                if record_path.exists():
                    for record_file in sorted(
                        record_path.glob("*.md"),
                        key=lambda p: p.stat().st_mtime,
                        reverse=True,
                    )[:5]:
                        if not record_file.name.startswith("_example"):
                            recent_records.append(
                                {
                                    "type": record_path.name,
                                    "file": record_file.name,
                                    "path": str(record_file),
                                }
                            )

            return {
                "success": True,
                "result": {
                    "active": len(active_sessions) > 0,
                    "active_count": len(active_sessions),
                    "sessions": active_sessions,
                    "recent_records": recent_records[:5],
                },
            }
        except Exception as e:
            logger.error(f"Error in session_status: {e}")
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
            "session_tools": [
                {
                    "name": "session_start",
                    "description": "Start a new AI collaboration session with tracking",
                },
                {
                    "name": "session_end",
                    "description": "End session and create conversation/handoff record",
                },
                {
                    "name": "session_status",
                    "description": "Get current session status and active sessions",
                },
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

    logger.info("mcp_server_starting", host=host, port=port)
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
    print("\nSession Tools:")
    print("  session_start, session_end, session_status")
    print("\nMeta:")
    print("  list_tools")


# ============================================================================
# CLI Entry Point
# ============================================================================

if __name__ == "__main__":
    import argparse

    from sage.core.logging import LogLevel, configure_logging

    parser = argparse.ArgumentParser(description="AI Collaboration KB MCP Server")
    parser.add_argument("--host", default="localhost", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    if args.debug:
        configure_logging(level=LogLevel.DEBUG)
    else:
        configure_logging(level=LogLevel.INFO)

    run_server(args.host, args.port)
