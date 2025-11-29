"""HTTP REST API Server for SAGE Knowledge Base.

This module provides a FastAPI-based HTTP REST API for the SAGE
Knowledge Base system, enabling HTTP-based access to knowledge
content and capabilities.

Version: 0.1.0

Note: This is an optional service. FastAPI and Uvicorn must be
installed separately: `pip install fastapi uvicorn`
"""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from sage.core.exceptions import (
    ConfigError,
    ContentNotFoundError,
    SAGEError,
    TimeoutError as SAGETimeoutError,
)
from sage.core.loader import KnowledgeLoader, Layer
from sage.core.logging import get_logger

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from fastapi import FastAPI

__all__ = [
    "create_app",
    "run_server",
    "HTTPServerConfig",
]

logger = get_logger(__name__)


@dataclass
class HTTPServerConfig:
    """Configuration for HTTP server."""

    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = False
    reload: bool = False
    workers: int = 1
    cors_origins: list[str] | None = None
    api_prefix: str = "/api/v1"


def _check_fastapi_available() -> bool:
    """Check if FastAPI is available."""
    try:
        import fastapi  # noqa: F401
        return True
    except ImportError:
        return False


def create_app(config: HTTPServerConfig | None = None) -> FastAPI:
    """Create and configure the FastAPI application.

    Args:
        config: Optional server configuration.

    Returns:
        Configured FastAPI application.

    Raises:
        ConfigError: If FastAPI is not installed.
    """
    if not _check_fastapi_available():
        raise ConfigError(
            "FastAPI is not installed. Install with: pip install fastapi uvicorn"
        )

    from fastapi import FastAPI, HTTPException, Query, Request
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse

    config = config or HTTPServerConfig()

    # Initialize loader (uses default kb_path from project root)
    loader = KnowledgeLoader()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        """Application lifespan manager."""
        logger.info("Starting SAGE HTTP API server")
        yield
        logger.info("Shutting down SAGE HTTP API server")

    app = FastAPI(
        title="SAGE Knowledge Base API",
        description="HTTP REST API for SAGE Knowledge Base",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Configure CORS
    if config.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=config.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Exception handlers
    @app.exception_handler(SAGEError)
    async def sage_error_handler(
        request: Request, exc: SAGEError
    ) -> JSONResponse:
        """Handle SAGE-specific errors."""
        status_code = 500
        if isinstance(exc, ContentNotFoundError):
            status_code = 404
        elif isinstance(exc, ConfigError):
            status_code = 400
        elif isinstance(exc, SAGETimeoutError):
            status_code = 504

        return JSONResponse(
            status_code=status_code,
            content={
                "error": exc.__class__.__name__,
                "message": str(exc),
                "details": getattr(exc, "details", None),
            },
        )

    # Health check endpoint
    @app.get("/health")
    async def health_check() -> dict[str, Any]:
        """Check API health status.

        Returns:
            Health status information.
        """
        return {
            "status": "healthy",
            "version": "0.1.0",
            "service": "sage-kb-api",
        }

    # API routes
    prefix = config.api_prefix

    @app.get(f"{prefix}/info")
    async def get_info() -> dict[str, Any]:
        """Get knowledge base information.

        Returns:
            Knowledge base metadata and statistics.
        """
        return {
            "name": "SAGE Knowledge Base",
            "version": "0.1.0",
            "layers": ["core", "guidelines", "frameworks", "practices", "scenarios"],
        }

    # Layer name to enum mapping
    layer_mapping = {
        "index": Layer.L0_INDEX,
        "core": Layer.L1_CORE,
        "guidelines": Layer.L2_GUIDELINES,
        "frameworks": Layer.L3_FRAMEWORKS,
        "practices": Layer.L4_PRACTICES,
    }

    @app.get(f"{prefix}/knowledge")
    async def get_knowledge(
        layer: str = Query(default="core", description="Knowledge layer"),
    ) -> dict[str, Any]:
        """Get knowledge content.

        Args:
            layer: Knowledge layer to retrieve.

        Returns:
            Knowledge content and metadata.
        """
        try:
            # Map string to Layer enum
            layer_lower = layer.lower() if layer else "core"
            if layer_lower not in layer_mapping:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid layer: {layer}. Valid layers: {list(layer_mapping.keys())}"
                )
            layer_enum = layer_mapping[layer_lower]
            result = await asyncio.to_thread(
                loader.load, layer=layer_enum
            )
            return {
                "layer": layer,
                "content": result.content if result else "",
                "status": "success",
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    @app.get(f"{prefix}/search")
    async def search_knowledge(
        q: str = Query(description="Search query"),
        limit: int = Query(default=10, ge=1, le=100, description="Max results"),
    ) -> dict[str, Any]:
        """Search knowledge content.

        Args:
            q: Search query string.
            limit: Maximum number of results.

        Returns:
            Search results.
        """
        try:
            results = await asyncio.to_thread(
                loader.search, q, max_results=limit
            )
            return {
                "query": q,
                "limit": limit,
                "results": [r.to_dict() if hasattr(r, 'to_dict') else r for r in results],
                "count": len(results) if results else 0,
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    @app.get(f"{prefix}/layers")
    async def list_layers() -> dict[str, Any]:
        """List available knowledge layers.

        Returns:
            List of layers with descriptions.
        """
        return {
            "layers": [
                {
                    "name": "core",
                    "description": "Core principles and philosophy",
                    "priority": 1,
                },
                {
                    "name": "guidelines",
                    "description": "Engineering guidelines",
                    "priority": 2,
                },
                {
                    "name": "frameworks",
                    "description": "Deep frameworks",
                    "priority": 3,
                },
                {
                    "name": "practices",
                    "description": "Best practices",
                    "priority": 4,
                },
                {
                    "name": "scenarios",
                    "description": "Scenario presets",
                    "priority": 5,
                },
            ]
        }

    @app.get(f"{prefix}/frameworks/{{framework_name}}")
    async def get_framework(
        framework_name: str,
    ) -> dict[str, Any]:
        """Get a specific framework.

        Args:
            framework_name: Name of the framework.

        Returns:
            Framework content and metadata.
        """
        try:
            result = await asyncio.to_thread(
                loader.load_framework, framework_name
            )
            return {
                "framework": framework_name,
                "content": result.content if result else "",
                "status": "success",
            }
        except FileNotFoundError as e:
            raise HTTPException(
                status_code=404,
                detail=f"Framework not found: {framework_name}"
            ) from e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    # Analysis endpoints
    @app.post(f"{prefix}/analyze/quality")
    async def analyze_quality(
        path: str = Query(description="Path to file to analyze"),
    ) -> dict[str, Any]:
        """Analyze file quality.

        Args:
            path: Path to file to analyze.

        Returns:
            Quality analysis results.
        """
        from sage.capabilities.analyzers.quality import QualityAnalyzer

        analyzer = QualityAnalyzer()
        try:
            results = await asyncio.to_thread(
                analyzer.analyze_file, Path(path)
            )
            return {
                "analysis_type": "quality",
                "path": path,
                "results": results.to_dict() if hasattr(results, 'to_dict') else results,
            }
        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    @app.get(f"{prefix}/check/structure")
    async def check_structure() -> dict[str, Any]:
        """Check knowledge base structure.

        Returns:
            Structure check results.
        """
        from sage.capabilities.analyzers.structure import StructureChecker

        checker = StructureChecker()
        try:
            results = await asyncio.to_thread(checker.check)
            return {
                "check_type": "structure",
                "results": results.to_dict() if hasattr(results, 'to_dict') else results,
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    @app.get(f"{prefix}/check/links")
    async def check_links() -> dict[str, Any]:
        """Check links in knowledge base.

        Returns:
            Link check results.
        """
        from sage.capabilities.checkers.links import LinkChecker

        checker = LinkChecker()
        try:
            results = await asyncio.to_thread(checker.check_all)
            return {
                "check_type": "links",
                "results": results.to_dict() if hasattr(results, 'to_dict') else results,
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    @app.get(f"{prefix}/check/health")
    async def check_health() -> dict[str, Any]:
        """Check system health.

        Returns:
            Health check results.
        """
        from sage.capabilities.monitors.health import HealthMonitor

        monitor = HealthMonitor()
        try:
            results = await asyncio.to_thread(monitor.check_all)
            return {
                "check_type": "health",
                "results": results.to_dict() if hasattr(results, 'to_dict') else results,
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    return app


def run_server(config: HTTPServerConfig | None = None) -> None:
    """Run the HTTP server.

    Args:
        config: Optional server configuration.

    Raises:
        ConfigError: If uvicorn is not installed.
    """
    try:
        import uvicorn
    except ImportError as e:
        raise ConfigError(
            "Uvicorn is not installed. Install with: pip install uvicorn"
        ) from e

    config = config or HTTPServerConfig()
    app = create_app(config)

    logger.info(
        "Starting HTTP server",
        host=config.host,
        port=config.port,
    )

    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        reload=config.reload,
        workers=config.workers,
        log_level="debug" if config.debug else "info",
    )
