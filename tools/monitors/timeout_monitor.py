"""
Timeout Monitor - Timeout tracking and alerting for AI Collaboration Knowledge Base.

This module provides:
- TimeoutEvent: Individual timeout event record
- TimeoutStats: Timeout statistics
- TimeoutMonitor: Real-time timeout monitoring and alerting

Author: SAGE AI Collab Team
Version: 2.0.0
"""

import asyncio
import logging
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class TimeoutLevel(Enum):
    """Timeout levels matching the 5-level hierarchy."""

    T1_CACHE = 1  # 100ms - Cache lookup
    T2_FILE = 2  # 500ms - Single file
    T3_LAYER = 3  # 2s - Layer load
    T4_FULL = 4  # 5s - Full KB load
    T5_ANALYSIS = 5  # 10s - Complex analysis


@dataclass
class TimeoutEvent:
    """Record of a timeout or near-timeout event."""

    operation: str
    level: TimeoutLevel
    timeout_ms: int
    actual_ms: float
    timed_out: bool
    timestamp: datetime = field(default_factory=datetime.now)
    details: dict[str, Any] = field(default_factory=dict)

    @property
    def utilization(self) -> float:
        """Percentage of timeout used."""
        return (self.actual_ms / self.timeout_ms) * 100 if self.timeout_ms > 0 else 0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "operation": self.operation,
            "level": self.level.name,
            "timeout_ms": self.timeout_ms,
            "actual_ms": round(self.actual_ms, 2),
            "timed_out": self.timed_out,
            "utilization": round(self.utilization, 1),
            "timestamp": self.timestamp.isoformat(),
            "details": self.details,
        }


@dataclass
class TimeoutStats:
    """Statistics for timeout events."""

    total_operations: int = 0
    timeout_count: int = 0
    near_timeout_count: int = 0  # >80% utilization
    avg_utilization: float = 0.0
    max_utilization: float = 0.0
    by_level: dict[str, dict[str, Any]] = field(default_factory=dict)
    period_start: datetime = field(default_factory=datetime.now)
    period_end: datetime = field(default_factory=datetime.now)

    @property
    def timeout_rate(self) -> float:
        """Percentage of operations that timed out."""
        return (
            (self.timeout_count / self.total_operations * 100)
            if self.total_operations > 0
            else 0
        )

    @property
    def near_timeout_rate(self) -> float:
        """Percentage of operations near timeout (>80% utilization)."""
        return (
            (self.near_timeout_count / self.total_operations * 100)
            if self.total_operations > 0
            else 0
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_operations": self.total_operations,
            "timeout_count": self.timeout_count,
            "timeout_rate": round(self.timeout_rate, 2),
            "near_timeout_count": self.near_timeout_count,
            "near_timeout_rate": round(self.near_timeout_rate, 2),
            "avg_utilization": round(self.avg_utilization, 1),
            "max_utilization": round(self.max_utilization, 1),
            "by_level": self.by_level,
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
        }


