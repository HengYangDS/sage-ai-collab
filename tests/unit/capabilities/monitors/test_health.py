"""Tests for HealthMonitor.

Version: 0.1.0
"""

import pytest
from pathlib import Path
from unittest.mock import Mock
import asyncio

from sage.capabilities.monitors.health import (
    HealthMonitor,
    HealthStatus,
    HealthCheck,
    HealthReport,
    get_health_monitor,
)


class TestHealthStatus:
    """Tests for HealthStatus enum."""

    def test_health_statuses_exist(self):
        """Test that all health statuses exist."""
        assert HealthStatus.HEALTHY is not None
        assert HealthStatus.DEGRADED is not None
        assert HealthStatus.UNHEALTHY is not None
        assert HealthStatus.UNKNOWN is not None


class TestHealthCheck:
    """Tests for HealthCheck dataclass."""

    def test_health_check_creation(self):
        """Test creating a HealthCheck."""
        check = HealthCheck(
            name="filesystem",
            status=HealthStatus.HEALTHY,
            message="All files accessible",
            duration_ms=15.5,
        )
        assert check.name == "filesystem"
        assert check.status == HealthStatus.HEALTHY
        assert check.message == "All files accessible"
        assert check.duration_ms == 15.5

    def test_to_dict(self):
        """Test conversion to dictionary."""
        check = HealthCheck(
            name="config",
            status=HealthStatus.DEGRADED,
            message="Config file missing",
            duration_ms=10.0,
        )
        d = check.to_dict()
        assert isinstance(d, dict)
        assert d["name"] == "config"
        assert d["status"] == "degraded"
        assert "duration_ms" in d
        assert "timestamp" in d


class TestHealthReport:
    """Tests for HealthReport dataclass."""

    def test_health_report_creation(self):
        """Test creating a HealthReport."""
        checks = [
            HealthCheck("fs", HealthStatus.HEALTHY, "OK", 10.0),
            HealthCheck("config", HealthStatus.HEALTHY, "OK", 5.0),
        ]
        report = HealthReport(
            overall_status=HealthStatus.HEALTHY,
            checks=checks,
            duration_ms=15.0,
        )
        assert report.overall_status == HealthStatus.HEALTHY
        assert len(report.checks) == 2
        assert report.duration_ms == 15.0

    def test_to_dict(self):
        """Test conversion to dictionary."""
        report = HealthReport(
            overall_status=HealthStatus.HEALTHY,
            checks=[],
            duration_ms=10.0,
        )
        d = report.to_dict()
        assert isinstance(d, dict)
        assert d["overall_status"] == "healthy"
        assert "checks" in d
        assert "timestamp" in d
        assert "summary" in d


class TestHealthMonitor:
    """Tests for HealthMonitor class."""

    @pytest.fixture
    def monitor(self, tmp_path):
        """Create HealthMonitor instance with temp path."""
        return HealthMonitor(kb_path=tmp_path)

    @pytest.fixture
    def populated_kb(self, tmp_path):
        """Create a populated knowledge base structure."""
        content_dir = tmp_path / "content"
        content_dir.mkdir()
        (content_dir / "core").mkdir()
        (content_dir / "core" / "principles.md").write_text("# Principles\n\nContent.")

        # Create sage.yaml config
        (tmp_path / "sage.yaml").write_text("version: 0.1.0\n")

        return tmp_path

    def test_init(self, monitor):
        """Test monitor initialization."""
        assert monitor is not None
        assert monitor.kb_path is not None

    @pytest.mark.asyncio
    async def test_check_filesystem(self, populated_kb):
        """Test filesystem health check."""
        monitor = HealthMonitor(kb_path=populated_kb)
        check = await monitor.check_filesystem()
        assert isinstance(check, HealthCheck)
        assert check.name == "filesystem"

    @pytest.mark.asyncio
    async def test_check_config(self, populated_kb):
        """Test config health check."""
        monitor = HealthMonitor(kb_path=populated_kb)
        check = await monitor.check_config()
        assert isinstance(check, HealthCheck)
        assert check.name == "config"

    @pytest.mark.asyncio
    async def test_check_loader(self, monitor):
        """Test loader health check."""
        check = await monitor.check_loader()
        assert isinstance(check, HealthCheck)
        assert check.name == "loader"

    @pytest.mark.asyncio
    async def test_check_all(self, monitor):
        """Test running all health checks."""
        report = await monitor.check_all()
        assert isinstance(report, HealthReport)
        assert len(report.checks) >= 1
        assert report.overall_status in [
            HealthStatus.HEALTHY,
            HealthStatus.DEGRADED,
            HealthStatus.UNHEALTHY,
            HealthStatus.UNKNOWN,
        ]

    @pytest.mark.asyncio
    async def test_check_all_populated(self, populated_kb):
        """Test all checks with populated KB."""
        monitor = HealthMonitor(kb_path=populated_kb)
        report = await monitor.check_all()
        assert isinstance(report, HealthReport)

    def test_register_alert_callback(self, monitor):
        """Test registering alert callback."""
        callback = Mock()
        monitor.register_alert_callback(callback)
        assert callback in monitor._alert_callbacks

    @pytest.mark.asyncio
    async def test_get_history(self, monitor):
        """Test getting health check history."""
        # Run some checks first
        await monitor.check_all()
        await monitor.check_all()

        history = monitor.get_history(limit=5)
        assert isinstance(history, list)

    @pytest.mark.asyncio
    async def test_get_status_summary(self, monitor):
        """Test getting status summary."""
        await monitor.check_all()
        summary = monitor.get_status_summary()
        assert isinstance(summary, dict)

    @pytest.mark.asyncio
    async def test_check_filesystem_missing_path(self, tmp_path):
        """Test filesystem check with missing path."""
        fake_path = tmp_path / "nonexistent"
        monitor = HealthMonitor(kb_path=fake_path)
        check = await monitor.check_filesystem()
        assert check.status in [HealthStatus.DEGRADED, HealthStatus.UNHEALTHY]

    @pytest.mark.asyncio
    async def test_check_config_missing(self, tmp_path):
        """Test config check with missing config file."""
        monitor = HealthMonitor(kb_path=tmp_path)
        check = await monitor.check_config()
        # Should handle missing config gracefully
        assert isinstance(check, HealthCheck)


class TestGetHealthMonitorFunction:
    """Tests for standalone get_health_monitor function."""

    def test_get_health_monitor_function(self, tmp_path):
        """Test the standalone function."""
        monitor = get_health_monitor(tmp_path)
        assert monitor is not None
        assert isinstance(monitor, HealthMonitor)

    def test_get_health_monitor_default(self):
        """Test with default path."""
        monitor = get_health_monitor()
        assert monitor is not None
