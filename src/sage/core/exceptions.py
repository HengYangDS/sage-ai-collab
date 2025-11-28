"""
SAGE Exception Hierarchy.

Structured exception classes for the knowledge base system.
All exceptions inherit from SAGEError for easy catching.

Version: 0.1.0

Exception Hierarchy:
    SAGEError (base)
    ├── LoadError
    │   ├── TimeoutError
    │   ├── ContentNotFoundError
    │   └── ValidationError
    ├── SearchError
    │   └── QueryError
    ├── ConfigError
    │   ├── ConfigNotFoundError
    │   └── ConfigParseError
    ├── PluginError
    │   ├── PluginLoadError
    │   └── PluginExecutionError
    └── ServiceError
        ├── MCPError
        └── CLIError
"""
from typing import Any


class SAGEError(Exception):
    """
    Base exception for all SAGE Knowledge Base errors.

    All custom exceptions should inherit from this class to enable
    catching all SAGE-related errors with a single except clause.

    Attributes:
        message: Human-readable error message
        code: Error code for programmatic handling
        details: Additional error context
    """

    def __init__(
        self,
        message: str,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code or "SAGE_ERROR"
        self.details = details or {}

    def __str__(self) -> str:
        if self.details:
            return f"[{self.code}] {self.message} - {self.details}"
        return f"[{self.code}] {self.message}"

    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for serialization."""
        return {
            "error": self.code,
            "message": self.message,
            "details": self.details,
        }


# =============================================================================
# Load Errors
# =============================================================================


class LoadError(SAGEError):
    """Base error for knowledge loading operations."""

    def __init__(
        self,
        message: str,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, code or "LOAD_ERROR", details)


class TimeoutError(LoadError):
    """Operation timed out."""

    def __init__(
        self,
        message: str = "Operation timed out",
        timeout_ms: int | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        details = details or {}
        if timeout_ms:
            details["timeout_ms"] = timeout_ms
        super().__init__(message, "TIMEOUT_ERROR", details)


class ContentNotFoundError(LoadError):
    """Requested content not found."""

    def __init__(
        self,
        path: str,
        message: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        details = details or {}
        details["path"] = path
        super().__init__(
            message or f"Content not found: {path}",
            "CONTENT_NOT_FOUND",
            details,
        )


class ValidationError(LoadError):
    """Content validation failed."""

    def __init__(
        self,
        message: str,
        errors: list[str] | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        details = details or {}
        if errors:
            details["validation_errors"] = errors
        super().__init__(message, "VALIDATION_ERROR", details)


# =============================================================================
# Search Errors
# =============================================================================


class SearchError(SAGEError):
    """Base error for search operations."""

    def __init__(
        self,
        message: str,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, code or "SEARCH_ERROR", details)


class QueryError(SearchError):
    """Invalid search query."""

    def __init__(
        self,
        query: str,
        message: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        details = details or {}
        details["query"] = query
        super().__init__(
            message or f"Invalid query: {query}",
            "QUERY_ERROR",
            details,
        )


# =============================================================================
# Config Errors
# =============================================================================


class ConfigError(SAGEError):
    """Base error for configuration operations."""

    def __init__(
        self,
        message: str,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, code or "CONFIG_ERROR", details)


class ConfigNotFoundError(ConfigError):
    """Configuration file not found."""

    def __init__(
        self,
        path: str,
        message: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        details = details or {}
        details["config_path"] = path
        super().__init__(
            message or f"Config file not found: {path}",
            "CONFIG_NOT_FOUND",
            details,
        )


class ConfigParseError(ConfigError):
    """Configuration parsing failed."""

    def __init__(
        self,
        path: str,
        message: str | None = None,
        parse_error: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        details = details or {}
        details["config_path"] = path
        if parse_error:
            details["parse_error"] = parse_error
        super().__init__(
            message or f"Failed to parse config: {path}",
            "CONFIG_PARSE_ERROR",
            details,
        )


# =============================================================================
# Plugin Errors
# =============================================================================


class PluginError(SAGEError):
    """Base error for plugin operations."""

    def __init__(
        self,
        message: str,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, code or "PLUGIN_ERROR", details)


class PluginLoadError(PluginError):
    """Plugin failed to load."""

    def __init__(
        self,
        plugin_name: str,
        message: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        details = details or {}
        details["plugin_name"] = plugin_name
        super().__init__(
            message or f"Failed to load plugin: {plugin_name}",
            "PLUGIN_LOAD_ERROR",
            details,
        )


class PluginExecutionError(PluginError):
    """Plugin execution failed."""

    def __init__(
        self,
        plugin_name: str,
        hook: str,
        message: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        details = details or {}
        details["plugin_name"] = plugin_name
        details["hook"] = hook
        super().__init__(
            message or f"Plugin {plugin_name} failed on hook {hook}",
            "PLUGIN_EXECUTION_ERROR",
            details,
        )


# =============================================================================
# Service Errors
# =============================================================================


class ServiceError(SAGEError):
    """Base error for service layer operations."""

    def __init__(
        self,
        message: str,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, code or "SERVICE_ERROR", details)


class MCPError(ServiceError):
    """MCP service error."""

    def __init__(
        self,
        message: str,
        tool_name: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        details = details or {}
        if tool_name:
            details["tool_name"] = tool_name
        super().__init__(message, "MCP_ERROR", details)


class CLIError(ServiceError):
    """CLI service error."""

    def __init__(
        self,
        message: str,
        command: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        details = details or {}
        if command:
            details["command"] = command
        super().__init__(message, "CLI_ERROR", details)


# =============================================================================
# DI Container Errors (re-export from di module for convenience)
# =============================================================================

# Note: DI-specific errors are defined in sage.core.di.container
# Import them here for convenience if needed:
# from sage.core.di.container import (
#     DIError,
#     ServiceNotFoundError,
#     CircularDependencyError,
#     ScopeRequiredError,
# )
