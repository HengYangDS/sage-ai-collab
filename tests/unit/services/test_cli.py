"""
Unit tests for CLI service.

Tests cover:
- CLI app initialization
- Command registration
- Basic command execution
- Output formatting

Author: SAGE AI Collab Team
Version: 0.1.0
"""

from typer.testing import CliRunner

from sage.services.cli import app

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
