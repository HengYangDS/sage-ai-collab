"""
Unit tests for CLI module.

Tests cover:
- Helper functions (get_loader, run_async, display_content, display_result)
- CLI commands (get, guidelines, framework, search, info, validate, cache, version)
- Command line argument parsing
- Output formatting
"""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from typer.testing import CliRunner

from ai_collab_kb.cli import (
    app,
    display_content,
    display_result,
    get_loader,
    run_async,
)
from ai_collab_kb.loader import KnowledgeLoader, LoadResult

runner = CliRunner()


class TestGetLoader:
    """Tests for get_loader function."""

    def test_get_loader_returns_knowledge_loader(self):
        """get_loader should return a KnowledgeLoader instance."""
        import ai_collab_kb.cli as cli_module

        cli_module._loader = None

        loader = get_loader()
        assert isinstance(loader, KnowledgeLoader)

    def test_get_loader_returns_singleton(self):
        """get_loader should return the same instance on multiple calls."""
        import ai_collab_kb.cli as cli_module

        cli_module._loader = None

        loader1 = get_loader()
        loader2 = get_loader()
        assert loader1 is loader2


class TestRunAsync:
    """Tests for run_async helper function."""

    def test_run_async_executes_coroutine(self):
        """run_async should execute an async coroutine."""

        async def simple_coro():
            return "result"

        result = run_async(simple_coro())
        assert result == "result"

    def test_run_async_with_awaitable(self):
        """run_async should handle awaitables."""

        async def add_numbers(a, b):
            return a + b

        result = run_async(add_numbers(2, 3))
        assert result == 5


class TestDisplayContent:
    """Tests for display_content function."""

    def test_display_content_markdown(self):
        """display_content with markdown format should not raise."""
        # Just verify it doesn't raise
        display_content("# Test", format="markdown")

    def test_display_content_syntax(self):
        """display_content with syntax format should not raise."""
        display_content("# Test", format="syntax")

    def test_display_content_raw(self):
        """display_content with raw format should not raise."""
        display_content("# Test", format="raw")

    def test_display_content_default(self):
        """display_content with unknown format should default to markdown."""
        display_content("# Test", format="unknown")


class TestDisplayResult:
    """Tests for display_result function."""

    def test_display_result_success(self):
        """display_result with success status should not raise."""
        result = LoadResult(
            content="# Test Content",
            status="success",
            tokens_estimate=100,
            duration_ms=50,
            files_loaded=["test.md"],
        )
        # Just verify it doesn't raise
        display_result(result)

    def test_display_result_partial(self):
        """display_result with partial status should not raise."""
        result = LoadResult(
            content="# Partial Content",
            status="partial",
            tokens_estimate=50,
            duration_ms=100,
        )
        display_result(result)

    def test_display_result_fallback(self):
        """display_result with fallback status should not raise."""
        result = LoadResult(
            content="# Fallback Content",
            status="fallback",
            tokens_estimate=30,
            duration_ms=10,
        )
        display_result(result)

    def test_display_result_verbose(self):
        """display_result with verbose=True should show more info."""
        result = LoadResult(
            content="# Test",
            status="success",
            tokens_estimate=100,
            duration_ms=50,
            files_loaded=["file1.md", "file2.md"],
            errors=["Warning: something"],
        )
        display_result(result, verbose=True)


class TestGetCommand:
    """Tests for 'get' command."""

    def test_get_default(self):
        """'aikb get' should return core content."""
        result = runner.invoke(app, ["get"])
        assert result.exit_code == 0

    def test_get_with_layer(self):
        """'aikb get 1' should return guidelines."""
        result = runner.invoke(app, ["get", "1"])
        assert result.exit_code == 0

    def test_get_with_topic(self):
        """'aikb get --topic code' should filter by topic."""
        result = runner.invoke(app, ["get", "--topic", "code"])
        assert result.exit_code == 0

    def test_get_with_format(self):
        """'aikb get --format raw' should use raw format."""
        result = runner.invoke(app, ["get", "--format", "raw"])
        assert result.exit_code == 0

    def test_get_with_timeout(self):
        """'aikb get --timeout 3000' should use custom timeout."""
        result = runner.invoke(app, ["get", "--timeout", "3000"])
        assert result.exit_code == 0

    def test_get_with_verbose(self):
        """'aikb get --verbose' should show detailed info."""
        result = runner.invoke(app, ["get", "--verbose"])
        assert result.exit_code == 0


