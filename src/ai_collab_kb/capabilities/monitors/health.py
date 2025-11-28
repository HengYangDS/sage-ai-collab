"""
Health Monitor - System health monitoring for AI Collaboration Knowledge Base.

This module provides:
- HealthStatus: Health status enumeration
- HealthCheck: Individual health check result
- HealthMonitor: Comprehensive health monitoring

Author: AI Collaboration KB Team
Version: 2.0.0
"""

import asyncio
import logging
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """Health status levels."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class HealthCheck:
    """Result of a single health check."""

    name: str
    status: HealthStatus
    message: str = ""
    duration_ms: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "status": self.status.value,
            "message": self.message,
            "duration_ms": self.duration_ms,
            "timestamp": self.timestamp.isoformat(),
            "details": self.details,
        }


@dataclass
class HealthReport:
    """Comprehensive health report."""

    overall_status: HealthStatus
    checks: list[HealthCheck]
    timestamp: datetime = field(default_factory=datetime.now)
    duration_ms: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "overall_status": self.overall_status.value,
            "checks": [c.to_dict() for c in self.checks],
            "timestamp": self.timestamp.isoformat(),
            "duration_ms": self.duration_ms,
            "summary": {
                "total": len(self.checks),
                "healthy": sum(
                    1 for c in self.checks if c.status == HealthStatus.HEALTHY
                ),
                "degraded": sum(
                    1 for c in self.checks if c.status == HealthStatus.DEGRADED
                ),
                "unhealthy": sum(
                    1 for c in self.checks if c.status == HealthStatus.UNHEALTHY
                ),
            },
        }


class HealthMonitor:
    """
    Comprehensive health monitoring for the knowledge base.

    Features:
    - Multiple health check types (file system, cache, timeout, etc.)
    - Configurable check intervals
    - Health history tracking
    - Alert callbacks
    """

    def __init__(
        self,
        kb_path: Path | None = None,
        check_interval_s: float = 60.0,
        history_size: int = 100,
    ):
        """
        Initialize health monitor.

        Args:
            kb_path: Path to knowledge base root
            check_interval_s: Interval between automatic checks
            history_size: Number of historical checks to retain
        """
        self.kb_path = kb_path or Path(__file__).parent.parent.parent
        self.check_interval_s = check_interval_s
        self.history_size = history_size

        self._history: list[HealthReport] = []
        self._alert_callbacks: list[Callable[[HealthReport], None]] = []
        self._running = False
        self._task: asyncio.Task | None = None

    def register_alert_callback(
        self,
        callback: Callable[[HealthReport], None],
    ) -> None:
        """Register a callback for health alerts."""
        self._alert_callbacks.append(callback)

    async def check_filesystem(self) -> HealthCheck:
        """Check file system health."""
        start = time.monotonic()
        try:
            # Check if KB path exists
            if not self.kb_path.exists():
                return HealthCheck(
                    name="filesystem",
                    status=HealthStatus.UNHEALTHY,
                    message=f"KB path not found: {self.kb_path}",
                    duration_ms=(time.monotonic() - start) * 1000,
                )

            # Check core directories
            core_dirs = ["content/core", "content/guidelines", "tools"]
            missing_dirs = []
            for dir_name in core_dirs:
                dir_path = self.kb_path / dir_name
                if not dir_path.exists():
                    missing_dirs.append(dir_name)

            if missing_dirs:
                return HealthCheck(
                    name="filesystem",
                    status=HealthStatus.DEGRADED,
                    message=f"Missing directories: {', '.join(missing_dirs)}",
                    duration_ms=(time.monotonic() - start) * 1000,
                    details={"missing": missing_dirs},
                )

            # Check index.md exists
            index_path = self.kb_path / "index.md"
            if not index_path.exists():
                return HealthCheck(
                    name="filesystem",
                    status=HealthStatus.DEGRADED,
                    message="index.md not found",
                    duration_ms=(time.monotonic() - start) * 1000,
                )

            # Count files
            md_count = len(list(self.kb_path.rglob("*.md")))
            py_count = len(list(self.kb_path.rglob("*.py")))

            return HealthCheck(
                name="filesystem",
                status=HealthStatus.HEALTHY,
                message=f"All directories present ({md_count} MD, {py_count} PY files)",
                duration_ms=(time.monotonic() - start) * 1000,
                details={"md_files": md_count, "py_files": py_count},
            )

        except Exception as e:
            return HealthCheck(
                name="filesystem",
                status=HealthStatus.UNHEALTHY,
                message=f"Error checking filesystem: {e}",
                duration_ms=(time.monotonic() - start) * 1000,
            )

    async def check_config(self) -> HealthCheck:
        """Check configuration health."""
        start = time.monotonic()
        try:
            config_path = self.kb_path / "aikb.yaml"

            if not config_path.exists():
                return HealthCheck(
                    name="config",
                    status=HealthStatus.DEGRADED,
                    message="aikb.yaml not found",
                    duration_ms=(time.monotonic() - start) * 1000,
                )

            # Try to parse YAML
            import yaml

            with open(config_path, encoding="utf-8") as f:
                config = yaml.safe_load(f)

            # Check required keys
            required_keys = ["version", "timeout", "loading"]
            missing_keys = [k for k in required_keys if k not in config]

            if missing_keys:
                return HealthCheck(
                    name="config",
                    status=HealthStatus.DEGRADED,
                    message=f"Missing config keys: {', '.join(missing_keys)}",
                    duration_ms=(time.monotonic() - start) * 1000,
                    details={"missing_keys": missing_keys},
                )

            return HealthCheck(
                name="config",
                status=HealthStatus.HEALTHY,
                message=f"Config valid (version: {config.get('version', 'unknown')})",
                duration_ms=(time.monotonic() - start) * 1000,
                details={"version": config.get("version")},
            )

        except Exception as e:
            return HealthCheck(
                name="config",
                status=HealthStatus.UNHEALTHY,
                message=f"Error checking config: {e}",
                duration_ms=(time.monotonic() - start) * 1000,
            )

    async def check_loader(self) -> HealthCheck:
        """Check loader health by attempting a quick load."""
        start = time.monotonic()
        try:
            # Import loader
            import sys

            src_path = self.kb_path / "src"
            if str(src_path) not in sys.path:
                sys.path.insert(0, str(src_path))

            from ai_collab_kb.loader import KnowledgeLoader

            loader = KnowledgeLoader(kb_path=self.kb_path)
            result = await loader.load_core(timeout_ms=2000)

            duration = (time.monotonic() - start) * 1000

            if result.status == "success":
                return HealthCheck(
                    name="loader",
                    status=HealthStatus.HEALTHY,
                    message=f"Loader OK ({result.tokens_estimate} tokens in {duration:.0f}ms)",
                    duration_ms=duration,
                    details={
                        "tokens": result.tokens_estimate,
                        "files_loaded": len(result.files_loaded),
                    },
                )
            elif result.status == "fallback":
                return HealthCheck(
                    name="loader",
                    status=HealthStatus.DEGRADED,
                    message="Loader using fallback",
                    duration_ms=duration,
                )
            else:
                return HealthCheck(
                    name="loader",
                    status=HealthStatus.DEGRADED,
                    message=f"Loader status: {result.status}",
                    duration_ms=duration,
                    details={"errors": result.errors},
                )

        except Exception as e:
            return HealthCheck(
                name="loader",
                status=HealthStatus.UNHEALTHY,
                message=f"Loader error: {e}",
                duration_ms=(time.monotonic() - start) * 1000,
            )

    async def check_all(self) -> HealthReport:
        """Run all health checks and generate a report."""
        start = time.monotonic()

        # Run all checks concurrently
        checks = await asyncio.gather(
            self.check_filesystem(),
            self.check_config(),
            self.check_loader(),
            return_exceptions=True,
        )

        # Process results
        results = []
        for check in checks:
            if isinstance(check, Exception):
                results.append(
                    HealthCheck(
                        name="unknown",
                        status=HealthStatus.UNHEALTHY,
                        message=str(check),
                    )
                )
            else:
                results.append(check)

        # Determine overall status
        if any(c.status == HealthStatus.UNHEALTHY for c in results):
            overall = HealthStatus.UNHEALTHY
        elif any(c.status == HealthStatus.DEGRADED for c in results):
            overall = HealthStatus.DEGRADED
        elif all(c.status == HealthStatus.HEALTHY for c in results):
            overall = HealthStatus.HEALTHY
        else:
            overall = HealthStatus.UNKNOWN

        report = HealthReport(
            overall_status=overall,
            checks=results,
            duration_ms=(time.monotonic() - start) * 1000,
        )

        # Store in history
        self._history.append(report)
        if len(self._history) > self.history_size:
            self._history.pop(0)

        # Trigger alerts if unhealthy
        if overall in [HealthStatus.UNHEALTHY, HealthStatus.DEGRADED]:
            for callback in self._alert_callbacks:
                try:
                    callback(report)
                except Exception as e:
                    logger.error(f"Alert callback error: {e}")

        return report

    async def start_monitoring(self) -> None:
        """Start continuous health monitoring."""
        if self._running:
            return

        self._running = True

        async def monitor_loop():
            while self._running:
                try:
                    await self.check_all()
                except Exception as e:
                    logger.error(f"Health check error: {e}")
                await asyncio.sleep(self.check_interval_s)

        self._task = asyncio.create_task(monitor_loop())
        logger.info(f"Health monitoring started (interval: {self.check_interval_s}s)")

    async def stop_monitoring(self) -> None:
        """Stop continuous health monitoring."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None
        logger.info("Health monitoring stopped")

    def get_history(self, limit: int = 10) -> list[HealthReport]:
        """Get recent health history."""
        return self._history[-limit:]

    def get_status_summary(self) -> dict[str, Any]:
        """Get the current status summary."""
        if not self._history:
            return {
                "status": "unknown",
                "message": "No health checks performed yet",
            }

        latest = self._history[-1]
        return {
            "status": latest.overall_status.value,
            "timestamp": latest.timestamp.isoformat(),
            "checks": {c.name: c.status.value for c in latest.checks},
            "history_size": len(self._history),
        }


# Convenience function
def get_health_monitor(kb_path: Path | None = None) -> HealthMonitor:
    """Get a health monitor instance."""
    return HealthMonitor(kb_path=kb_path)
