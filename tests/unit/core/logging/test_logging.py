"""Tests for sage.core.logging module.

Version: 0.1.0
"""

import pytest

from sage.core.logging import (
    LogFormat,
    LogLevel,
    bind_context,
    clear_context,
    configure_logging,
    get_context,
    get_logger,
    logging_context,
    reset_logging,
    unbind_context,
)


class TestLogLevel:
    """Tests for LogLevel enum."""

    def test_log_levels_exist(self):
        """Test that all standard log levels exist."""
        assert LogLevel.DEBUG == "DEBUG"
        assert LogLevel.INFO == "INFO"
        assert LogLevel.WARNING == "WARNING"
        assert LogLevel.ERROR == "ERROR"
        assert LogLevel.CRITICAL == "CRITICAL"

    def test_log_level_is_string(self):
        """Test that LogLevel values are strings."""
        assert isinstance(LogLevel.INFO.value, str)


class TestLogFormat:
    """Tests for LogFormat enum."""

    def test_log_formats_exist(self):
        """Test that all log formats exist."""
        assert LogFormat.CONSOLE == "console"
        assert LogFormat.JSON == "json"


class TestConfigureLogging:
    """Tests for configure_logging function."""

    def setup_method(self):
        """Reset logging before each test."""
        reset_logging()
        clear_context()

    def teardown_method(self):
        """Reset logging after each test."""
        reset_logging()
        clear_context()

    def test_configure_with_default_settings(self):
        """Test configure_logging with default settings."""
        configure_logging()
        logger = get_logger("test")
        assert logger is not None

    def test_configure_with_log_level_enum(self):
        """Test configure_logging with LogLevel enum."""
        configure_logging(level=LogLevel.DEBUG)
        logger = get_logger("test")
        assert logger is not None

    def test_configure_with_log_level_string(self):
        """Test configure_logging with string log level."""
        configure_logging(level="DEBUG")
        logger = get_logger("test")
        assert logger is not None

    def test_configure_with_format_enum(self):
        """Test configure_logging with LogFormat enum."""
        configure_logging(format_type=LogFormat.JSON)
        logger = get_logger("test")
        assert logger is not None

    def test_configure_with_format_string(self):
        """Test configure_logging with string format."""
        configure_logging(format_type="json")
        logger = get_logger("test")
        assert logger is not None

    def test_configure_with_cache_disabled(self):
        """Test configure_logging with caching disabled."""
        configure_logging(cache_logger=False)
        logger = get_logger("test")
        assert logger is not None


class TestGetLogger:
    """Tests for get_logger function."""

    def setup_method(self):
        """Reset logging before each test."""
        reset_logging()
        clear_context()
        configure_logging()

    def teardown_method(self):
        """Reset logging after each test."""
        reset_logging()
        clear_context()

    def test_get_logger_with_name(self):
        """Test get_logger with a specific name."""
        logger = get_logger("sage.core.loader")
        assert logger is not None

    def test_get_logger_without_name(self):
        """Test get_logger without a name."""
        logger = get_logger()
        assert logger is not None

    def test_logger_has_log_methods(self):
        """Test that logger has standard logging methods."""
        logger = get_logger("test")
        assert hasattr(logger, "debug")
        assert hasattr(logger, "info")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "error")


class TestContextManagement:
    """Tests for context management functions."""

    def setup_method(self):
        """Reset logging and context before each test."""
        reset_logging()
        clear_context()
        configure_logging()

    def teardown_method(self):
        """Reset logging and context after each test."""
        reset_logging()
        clear_context()

    def test_bind_context(self):
        """Test bind_context adds context variables."""
        bind_context(request_id="abc-123")
        ctx = get_context()
        assert ctx.get("request_id") == "abc-123"

    def test_bind_multiple_context(self):
        """Test bind_context with multiple values."""
        bind_context(request_id="abc-123", user="admin")
        ctx = get_context()
        assert ctx.get("request_id") == "abc-123"
        assert ctx.get("user") == "admin"

    def test_unbind_context(self):
        """Test unbind_context removes specific keys."""
        bind_context(request_id="abc-123", temp="xyz")
        unbind_context("temp")
        ctx = get_context()
        assert ctx.get("request_id") == "abc-123"
        assert "temp" not in ctx

    def test_clear_context(self):
        """Test clear_context removes all context."""
        bind_context(request_id="abc-123", user="admin")
        clear_context()
        ctx = get_context()
        assert len(ctx) == 0

    def test_get_context_returns_dict(self):
        """Test get_context returns a dictionary."""
        ctx = get_context()
        assert isinstance(ctx, dict)


class TestLoggingContext:
    """Tests for logging_context context manager."""

    def setup_method(self):
        """Reset logging and context before each test."""
        reset_logging()
        clear_context()
        configure_logging()

    def teardown_method(self):
        """Reset logging and context after each test."""
        reset_logging()
        clear_context()

    def test_logging_context_adds_context(self):
        """Test logging_context adds context within block."""
        with logging_context(operation="test"):
            ctx = get_context()
            assert ctx.get("operation") == "test"

    def test_logging_context_removes_context_after(self):
        """Test logging_context removes context after block."""
        with logging_context(operation="test"):
            pass
        ctx = get_context()
        assert "operation" not in ctx

    def test_logging_context_preserves_existing(self):
        """Test logging_context preserves existing context."""
        bind_context(request_id="abc-123")
        with logging_context(operation="test"):
            ctx = get_context()
            assert ctx.get("request_id") == "abc-123"
            assert ctx.get("operation") == "test"
        ctx = get_context()
        assert ctx.get("request_id") == "abc-123"
        assert "operation" not in ctx

    def test_logging_context_with_multiple_keys(self):
        """Test logging_context with multiple keys."""
        with logging_context(operation="load", layer="core"):
            ctx = get_context()
            assert ctx.get("operation") == "load"
            assert ctx.get("layer") == "core"
        ctx = get_context()
        assert "operation" not in ctx
        assert "layer" not in ctx


class TestResetLogging:
    """Tests for reset_logging function."""

    def test_reset_logging_clears_config(self):
        """Test reset_logging clears configuration."""
        configure_logging(level=LogLevel.DEBUG)
        reset_logging()
        # After reset, we should be able to reconfigure
        configure_logging(level=LogLevel.INFO)
        logger = get_logger("test")
        assert logger is not None