class TimeoutMonitor:
    """
    Real-time timeout monitoring and alerting.

    Features:
    - Track all timeout events
    - Calculate statistics by level and operation
    - Alert on high timeout rates
    - Provide recommendations for timeout tuning
    """

    # Thresholds for alerts
    TIMEOUT_RATE_WARNING = 1.0  # 1% timeout rate triggers warning
    TIMEOUT_RATE_CRITICAL = 5.0  # 5% timeout rate triggers critical
    NEAR_TIMEOUT_WARNING = 10.0  # 10% near-timeout rate triggers warning
    UTILIZATION_WARNING = 80.0  # 80% utilization is considered "near timeout"

    def __init__(
        self,
        max_events: int = 10000,
        stats_window_minutes: int = 60,
    ):
        """
        Initialize timeout monitor.

        Args:
            max_events: Maximum events to retain in memory
            stats_window_minutes: Window for rolling statistics
        """
        self.max_events = max_events
        self.stats_window_minutes = stats_window_minutes

        self._events: deque[TimeoutEvent] = deque(maxlen=max_events)
        self._alert_callbacks: list[Callable[[str, TimeoutStats], None]] = []
        self._running = False
        self._task: asyncio.Task | None = None

    def register_alert_callback(
        self,
        callback: Callable[[str, TimeoutStats], None],
    ) -> None:
        """
        Register a callback for timeout alerts.

        Args:
            callback: Function(alert_level, stats) to call on alerts
        """
        self._alert_callbacks.append(callback)

    def record_event(
        self,
        operation: str,
        level: TimeoutLevel,
        timeout_ms: int,
        actual_ms: float,
        timed_out: bool = False,
        details: dict[str, Any] | None = None,
    ) -> TimeoutEvent:
        """
        Record a timeout event.

        Args:
            operation: Name of the operation
            level: Timeout level (T1-T5)
            timeout_ms: Configured timeout in milliseconds
            actual_ms: Actual duration in milliseconds
            timed_out: Whether the operation timed out
            details: Additional details

        Returns:
            The recorded TimeoutEvent
        """
        event = TimeoutEvent(
            operation=operation,
            level=level,
            timeout_ms=timeout_ms,
            actual_ms=actual_ms,
            timed_out=timed_out,
            details=details or {},
        )

        self._events.append(event)

        # Check for immediate alerts
        if timed_out or event.utilization >= self.UTILIZATION_WARNING:
            self._check_alerts()

        return event

    def get_stats(
        self,
        minutes: int | None = None,
        level: TimeoutLevel | None = None,
        operation: str | None = None,
    ) -> TimeoutStats:
        """
        Get timeout statistics.

        Args:
            minutes: Time window in minutes (default: stats_window_minutes)
            level: Filter by timeout level
            operation: Filter by operation name

        Returns:
            TimeoutStats for the specified filters
        """
        minutes = minutes or self.stats_window_minutes
        cutoff = datetime.now() - timedelta(minutes=minutes)

        # Filter events
        events = [
            e
            for e in self._events
            if e.timestamp >= cutoff
            and (level is None or e.level == level)
            and (operation is None or e.operation == operation)
        ]

        if not events:
            return TimeoutStats()

        # Calculate statistics
        total = len(events)
        timeouts = sum(1 for e in events if e.timed_out)
        near_timeouts = sum(
            1
            for e in events
            if e.utilization >= self.UTILIZATION_WARNING and not e.timed_out
        )
        utilizations = [e.utilization for e in events]

        # Stats by level
        by_level = {}
        for lvl in TimeoutLevel:
            level_events = [e for e in events if e.level == lvl]
            if level_events:
                by_level[lvl.name] = {
                    "count": len(level_events),
                    "timeouts": sum(1 for e in level_events if e.timed_out),
                    "avg_utilization": sum(e.utilization for e in level_events)
                    / len(level_events),
                }

        return TimeoutStats(
            total_operations=total,
            timeout_count=timeouts,
            near_timeout_count=near_timeouts,
            avg_utilization=sum(utilizations) / len(utilizations),
            max_utilization=max(utilizations),
            by_level=by_level,
            period_start=min(e.timestamp for e in events),
            period_end=max(e.timestamp for e in events),
        )

    def get_recent_events(
        self,
        limit: int = 100,
        timed_out_only: bool = False,
    ) -> list[TimeoutEvent]:
        """
        Get recent timeout events.

        Args:
            limit: Maximum events to return
            timed_out_only: Only return events that timed out

        Returns:
            List of recent TimeoutEvents
        """
        events = list(self._events)

        if timed_out_only:
            events = [e for e in events if e.timed_out]

        return events[-limit:]

    def get_recommendations(self) -> list[dict[str, Any]]:
        """
        Get recommendations for timeout tuning.

        Returns:
            List of recommendation dictionaries
        """
        stats = self.get_stats()
        recommendations = []

        # Check overall timeout rate
        if stats.timeout_rate > self.TIMEOUT_RATE_CRITICAL:
            recommendations.append(
                {
                    "severity": "critical",
                    "message": f"High timeout rate: {stats.timeout_rate:.1f}%",
                    "recommendation": "Increase timeout values or optimize slow operations",
                }
            )
        elif stats.timeout_rate > self.TIMEOUT_RATE_WARNING:
            recommendations.append(
                {
                    "severity": "warning",
                    "message": f"Elevated timeout rate: {stats.timeout_rate:.1f}%",
                    "recommendation": "Monitor closely and consider increasing timeouts",
                }
            )

        # Check near-timeout rate
        if stats.near_timeout_rate > self.NEAR_TIMEOUT_WARNING:
            recommendations.append(
                {
                    "severity": "warning",
                    "message": f"High near-timeout rate: {stats.near_timeout_rate:.1f}%",
                    "recommendation": "Operations are running close to timeout limits",
                }
            )

        # Check by level
        for level_name, level_stats in stats.by_level.items():
            if level_stats.get("timeouts", 0) > 0:
                timeout_rate = level_stats["timeouts"] / level_stats["count"] * 100
                if timeout_rate > 5:
                    recommendations.append(
                        {
                            "severity": "warning",
                            "level": level_name,
                            "message": f"{level_name} has {timeout_rate:.1f}% timeout rate",
                            "recommendation": f"Consider increasing {level_name} timeout",
                        }
                    )

        if not recommendations:
            recommendations.append(
                {
                    "severity": "info",
                    "message": "All timeout metrics within normal range",
                    "recommendation": "No action needed",
                }
            )

        return recommendations

    def _check_alerts(self) -> None:
        """Check if alerts should be triggered."""
        stats = self.get_stats(minutes=5)  # Last 5 minutes

        alert_level = None
        if stats.timeout_rate > self.TIMEOUT_RATE_CRITICAL:
            alert_level = "critical"
        elif stats.timeout_rate > self.TIMEOUT_RATE_WARNING:
            alert_level = "warning"
        elif stats.near_timeout_rate > self.NEAR_TIMEOUT_WARNING:
            alert_level = "warning"

        if alert_level:
            for callback in self._alert_callbacks:
                try:
                    callback(alert_level, stats)
                except Exception as e:
                    logger.error(f"Alert callback error: {e}")

    async def start_monitoring(self, interval_s: float = 60.0) -> None:
        """
        Start periodic monitoring.

        Args:
            interval_s: Check interval in seconds
        """
        if self._running:
            return

        self._running = True

        async def monitor_loop():
            while self._running:
                try:
                    self._check_alerts()
                except Exception as e:
                    logger.error(f"Timeout monitor error: {e}")
                await asyncio.sleep(interval_s)

        self._task = asyncio.create_task(monitor_loop())
        logger.info(f"Timeout monitoring started (interval: {interval_s}s)")

    async def stop_monitoring(self) -> None:
        """Stop periodic monitoring."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None
        logger.info("Timeout monitoring stopped")

    def clear_events(self) -> int:
        """
        Clear all recorded events.

        Returns:
            Number of events cleared
        """
        count = len(self._events)
        self._events.clear()
        return count

    def get_summary(self) -> dict[str, Any]:
        """Get a summary of timeout monitoring status."""
        stats = self.get_stats()
        recommendations = self.get_recommendations()

        return {
            "status": (
                "healthy"
                if stats.timeout_rate < self.TIMEOUT_RATE_WARNING
                else "warning"
            ),
            "stats": stats.to_dict(),
            "recommendations": recommendations,
            "event_count": len(self._events),
            "monitoring_active": self._running,
        }


# Global monitor instance
_monitor: TimeoutMonitor | None = None


def get_timeout_monitor() -> TimeoutMonitor:
    """Get or create the global timeout monitor."""
    global _monitor
    if _monitor is None:
        _monitor = TimeoutMonitor()
    return _monitor


def record_timeout_event(
    operation: str,
    level: TimeoutLevel,
    timeout_ms: int,
    actual_ms: float,
    timed_out: bool = False,
    details: dict[str, Any] | None = None,
) -> TimeoutEvent:
    """Convenience function to record a timeout event."""
    monitor = get_timeout_monitor()
    return monitor.record_event(
        operation=operation,
        level=level,
        timeout_ms=timeout_ms,
        actual_ms=actual_ms,
        timed_out=timed_out,
        details=details,
    )
