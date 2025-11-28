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


    @pytest.mark.asyncio
    async def test_check_filesystem_no_index(self, tmp_path):
        """Test filesystem check when index.md is missing."""
        # Create all required directories but no index.md
        (tmp_path / "content" / "core").mkdir(parents=True)
        (tmp_path / "content" / "guidelines").mkdir(parents=True)
        (tmp_path / "tools").mkdir(parents=True)
        monitor = HealthMonitor(kb_path=tmp_path)
        check = await monitor.check_filesystem()
        assert check.status == HealthStatus.DEGRADED
        assert "index.md" in check.message

    @pytest.mark.asyncio
    async def test_check_filesystem_healthy(self, tmp_path):
        """Test filesystem check when everything is present."""
        # Create all required directories and index.md
        (tmp_path / "content" / "core").mkdir(parents=True)
        (tmp_path / "content" / "guidelines").mkdir(parents=True)
        (tmp_path / "tools").mkdir(parents=True)
        (tmp_path / "index.md").write_text("# Index\n")
        monitor = HealthMonitor(kb_path=tmp_path)
        check = await monitor.check_filesystem()
        assert check.status == HealthStatus.HEALTHY
        assert check.details is not None

    @pytest.mark.asyncio
    async def test_check_filesystem_exception(self, tmp_path, monkeypatch):
        """Test filesystem check handles exceptions."""
        monitor = HealthMonitor(kb_path=tmp_path)
        # Monkeypatch to raise exception
        def raise_error(*args, **kwargs):
            raise PermissionError("Access denied")
        monkeypatch.setattr(Path, "exists", raise_error)
        check = await monitor.check_filesystem()
        assert check.status == HealthStatus.UNHEALTHY
        assert "Error" in check.message

    @pytest.mark.asyncio
    async def test_check_config_valid_yaml(self, tmp_path):
        """Test config check with valid YAML containing all keys."""
        config_content = """
version: 0.1.0
timeout:
  default: 5000
loading:
  lazy: true
"""
        (tmp_path / "aikb.yaml").write_text(config_content)
        monitor = HealthMonitor(kb_path=tmp_path)
        check = await monitor.check_config()
        assert check.status == HealthStatus.HEALTHY
        assert check.details is not None

    @pytest.mark.asyncio
    async def test_check_config_missing_keys(self, tmp_path):
        """Test config check with missing required keys."""
        (tmp_path / "aikb.yaml").write_text("version: 0.1.0\n")
        monitor = HealthMonitor(kb_path=tmp_path)
        check = await monitor.check_config()
        assert check.status == HealthStatus.DEGRADED
        assert "Missing config keys" in check.message

    @pytest.mark.asyncio
    async def test_check_config_invalid_yaml(self, tmp_path):
        """Test config check with invalid YAML."""
        (tmp_path / "aikb.yaml").write_text("invalid: yaml: content: [")
        monitor = HealthMonitor(kb_path=tmp_path)
        check = await monitor.check_config()
        assert check.status == HealthStatus.UNHEALTHY
        assert "Error" in check.message

    @pytest.mark.asyncio
    async def test_check_loader_fallback(self, tmp_path, monkeypatch):
        """Test loader check with fallback status."""
        from sage.core.loader import LoadResult
        
        async def mock_load_core(*args, **kwargs):
            return LoadResult(
                content="fallback content",
                status="fallback",
                tokens_estimate=100,
                files_loaded=[],
                errors=[],
            )
        
        monitor = HealthMonitor(kb_path=tmp_path)
        monkeypatch.setattr(
            "sage.core.loader.KnowledgeLoader.load_core",
            mock_load_core
        )
        check = await monitor.check_loader()
        assert check.status == HealthStatus.DEGRADED
        assert "fallback" in check.message.lower()

    @pytest.mark.asyncio
    async def test_check_loader_other_status(self, tmp_path, monkeypatch):
        """Test loader check with other status."""
        from sage.core.loader import LoadResult
        
        async def mock_load_core(*args, **kwargs):
            return LoadResult(
                content="",
                status="partial",
                tokens_estimate=0,
                files_loaded=[],
                errors=["Some error"],
            )
        
        monitor = HealthMonitor(kb_path=tmp_path)
        monkeypatch.setattr(
            "sage.core.loader.KnowledgeLoader.load_core",
            mock_load_core
        )
        check = await monitor.check_loader()
        assert check.status == HealthStatus.DEGRADED
        assert check.details is not None

    @pytest.mark.asyncio
    async def test_check_loader_exception(self, tmp_path, monkeypatch):
        """Test loader check handles exceptions."""
        async def mock_load_core(*args, **kwargs):
            raise RuntimeError("Loader failed")
        
        monitor = HealthMonitor(kb_path=tmp_path)
        monkeypatch.setattr(
            "sage.core.loader.KnowledgeLoader.load_core",
            mock_load_core
        )
        check = await monitor.check_loader()
        assert check.status == HealthStatus.UNHEALTHY
        assert "error" in check.message.lower()

    @pytest.mark.asyncio
    async def test_check_all_with_exception(self, tmp_path, monkeypatch):
        """Test check_all handles exceptions from individual checks."""
        monitor = HealthMonitor(kb_path=tmp_path)
        
        async def raise_exception():
            raise ValueError("Test exception")
        
        monkeypatch.setattr(monitor, "check_filesystem", raise_exception)
        report = await monitor.check_all()
        assert report.overall_status == HealthStatus.UNHEALTHY
        assert any(c.name == "unknown" for c in report.checks)

    @pytest.mark.asyncio
    async def test_check_all_triggers_alert(self, tmp_path):
        """Test check_all triggers alert callbacks on unhealthy status."""
        monitor = HealthMonitor(kb_path=tmp_path)
        callback = Mock()
        monitor.register_alert_callback(callback)
        
        # Run check (will be degraded/unhealthy due to missing files)
        await monitor.check_all()
        
        # Callback should be called
        assert callback.called

    @pytest.mark.asyncio
    async def test_check_all_alert_callback_exception(self, tmp_path):
        """Test check_all handles alert callback exceptions."""
        monitor = HealthMonitor(kb_path=tmp_path)
        
        def bad_callback(report):
            raise RuntimeError("Callback error")
        
        monitor.register_alert_callback(bad_callback)
        # Should not raise exception
        report = await monitor.check_all()
        assert report is not None

    @pytest.mark.asyncio
    async def test_history_overflow(self, tmp_path):
        """Test history respects size limit."""
        monitor = HealthMonitor(kb_path=tmp_path, history_size=3)
        
        # Run more checks than history size
        for _ in range(5):
            await monitor.check_all()
        
        assert len(monitor._history) == 3

    @pytest.mark.asyncio
    async def test_start_stop_monitoring(self, tmp_path):
        """Test start and stop monitoring."""
        monitor = HealthMonitor(kb_path=tmp_path, check_interval_s=0.1)
        
        await monitor.start_monitoring()
        assert monitor._running is True
        
        # Wait a bit for at least one check
        await asyncio.sleep(0.15)
        
        await monitor.stop_monitoring()
        assert monitor._running is False
        assert monitor._task is None

    @pytest.mark.asyncio
    async def test_start_monitoring_already_running(self, tmp_path):
        """Test start_monitoring when already running."""
        monitor = HealthMonitor(kb_path=tmp_path, check_interval_s=0.1)
        
        await monitor.start_monitoring()
        task1 = monitor._task
        
        # Try to start again
        await monitor.start_monitoring()
        task2 = monitor._task
        
        # Should be the same task
        assert task1 is task2
        
        await monitor.stop_monitoring()

    def test_get_status_summary_no_history(self, tmp_path):
        """Test get_status_summary with no history."""
        monitor = HealthMonitor(kb_path=tmp_path)
        summary = monitor.get_status_summary()
        assert summary["status"] == "unknown"
        assert "No health checks" in summary["message"]


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
