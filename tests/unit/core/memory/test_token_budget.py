"""Unit tests for TokenBudget.

Tests cover:
- TokenWarningLevel enum
- TokenBudgetConfig
- TokenUsage dataclass
- TokenBudget controller with warning levels and callbacks
"""

import tempfile
from pathlib import Path

import pytest

from sage.core.memory.store import MemoryPriority, MemoryStore, MemoryType
from sage.core.memory.token_budget import (
    TokenBudget,
    TokenBudgetConfig,
    TokenUsage,
    TokenWarningLevel,
)


class TestTokenWarningLevel:
    """Tests for TokenWarningLevel enum."""

    def test_warning_levels_exist(self):
        """Test all expected warning levels exist."""
        assert TokenWarningLevel.NORMAL == "normal"
        assert TokenWarningLevel.CAUTION == "caution"
        assert TokenWarningLevel.WARNING == "warning"
        assert TokenWarningLevel.CRITICAL == "critical"
        assert TokenWarningLevel.OVERFLOW == "overflow"

    def test_warning_level_count(self):
        """Test the correct number of warning levels."""
        assert len(TokenWarningLevel) == 5


class TestTokenBudgetConfig:
    """Tests for TokenBudgetConfig dataclass."""

    def test_default_config(self):
        """Test default configuration values."""
        config = TokenBudgetConfig()
        assert config.max_tokens == 128000
        assert config.reserved_tokens == 4000
        assert config.warning_threshold == 0.70
        assert config.caution_threshold == 0.80
        assert config.critical_threshold == 0.90
        assert config.overflow_threshold == 0.95
        assert config.auto_summarize is True
        assert config.auto_prune is True

    def test_available_tokens(self):
        """Test available_tokens property."""
        config = TokenBudgetConfig(max_tokens=100000, reserved_tokens=5000)
        assert config.available_tokens == 95000

    def test_custom_config(self):
        """Test custom configuration values."""
        config = TokenBudgetConfig(
            max_tokens=64000,
            reserved_tokens=2000,
            warning_threshold=0.60,
            auto_summarize=False,
        )
        assert config.max_tokens == 64000
        assert config.reserved_tokens == 2000
        assert config.warning_threshold == 0.60
        assert config.auto_summarize is False


class TestTokenUsage:
    """Tests for TokenUsage dataclass."""

    def test_create_usage(self):
        """Test creating a token usage instance."""
        usage = TokenUsage(
            total_tokens=50000,
            available_tokens=124000,
            used_percentage=0.40,
            level=TokenWarningLevel.NORMAL,
            remaining_tokens=74000,
        )
        assert usage.total_tokens == 50000
        assert usage.level == TokenWarningLevel.NORMAL

    def test_usage_to_dict(self):
        """Test converting usage to dictionary."""
        usage = TokenUsage(
            total_tokens=100000,
            available_tokens=124000,
            used_percentage=0.806,
            level=TokenWarningLevel.WARNING,
            remaining_tokens=24000,
            session_id="test-session",
        )
        data = usage.to_dict()

        assert data["total_tokens"] == 100000
        assert data["used_percentage"] == 80.6
        assert data["level"] == "warning"
        assert data["session_id"] == "test-session"
        assert "timestamp" in data


