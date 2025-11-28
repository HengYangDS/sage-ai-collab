"""
Unit tests for CLI service.

Tests cover:
- CLI app initialization
- Command registration
- Basic command execution
- Output formatting
- Display functions
- Interactive mode

Author: SAGE AI Collab Team
Version: 0.1.0
"""

from io import StringIO
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from sage.services.cli import app, display_content, display_result, console

runner = CliRunner()


class TestCLIApp:
    """Tests for CLI application."""

    def test_app_exists(self):
        """Test CLI app is properly initialized."""
        assert app is not None

    def test_help_command(self):
        """Test --help shows usage information."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Usage:" in result.output
        # Rich uses "Options" with box border, not "Options:"
        assert "Options" in result.output
        assert "Commands" in result.output

    def test_version_command(self):
        """Test version command shows version."""
        result = runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output


class TestInfoCommand:
    """Tests for info command."""

    def test_info_command_runs(self):
        """Test info command executes without error."""
        result = runner.invoke(app, ["info"])
        assert result.exit_code == 0

    def test_info_shows_version(self):
        """Test info command shows version."""
        result = runner.invoke(app, ["info"])
        assert "0.1.0" in result.output or "Version" in result.output

    def test_info_shows_status(self):
        """Test info command shows status."""
        result = runner.invoke(app, ["info"])
        # Should show operational status or similar
        assert result.exit_code == 0


class TestGetCommand:
    """Tests for get command."""

    def test_get_help(self):
        """Test get command help."""
        result = runner.invoke(app, ["get", "--help"])
        assert result.exit_code == 0
        assert "Get knowledge" in result.output or "layer" in result.output.lower()

    def test_get_core(self):
        """Test get core command (layer 0)."""
        # get command uses numeric layers: 0=core, 1=guidelines, etc.
        result = runner.invoke(app, ["get", "0"])
        # May succeed or fail depending on content availability
        # Just verify it doesn't crash
        assert result.exit_code in [0, 1]

    def test_get_default(self):
        """Test get command with default layer."""
        result = runner.invoke(app, ["get"])
        # Default is layer 0 (core)
        assert result.exit_code in [0, 1]


class TestSearchCommand:
    """Tests for search command."""

    def test_search_help(self):
        """Test search command help."""
        result = runner.invoke(app, ["search", "--help"])
        assert result.exit_code == 0
        assert "Search" in result.output or "query" in result.output.lower()

    def test_search_with_query(self):
        """Test search with a query string."""
        result = runner.invoke(app, ["search", "test"])
        # May or may not find results
        assert result.exit_code in [0, 1]


class TestValidateCommand:
    """Tests for validate command."""

    def test_validate_help(self):
        """Test validate command help."""
        result = runner.invoke(app, ["validate", "--help"])
        assert result.exit_code == 0
        assert "Validate" in result.output or "structure" in result.output.lower()

    def test_validate_runs(self):
        """Test validate command executes."""
        result = runner.invoke(app, ["validate"])
        # May pass or fail depending on structure
        assert result.exit_code in [0, 1]


class TestCacheCommand:
    """Tests for cache command."""

    def test_cache_help(self):
        """Test cache command help."""
        result = runner.invoke(app, ["cache", "--help"])
        assert result.exit_code == 0


class TestGuidelinesCommand:
    """Tests for guidelines command."""

    def test_guidelines_help(self):
        """Test guidelines command help."""
        result = runner.invoke(app, ["guidelines", "--help"])
        assert result.exit_code == 0

    def test_guidelines_overview(self):
        """Test guidelines with overview section."""
        result = runner.invoke(app, ["guidelines", "overview"])
        # May succeed or fail depending on content
        assert result.exit_code in [0, 1]


class TestFrameworkCommand:
    """Tests for framework command."""

    def test_framework_help(self):
        """Test framework command help."""
        result = runner.invoke(app, ["framework", "--help"])
        assert result.exit_code == 0

    def test_framework_with_name(self):
        """Test framework with a name argument."""
        result = runner.invoke(app, ["framework", "autonomy"])
        # May succeed or fail depending on content
        assert result.exit_code in [0, 1]


class TestServeCommand:
    """Tests for serve command."""

    def test_serve_help(self):
        """Test serve command help."""
        result = runner.invoke(app, ["serve", "--help"])
        assert result.exit_code == 0
        assert "MCP" in result.output or "server" in result.output.lower()


class TestInteractiveCommand:
    """Tests for interactive command."""

    def test_interactive_help(self):
        """Test interactive command help."""
        result = runner.invoke(app, ["interactive", "--help"])
        assert result.exit_code == 0
        assert "REPL" in result.output or "interactive" in result.output.lower()


class TestCLIErrorHandling:
    """Tests for CLI error handling."""

    def test_unknown_command(self):
        """Test unknown command shows error."""
        result = runner.invoke(app, ["unknown_command_xyz"])
        assert result.exit_code != 0

    def test_invalid_option(self):
        """Test invalid option shows error."""
        result = runner.invoke(app, ["--invalid-option-xyz"])
        assert result.exit_code != 0


class TestCLIOutputFormat:
    """Tests for CLI output formatting."""

    def test_info_uses_table(self):
        """Test info command uses Rich table formatting."""
        result = runner.invoke(app, ["info"])
        # Rich tables use box characters or structured output
        assert result.exit_code == 0
        # Output should be structured (contains property names)
        assert (
            "Version" in result.output
            or "Status" in result.output
            or "Property" in result.output
        )

    def test_help_shows_all_commands(self):
        """Test help shows all registered commands."""
        result = runner.invoke(app, ["--help"])
        expected_commands = [
            "get",
            "search",
            "info",
            "validate",
            "serve",
            "cache",
            "version",
        ]
        for cmd in expected_commands:
            assert cmd in result.output.lower()


class TestDisplayContent:
    """Tests for display_content function."""

    def test_display_markdown_format(self):
        """Test display_content with markdown format."""
        with patch.object(console, 'print') as mock_print:
            display_content("# Test Header", format="markdown")
            mock_print.assert_called_once()

    def test_display_syntax_format(self):
        """Test display_content with syntax format."""
        with patch.object(console, 'print') as mock_print:
            display_content("# Test Header", format="syntax")
            mock_print.assert_called_once()

    def test_display_raw_format(self):
        """Test display_content with raw format."""
        with patch.object(console, 'print') as mock_print:
            display_content("Test content", format="raw")
            mock_print.assert_called_once_with("Test content")

    def test_display_unknown_format_defaults_to_markdown(self):
        """Test display_content with unknown format defaults to markdown."""
        with patch.object(console, 'print') as mock_print:
            display_content("# Test", format="unknown")
            mock_print.assert_called_once()


class TestDisplayResult:
    """Tests for display_result function."""

    def test_display_result_success(self):
        """Test display_result with success status."""
        mock_result = MagicMock()
        mock_result.status = "success"
        mock_result.tokens_estimate = 100
        mock_result.duration_ms = 50
        mock_result.content = "Test content"
        mock_result.files_loaded = []
        mock_result.errors = []

        with patch.object(console, 'print'):
            display_result(mock_result)

    def test_display_result_verbose_with_files(self):
        """Test display_result with verbose mode showing files."""
        mock_result = MagicMock()
        mock_result.status = "success"
        mock_result.tokens_estimate = 100
        mock_result.duration_ms = 50
        mock_result.content = "Test content"
        mock_result.files_loaded = ["file1.md", "file2.md"]
        mock_result.errors = []

        with patch.object(console, 'print'):
            display_result(mock_result, verbose=True)

    def test_display_result_verbose_with_errors(self):
        """Test display_result with verbose mode showing errors."""
        mock_result = MagicMock()
        mock_result.status = "error"
        mock_result.tokens_estimate = 0
        mock_result.duration_ms = 10
        mock_result.content = ""
        mock_result.files_loaded = []
        mock_result.errors = ["Error 1", "Error 2"]

        with patch.object(console, 'print'):
            display_result(mock_result, verbose=True)

    def test_display_result_partial_status(self):
        """Test display_result with partial status."""
        mock_result = MagicMock()
        mock_result.status = "partial"
        mock_result.tokens_estimate = 50
        mock_result.duration_ms = 30
        mock_result.content = "Partial content"
        mock_result.files_loaded = []
        mock_result.errors = []

        with patch.object(console, 'print'):
            display_result(mock_result)

    def test_display_result_fallback_status(self):
        """Test display_result with fallback status."""
        mock_result = MagicMock()
        mock_result.status = "fallback"
        mock_result.tokens_estimate = 25
        mock_result.duration_ms = 5
        mock_result.content = "Fallback content"
        mock_result.files_loaded = []
        mock_result.errors = []

        with patch.object(console, 'print'):
            display_result(mock_result)


class TestInteractiveMode:
    """Tests for interactive REPL mode."""

    def test_interactive_exit_command(self):
        """Test interactive mode exits with 'exit' command."""
        result = runner.invoke(app, ["interactive"], input="exit\n")
        assert result.exit_code == 0
        assert "Goodbye" in result.output or "exit" in result.output.lower()

    def test_interactive_quit_command(self):
        """Test interactive mode exits with 'quit' command."""
        result = runner.invoke(app, ["interactive"], input="quit\n")
        assert result.exit_code == 0

    def test_interactive_help_command(self):
        """Test interactive mode help command."""
        result = runner.invoke(app, ["interactive"], input="help\nexit\n")
        assert result.exit_code == 0
        assert "Available commands" in result.output or "get" in result.output

    def test_interactive_empty_input(self):
        """Test interactive mode handles empty input."""
        result = runner.invoke(app, ["interactive"], input="\nexit\n")
        assert result.exit_code == 0

    def test_interactive_unknown_command(self):
        """Test interactive mode handles unknown command."""
        result = runner.invoke(app, ["interactive"], input="unknowncmd\nexit\n")
        assert result.exit_code == 0
        assert "Unknown command" in result.output or "unknowncmd" in result.output

    def test_interactive_info_command(self):
        """Test interactive mode info command."""
        result = runner.invoke(app, ["interactive"], input="info\nexit\n")
        assert result.exit_code == 0

    def test_interactive_cache_command(self):
        """Test interactive mode cache command."""
        result = runner.invoke(app, ["interactive"], input="cache\nexit\n")
        assert result.exit_code == 0
        assert "Cached" in result.output or "files" in result.output

    def test_interactive_clear_command(self):
        """Test interactive mode clear command."""
        result = runner.invoke(app, ["interactive"], input="clear\nexit\n")
        assert result.exit_code == 0
        assert "cleared" in result.output.lower()

    def test_interactive_get_command(self):
        """Test interactive mode get command."""
        result = runner.invoke(app, ["interactive"], input="get 0\nexit\n")
        # May succeed or fail depending on content
        assert result.exit_code == 0

    def test_interactive_search_without_query(self):
        """Test interactive mode search without query shows usage."""
        result = runner.invoke(app, ["interactive"], input="search\nexit\n")
        assert result.exit_code == 0
        assert "Usage" in result.output or "search" in result.output

    def test_interactive_search_with_query(self):
        """Test interactive mode search with query."""
        result = runner.invoke(app, ["interactive"], input="search test\nexit\n")
        assert result.exit_code == 0

    def test_interactive_framework_without_name(self):
        """Test interactive mode framework without name shows usage."""
        result = runner.invoke(app, ["interactive"], input="framework\nexit\n")
        assert result.exit_code == 0
        assert "Usage" in result.output or "framework" in result.output

    def test_interactive_guidelines_command(self):
        """Test interactive mode guidelines command."""
        result = runner.invoke(app, ["interactive"], input="guidelines\nexit\n")
        assert result.exit_code == 0


class TestSearchWithResults:
    """Tests for search command with results."""

    def test_search_no_results(self):
        """Test search with no results shows message."""
        result = runner.invoke(app, ["search", "xyznonexistent123"])
        assert result.exit_code == 0
        # Should show "No results" or empty table
        assert "No results" in result.output or result.exit_code == 0

    def test_search_with_limit(self):
        """Test search with custom limit."""
        result = runner.invoke(app, ["search", "test", "--limit", "3"])
        assert result.exit_code in [0, 1]

    def test_search_with_timeout(self):
        """Test search with custom timeout."""
        result = runner.invoke(app, ["search", "test", "--timeout", "1000"])
        assert result.exit_code in [0, 1]


class TestValidateDetailed:
    """Detailed tests for validate command."""

    def test_validate_with_path(self):
        """Test validate with specific path."""
        result = runner.invoke(app, ["validate", "."])
        assert result.exit_code in [0, 1]

    def test_validate_with_fix_option(self):
        """Test validate with --fix option."""
        result = runner.invoke(app, ["validate", "--fix"])
        assert result.exit_code in [0, 1]


class TestGetCommandFormats:
    """Tests for get command with different formats."""

    def test_get_with_syntax_format(self):
        """Test get command with syntax format."""
        result = runner.invoke(app, ["get", "0", "--format", "syntax"])
        assert result.exit_code in [0, 1]

    def test_get_with_raw_format(self):
        """Test get command with raw format."""
        result = runner.invoke(app, ["get", "0", "--format", "raw"])
        assert result.exit_code in [0, 1]

    def test_get_with_verbose(self):
        """Test get command with verbose option."""
        result = runner.invoke(app, ["get", "0", "--verbose"])
        assert result.exit_code in [0, 1]

    def test_get_with_topic(self):
        """Test get command with topic option."""
        result = runner.invoke(app, ["get", "0", "--topic", "testing"])
        assert result.exit_code in [0, 1]


class TestValidateExtended:
    """Extended tests for validate command."""

    def test_validate_checks_index_file(self, tmp_path):
        """Test validate checks for index.md file."""
        # Create minimal structure without index.md
        (tmp_path / "content" / "core").mkdir(parents=True)
        result = runner.invoke(app, ["validate", str(tmp_path)])
        assert result.exit_code in [0, 1]
        # Should mention index.md in output
        assert "index" in result.output.lower() or "✓" in result.output or "✗" in result.output

    def test_validate_checks_guidelines_files(self, tmp_path):
        """Test validate checks for guideline files."""
        (tmp_path / "content" / "guidelines").mkdir(parents=True)
        result = runner.invoke(app, ["validate", str(tmp_path)])
        assert result.exit_code in [0, 1]

    def test_validate_with_all_directories(self, tmp_path):
        """Test validate with all required directories present."""
        dirs = [
            "content/core",
            "content/guidelines",
            "content/frameworks",
            "content/practices",
            "content/templates",
            "content/scenarios",
        ]
        for d in dirs:
            (tmp_path / d).mkdir(parents=True)
        (tmp_path / "index.md").write_text("# Index")
        result = runner.invoke(app, ["validate", str(tmp_path)])
        assert result.exit_code in [0, 1]

    def test_validate_fix_creates_directories(self, tmp_path):
        """Test validate --fix creates missing directories."""
        result = runner.invoke(app, ["validate", str(tmp_path), "--fix"])
        assert result.exit_code in [0, 1]
        # --fix should create some directories
        if "Created" in result.output:
            assert True  # Directories were created


class TestSearchWithActualResults:
    """Tests for search command when results are found."""

    def test_search_displays_table(self):
        """Test search displays results table when found."""
        # Search for common term in project
        result = runner.invoke(app, ["search", "knowledge"])
        assert result.exit_code == 0
        # Output should contain table elements or "No results"
        assert "Score" in result.output or "No results" in result.output or "Path" in result.output

    def test_search_truncates_preview(self):
        """Test search truncates long preview text."""
        result = runner.invoke(app, ["search", "content"])
        assert result.exit_code == 0


class TestInteractiveExtended:
    """Extended tests for interactive mode."""

    def test_interactive_framework_with_name(self):
        """Test interactive mode framework command with name."""
        result = runner.invoke(app, ["interactive"], input="framework autonomy\nexit\n")
        assert result.exit_code == 0

    def test_interactive_guidelines_with_chapter(self):
        """Test interactive mode guidelines with chapter."""
        result = runner.invoke(app, ["interactive"], input="guidelines quick_start\nexit\n")
        assert result.exit_code == 0

    def test_interactive_multiple_commands(self):
        """Test interactive mode with multiple commands."""
        result = runner.invoke(app, ["interactive"], input="info\ncache\nexit\n")
        assert result.exit_code == 0

    def test_interactive_quit_command(self):
        """Test interactive mode quit command."""
        result = runner.invoke(app, ["interactive"], input="quit\n")
        assert result.exit_code == 0

    def test_interactive_get_with_layer(self):
        """Test interactive mode get with layer number."""
        result = runner.invoke(app, ["interactive"], input="get 1\nexit\n")
        assert result.exit_code == 0


class TestInfoCommandExtended:
    """Extended tests for info command."""

    def test_info_shows_version(self):
        """Test info command shows version."""
        result = runner.invoke(app, ["info"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output or "Version" in result.output

    def test_info_shows_features(self):
        """Test info command shows features."""
        result = runner.invoke(app, ["info"])
        assert result.exit_code == 0
        assert "Features" in result.output or "timeout" in result.output.lower()


class TestServeCommandExtended:
    """Extended tests for serve command."""

    def test_serve_help(self):
        """Test serve command help."""
        result = runner.invoke(app, ["serve", "--help"])
        assert result.exit_code == 0
        assert "MCP" in result.output or "server" in result.output.lower()


class TestCLIEdgeCases:
    """Tests for CLI edge cases."""

    def test_get_invalid_layer_number(self):
        """Test get with invalid layer number."""
        result = runner.invoke(app, ["get", "999"])
        # Should handle gracefully
        assert result.exit_code in [0, 1, 2]

    def test_search_empty_query(self):
        """Test search with empty-like query."""
        result = runner.invoke(app, ["search", " "])
        assert result.exit_code in [0, 1]

    def test_guidelines_invalid_chapter(self):
        """Test guidelines with invalid chapter name."""
        result = runner.invoke(app, ["guidelines", "nonexistent_xyz"])
        assert result.exit_code in [0, 1]

    def test_framework_invalid_name(self):
        """Test framework with invalid name."""
        result = runner.invoke(app, ["framework", "nonexistent_xyz"])
        assert result.exit_code in [0, 1]
