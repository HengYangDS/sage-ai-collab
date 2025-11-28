"""
Test Configuration - Global pytest fixtures.

This module provides shared fixtures for all tests following the mock strategy:

Mock Principles:
1. Mock at boundaries (I/O, network, filesystem)
2. Never mock the code under test
3. Use dependency injection for testability
4. Prefer fakes over mocks for complex behavior

What to Mock vs What to Use Real:
- Always Mock: File system operations (use tmp_path), network calls, time-dependent operations
- Never Mock: The class/function under test, pure data transformations, internal business logic
- Use Real (Isolated): In-memory databases, real DI container with test implementations

Author: SAGE AI Collab Team
Version: 0.1.0
"""

import asyncio
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest


# ============================================================================
# Configuration Fixtures
# ============================================================================


@pytest.fixture
def mock_config() -> MagicMock:
    """Mock configuration for unit tests."""
    config = MagicMock()
    config.timeout_ms = 5000
    config.layers = ["core", "guidelines"]
    config.debug = True
    config.content_root = Path("content")
    return config


@pytest.fixture
def timeout_config() -> dict[str, Any]:
    """Timeout configuration for tests."""
    return {
        "cache_ms": 100,
        "file_ms": 500,
        "layer_ms": 2000,
        "full_ms": 5000,
        "analysis_ms": 10000,
    }


# ============================================================================
# Loader Fixtures
# ============================================================================


@pytest.fixture
def mock_loader() -> AsyncMock:
    """Mock loader that returns predictable content."""
    from sage.core.loader import LoadResult, Layer

    loader = AsyncMock()
    loader.load.return_value = LoadResult(
        content="# Mock Content\nTest principles for testing.",
        layers_loaded=[Layer.L1_CORE],
        files_loaded=["content/core/principles.md"],
        tokens_estimate=10,
        duration_ms=50,
        complete=True,
        status="success",
        errors=[],
    )
    loader.load_core.return_value = LoadResult(
        content="# Core Principles\nBe accurate. Be clear. Be elegant.",
        layers_loaded=[Layer.L1_CORE],
        files_loaded=["content/core/principles.md"],
        tokens_estimate=15,
        duration_ms=30,
        complete=True,
        status="success",
        errors=[],
    )
    loader.search.return_value = [
        {
            "path": "content/core/principles.md",
            "score": 0.95,
            "preview": "Test preview...",
            "layer": "L1_CORE",
        }
    ]
    loader.get_cache_stats.return_value = {"cached_files": 0, "total_size": 0}
    return loader


@pytest.fixture
def real_loader():
    """Real loader instance for integration tests."""
    from sage.core.loader import KnowledgeLoader

    return KnowledgeLoader()


# ============================================================================
# Content Fixtures
# ============================================================================


@pytest.fixture
def temp_content_dir(tmp_path: Path) -> Path:
    """Temporary content directory with sample files."""
    content = tmp_path / "content"
    content.mkdir()

    # Create core directory with sample content
    core = content / "core"
    core.mkdir()
    (core / "principles.md").write_text(
        "# Test Principles\n\n"
        "## 信达雅 (Xin-Da-Ya)\n"
        "- **信**: Be accurate and reliable\n"
        "- **达**: Be clear and accessible\n"
        "- **雅**: Be refined and sustainable\n"
    )
    (core / "quick_reference.md").write_text(
        "# Quick Reference\n\n"
        "## Autonomy Levels\n"
        "- L1-L2: Ask before changes\n"
        "- L3-L4: Proceed and report\n"
        "- L5-L6: High autonomy\n"
    )

    # Create guidelines directory
    guidelines = content / "guidelines"
    guidelines.mkdir()
    (guidelines / "code_style.md").write_text(
        "# Code Style\n\n## Formatting\n- Line length: 88\n- Use ruff for formatting\n"
    )

    # Create index.md
    (content.parent / "index.md").write_text(
        "# SAGE Knowledge Base\n\nNavigation entry point.\n"
    )

    return content


@pytest.fixture
def sample_markdown_content() -> str:
    """Sample markdown content for testing."""
    return """# Test Document

## Section 1

This is test content for validation.

### Subsection 1.1

- Item 1
- Item 2
- Item 3

## Section 2

More content here.

```python
def example():
    return "test"
```
"""


# ============================================================================
# MCP/API Fixtures
# ============================================================================


@pytest.fixture
def mock_mcp_response() -> dict[str, Any]:
    """Mock MCP response for testing."""
    return {
        "content": "# Mock Knowledge\nTest content.",
        "tokens": 50,
        "status": "success",
        "duration_ms": 100,
        "layer": "core",
    }


@pytest.fixture
def mock_search_results() -> list[dict[str, Any]]:
    """Mock search results for testing."""
    return [
        {
            "path": "content/core/principles.md",
            "score": 0.95,
            "preview": "Be accurate and reliable...",
            "layer": "L1_CORE",
        },
        {
            "path": "content/guidelines/code_style.md",
            "score": 0.72,
            "preview": "Code style standards...",
            "layer": "L2_GUIDELINES",
        },
    ]


# ============================================================================
# Async Fixtures
# ============================================================================


@pytest.fixture
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# ============================================================================
# Marker Registration
# ============================================================================


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "e2e: mark test as an end-to-end test")
    config.addinivalue_line(
        "markers", "benchmark: mark test as a performance benchmark"
    )
    config.addinivalue_line("markers", "slow: mark test as slow running")