class TestTokenBudget:
    """Tests for TokenBudget class."""

    @pytest.fixture
    def temp_store(self):
        """Create a temporary memory store."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = MemoryStore(base_path=Path(tmpdir), auto_save=False)
            yield store

    @pytest.fixture
    def budget(self, temp_store):
        """Create a token budget with the default config."""
        return TokenBudget(temp_store)

    @pytest.fixture
    def small_budget(self, temp_store):
        """Create a token budget with small limits for testing."""
        config = TokenBudgetConfig(
            max_tokens=1000,
            reserved_tokens=100,
            auto_summarize=False,
            auto_prune=False,
        )
        return TokenBudget(temp_store, config)

    # Basic Tests

    def test_create_budget(self, temp_store):
        """Test creating a token budget."""
        budget = TokenBudget(temp_store)
        assert budget.config.max_tokens == 128000

    def test_custom_config(self, temp_store):
        """Test budget with custom config."""
        config = TokenBudgetConfig(max_tokens=64000)
        budget = TokenBudget(temp_store, config)
        assert budget.config.max_tokens == 64000

    # Warning Level Tests

    def test_level_normal(self, small_budget, temp_store):
        """Test NORMAL level when under 70%."""
        # 900 available, 500 used = 55.5%
        temp_store.add(type=MemoryType.CONTEXT, content="A", tokens=500)
        usage = small_budget.get_usage()
        assert usage.level == TokenWarningLevel.NORMAL

    def test_level_caution(self, small_budget, temp_store):
        """Test CAUTION level at 70-80%."""
        # 900 available, 650 used = 72.2%
        temp_store.add(type=MemoryType.CONTEXT, content="A", tokens=650)
        usage = small_budget.get_usage()
        assert usage.level == TokenWarningLevel.CAUTION

    def test_level_warning(self, small_budget, temp_store):
        """Test WARNING level at 80-90%."""
        # 900 available, 750 used = 83.3%
        temp_store.add(type=MemoryType.CONTEXT, content="A", tokens=750)
        usage = small_budget.get_usage()
        assert usage.level == TokenWarningLevel.WARNING

    def test_level_critical(self, small_budget, temp_store):
        """Test CRITICAL level at 90-95%."""
        # 900 available, 820 used = 91.1%
        temp_store.add(type=MemoryType.CONTEXT, content="A", tokens=820)
        usage = small_budget.get_usage()
        assert usage.level == TokenWarningLevel.CRITICAL

    def test_level_overflow(self, small_budget, temp_store):
        """Test OVERFLOW level above 95%."""
        # 900 available, 870 used = 96.7%
        temp_store.add(type=MemoryType.CONTEXT, content="A", tokens=870)
        usage = small_budget.get_usage()
        assert usage.level == TokenWarningLevel.OVERFLOW

    # Usage Tests

    def test_get_usage_empty(self, budget):
        """Test getting usage when the store is empty."""
        usage = budget.get_usage()
        assert usage.total_tokens == 0
        assert usage.level == TokenWarningLevel.NORMAL
        assert usage.used_percentage == 0.0

    def test_get_usage_by_session(self, budget, temp_store):
        """Test getting usage for a specific session."""
        temp_store.add(
            type=MemoryType.CONTEXT,
            content="A",
            tokens=1000,
            session_id="s1",
        )
        temp_store.add(
            type=MemoryType.CONTEXT,
            content="B",
            tokens=2000,
            session_id="s2",
        )

        usage = budget.get_usage("s1")
        assert usage.total_tokens == 1000
        assert usage.session_id == "s1"

    def test_remaining_tokens(self, small_budget, temp_store):
        """Test remaining tokens' calculation."""
        temp_store.add(type=MemoryType.CONTEXT, content="A", tokens=400)
        usage = small_budget.get_usage()
        # 900 available - 400 used = 500 remaining
        assert usage.remaining_tokens == 500

    # Check Budget Tests

    def test_check_budget_ok(self, small_budget, temp_store):
        """Test check_budget when addition is OK."""
        temp_store.add(type=MemoryType.CONTEXT, content="A", tokens=400)
        can_add, usage = small_budget.check_budget(200)
        assert can_add is True

    def test_check_budget_overflow(self, small_budget, temp_store):
        """Test check_budget when addition would overflow."""
        temp_store.add(type=MemoryType.CONTEXT, content="A", tokens=800)
        can_add, usage = small_budget.check_budget(100)
        assert can_add is False

    # Reserve Tokens Tests

    def test_reserve_tokens_ok(self, small_budget, temp_store):
        """Test successful token reservation."""
        temp_store.add(type=MemoryType.CONTEXT, content="A", tokens=400)
        result = small_budget.reserve_tokens(200)
        assert result is True

    def test_reserve_tokens_overflow(self, small_budget, temp_store):
        """Test failed token reservation."""
        temp_store.add(type=MemoryType.CONTEXT, content="A", tokens=800)
        result = small_budget.reserve_tokens(200)
        assert result is False

    # Callback Tests

    def test_warning_callback(self, temp_store):
        """Test warning callback is triggered."""
        warning_called = []

        def on_warning(usage):
            warning_called.append(usage)

        config = TokenBudgetConfig(
            max_tokens=1000,
            reserved_tokens=100,
            auto_summarize=False,
        )
        budget = TokenBudget(temp_store, config, on_warning=on_warning)

        # First usage - normal level
        temp_store.add(type=MemoryType.CONTEXT, content="A", tokens=700)
        budget.get_usage()

        # Add more to trigger warning
        temp_store.add(type=MemoryType.CONTEXT, content="B", tokens=50)
        budget.get_usage()

        assert len(warning_called) == 1

    def test_critical_callback(self, temp_store):
        """Test critical callback is triggered."""
        critical_called = []

        def on_critical(usage):
            critical_called.append(usage)

        config = TokenBudgetConfig(
            max_tokens=1000,
            reserved_tokens=100,
            auto_summarize=False,
        )
        budget = TokenBudget(temp_store, config, on_critical=on_critical)

        # Add tokens to trigger critical
        temp_store.add(type=MemoryType.CONTEXT, content="A", tokens=820)
        budget.get_usage()

        assert len(critical_called) == 1

    # Recommendations Tests

    def test_recommendations_normal(self, budget):
        """Test recommendations at NORMAL level."""
        recs = budget.get_recommendations()
        assert "no action needed" in recs[0].lower()

    def test_recommendations_warning(self, small_budget, temp_store):
        """Test recommendations at WARNING level."""
        temp_store.add(type=MemoryType.CONTEXT, content="A", tokens=750)
        recs = small_budget.get_recommendations()
        assert any("summariz" in r.lower() for r in recs)

    def test_recommendations_critical(self, small_budget, temp_store):
        """Test recommendations at CRITICAL level."""
        temp_store.add(type=MemoryType.CONTEXT, content="A", tokens=820)
        recs = small_budget.get_recommendations()
        assert any("urgent" in r.lower() for r in recs)

    # Format Status Tests

    def test_format_status(self, budget):
        """Test status formatting."""
        status = budget.format_status()
        assert "Token Budget Status" in status
        assert "Level" in status
        assert "Used" in status
        assert "Recommendations" in status

    def test_format_status_with_session(self, budget, temp_store):
        """Test status formatting with session."""
        temp_store.add(
            type=MemoryType.CONTEXT,
            content="A",
            tokens=1000,
            session_id="test-session",
        )
        status = budget.format_status("test-session")
        assert "Token Budget Status" in status


class TestTokenBudgetAutoPrune:
    """Tests for auto-pruning functionality."""

    @pytest.fixture
    def temp_store(self):
        """Create a temporary memory store."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = MemoryStore(base_path=Path(tmpdir), auto_save=False)
            yield store

    def test_auto_prune_on_overflow(self, temp_store):
        """Test auto pruning when overflow is triggered."""
        config = TokenBudgetConfig(
            max_tokens=1000,
            reserved_tokens=100,
            auto_summarize=False,
            auto_prune=True,
        )
        budget = TokenBudget(temp_store, config)

        # Add ephemeral entries
        temp_store.add(
            type=MemoryType.CONTEXT,
            content="Ephemeral",
            tokens=100,
            priority=MemoryPriority.EPHEMERAL,
        )

        # Add enough to trigger overflow
        temp_store.add(
            type=MemoryType.CONTEXT,
            content="Main",
            tokens=800,
            priority=MemoryPriority.NORMAL,
        )

        # Get usage should trigger auto prune
        _ = budget.get_usage()

        # After pruning, ephemeral entries should be removed
        ephemeral = temp_store.query(
            type=MemoryType.CONTEXT,
            max_priority=MemoryPriority.EPHEMERAL,
        )
        assert len(ephemeral) == 0