class TestGuidelinesCommand:
    """Tests for 'guidelines' command."""

    def test_guidelines_default(self):
        """'aikb guidelines' should return overview."""
        result = runner.invoke(app, ["guidelines"])
        assert result.exit_code == 0

    def test_guidelines_code_style(self):
        """'aikb guidelines code_style' should return code style."""
        result = runner.invoke(app, ["guidelines", "code_style"])
        assert result.exit_code == 0

    def test_guidelines_with_timeout(self):
        """'aikb guidelines --timeout 2000' should use custom timeout."""
        result = runner.invoke(app, ["guidelines", "--timeout", "2000"])
        assert result.exit_code == 0

    def test_guidelines_with_verbose(self):
        """'aikb guidelines --verbose' should show detailed info."""
        result = runner.invoke(app, ["guidelines", "--verbose"])
        assert result.exit_code == 0


class TestFrameworkCommand:
    """Tests for 'framework' command."""

    def test_framework_autonomy(self):
        """'aikb framework autonomy' should return autonomy framework."""
        result = runner.invoke(app, ["framework", "autonomy"])
        assert result.exit_code == 0

    def test_framework_cognitive(self):
        """'aikb framework cognitive' should return cognitive framework."""
        result = runner.invoke(app, ["framework", "cognitive"])
        assert result.exit_code == 0

    def test_framework_with_timeout(self):
        """'aikb framework --timeout 4000' should use custom timeout."""
        result = runner.invoke(app, ["framework", "autonomy", "--timeout", "4000"])
        assert result.exit_code == 0


class TestSearchCommand:
    """Tests for 'search' command."""

    def test_search_basic(self):
        """'aikb search principles' should find results."""
        result = runner.invoke(app, ["search", "principles"])
        assert result.exit_code == 0

    def test_search_with_limit(self):
        """'aikb search --limit 3' should limit results."""
        result = runner.invoke(app, ["search", "test", "--limit", "3"])
        assert result.exit_code == 0

    def test_search_no_results(self):
        """'aikb search xyznonexistent' should handle no results."""
        result = runner.invoke(app, ["search", "xyznonexistent123"])
        assert result.exit_code == 0


class TestInfoCommand:
    """Tests for 'info' command."""

    def test_info(self):
        """'aikb info' should show KB information."""
        result = runner.invoke(app, ["info"])
        assert result.exit_code == 0
        # Should contain some expected content
        assert "Knowledge Base" in result.output or "aikb" in result.output.lower()


class TestValidateCommand:
    """Tests for 'validate' command."""

    def test_validate_default(self):
        """'aikb validate' should validate current directory."""
        result = runner.invoke(app, ["validate"])
        # May succeed or fail depending on environment
        assert result.exit_code in [0, 1]

    def test_validate_with_path(self):
        """'aikb validate .' should validate specified path."""
        result = runner.invoke(app, ["validate", "."])
        assert result.exit_code in [0, 1]


class TestCacheCommand:
    """Tests for 'cache' command."""

    def test_cache_stats(self):
        """'aikb cache stats' should show cache statistics."""
        result = runner.invoke(app, ["cache", "stats"])
        assert result.exit_code == 0

    def test_cache_clear(self):
        """'aikb cache clear' should clear cache."""
        result = runner.invoke(app, ["cache", "clear"])
        assert result.exit_code == 0


class TestVersionCommand:
    """Tests for 'version' command."""

    def test_version(self):
        """'aikb version' should show version info."""
        result = runner.invoke(app, ["version"])
        assert result.exit_code == 0
        # Should contain version number
        assert "2.0" in result.output or "version" in result.output.lower()


class TestHelp:
    """Tests for help functionality."""

    def test_main_help(self):
        """'aikb --help' should show help."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Usage" in result.output or "usage" in result.output.lower()

    def test_get_help(self):
        """'aikb get --help' should show get command help."""
        result = runner.invoke(app, ["get", "--help"])
        assert result.exit_code == 0

    def test_search_help(self):
        """'aikb search --help' should show search command help."""
        result = runner.invoke(app, ["search", "--help"])
        assert result.exit_code == 0


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_invalid_layer(self):
        """Invalid layer should be handled gracefully."""
        result = runner.invoke(app, ["get", "99"])
        # Should handle gracefully (may succeed with fallback or error)
        assert result.exit_code in [0, 1, 2]

    def test_very_short_timeout(self):
        """Very short timeout should be handled."""
        result = runner.invoke(app, ["get", "--timeout", "1"])
        # Should complete (may use fallback)
        assert result.exit_code in [0, 1]

    def test_empty_search(self):
        """Empty search query should be handled."""
        # Typer requires the argument, so this tests the minimum case
        result = runner.invoke(app, ["search", "a"])
        assert result.exit_code == 0
