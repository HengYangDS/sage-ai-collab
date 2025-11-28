"""
Unit tests for timeout_manager module.

Tests cover:
- TimeoutLevel enum
- CircuitState enum
- TimeoutConfig class
- CircuitBreakerConfig class
- TimeoutResult class
- CircuitBreaker class
- TimeoutManager class
- Convenience functions
"""

import asyncio
import sys
import time
from pathlib import Path

import pytest

# Add the tools directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from timeout_manager import (
    EMBEDDED_CORE,
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitState,
    TimeoutConfig,
    TimeoutLevel,
    TimeoutManager,
    TimeoutResult,
    get_default_timeout_manager,
    get_timeout_manager,
)


class TestTimeoutLevel:
    """Tests for TimeoutLevel enum."""

    def test_timeout_levels_exist(self):
        """All 5 timeout levels should exist."""
        assert TimeoutLevel.T1_CACHE.value == 1
        assert TimeoutLevel.T2_FILE.value == 2
        assert TimeoutLevel.T3_LAYER.value == 3
        assert TimeoutLevel.T4_FULL.value == 4
        assert TimeoutLevel.T5_ANALYSIS.value == 5

    def test_timeout_level_count(self):
        """Should have exactly 5 levels."""
        assert len(TimeoutLevel) == 5


class TestCircuitState:
    """Tests for CircuitState enum."""

    def test_circuit_states_exist(self):
        """All 3 circuit states should exist."""
        assert CircuitState.CLOSED.value == "closed"
        assert CircuitState.OPEN.value == "open"
        assert CircuitState.HALF_OPEN.value == "half_open"

    def test_circuit_state_count(self):
        """Should have exactly 3 states."""
        assert len(CircuitState) == 3


class TestTimeoutConfig:
    """Tests for TimeoutConfig dataclass."""

    def test_default_values(self):
        """Default timeout values should match spec."""
        config = TimeoutConfig()
        assert config.cache_ms == 100
        assert config.file_ms == 500
        assert config.layer_ms == 2000
        assert config.full_ms == 5000
        assert config.analysis_ms == 10000
        assert config.mcp_ms == 10000

    def test_custom_values(self):
        """Custom timeout values should be set correctly."""
        config = TimeoutConfig(
            cache_ms=200,
            file_ms=1000,
            layer_ms=3000,
            full_ms=8000,
            analysis_ms=15000,
            mcp_ms=12000,
        )
        assert config.cache_ms == 200
        assert config.file_ms == 1000
        assert config.layer_ms == 3000
        assert config.full_ms == 8000
        assert config.analysis_ms == 15000
        assert config.mcp_ms == 12000

    def test_get_timeout_all_levels(self):
        """get_timeout should return correct seconds for each level."""
        config = TimeoutConfig()
        assert config.get_timeout(TimeoutLevel.T1_CACHE) == 0.1
        assert config.get_timeout(TimeoutLevel.T2_FILE) == 0.5
        assert config.get_timeout(TimeoutLevel.T3_LAYER) == 2.0
        assert config.get_timeout(TimeoutLevel.T4_FULL) == 5.0
        assert config.get_timeout(TimeoutLevel.T5_ANALYSIS) == 10.0

    def test_get_timeout_custom_config(self):
        """get_timeout should work with custom config."""
        config = TimeoutConfig(cache_ms=250, file_ms=750)
        assert config.get_timeout(TimeoutLevel.T1_CACHE) == 0.25
        assert config.get_timeout(TimeoutLevel.T2_FILE) == 0.75


class TestCircuitBreakerConfig:
    """Tests for CircuitBreakerConfig dataclass."""

    def test_default_values(self):
        """Default circuit breaker config values."""
        config = CircuitBreakerConfig()
        assert config.failure_threshold == 3
        assert config.reset_timeout_s == 30.0
        assert config.half_open_max_calls == 1

    def test_custom_values(self):
        """Custom circuit breaker config values."""
        config = CircuitBreakerConfig(
            failure_threshold=5,
            reset_timeout_s=60.0,
            half_open_max_calls=3,
        )
        assert config.failure_threshold == 5
        assert config.reset_timeout_s == 60.0
        assert config.half_open_max_calls == 3


class TestTimeoutResult:
    """Tests for TimeoutResult dataclass."""

    def test_success_result(self):
        """Successful result should have correct attributes."""
        result = TimeoutResult(
            success=True,
            value="test_value",
            duration_ms=100,
            timeout_ms=5000,
        )
        assert result.success is True
        assert result.value == "test_value"
        assert result.error is None
        assert result.duration_ms == 100
        assert result.timeout_ms == 5000
        assert result.partial is False
        assert result.fallback_used is False

    def test_failure_result(self):
        """Failed result should have correct attributes."""
        result = TimeoutResult(
            success=False,
            error="Timeout occurred",
            duration_ms=5001,
            timeout_ms=5000,
            fallback_used=True,
            value="fallback_value",
        )
        assert result.success is False
        assert result.error == "Timeout occurred"
        assert result.fallback_used is True
        assert result.value == "fallback_value"

    def test_to_dict(self):
        """to_dict should return correct dictionary."""
        result = TimeoutResult(
            success=True,
            value="test",
            error=None,
            duration_ms=50,
            timeout_ms=100,
            partial=True,
            fallback_used=False,
        )
        d = result.to_dict()
        assert d["success"] is True
        assert d["value"] == "test"
        assert d["error"] is None
        assert d["duration_ms"] == 50
        assert d["timeout_ms"] == 100
        assert d["partial"] is True
        assert d["fallback_used"] is False


class TestCircuitBreaker:
    """Tests for CircuitBreaker class."""

    def test_initial_state_closed(self):
        """Circuit breaker should start in CLOSED state."""
        cb = CircuitBreaker()
        assert cb.state == CircuitState.CLOSED

    def test_record_success_resets_failures(self):
        """Recording success should reset failure count."""
        cb = CircuitBreaker()
        cb._failure_count = 2
        cb.record_success()
        assert cb._failure_count == 0

    def test_record_failure_increments_count(self):
        """Recording failure should increment count."""
        cb = CircuitBreaker()
        cb.record_failure()
        assert cb._failure_count == 1
        cb.record_failure()
        assert cb._failure_count == 2

    def test_circuit_opens_after_threshold(self):
        """Circuit should open after reaching failure threshold."""
        config = CircuitBreakerConfig(failure_threshold=3)
        cb = CircuitBreaker(config)

        cb.record_failure()
        cb.record_failure()
        assert cb.state == CircuitState.CLOSED

        cb.record_failure()  # 3rd failure
        assert cb._state == CircuitState.OPEN

    def test_allow_request_when_closed(self):
        """Should allow requests when closed."""
        cb = CircuitBreaker()
        assert cb.allow_request() is True

    def test_reject_request_when_open(self):
        """Should reject requests when open."""
        cb = CircuitBreaker()
        cb._state = CircuitState.OPEN
        cb._last_failure_time = time.monotonic()  # Recent failure
        assert cb.allow_request() is False

    def test_half_open_allows_limited_requests(self):
        """Half-open state should allow limited requests."""
        config = CircuitBreakerConfig(half_open_max_calls=2)
        cb = CircuitBreaker(config)
        cb._state = CircuitState.HALF_OPEN

        assert cb.allow_request() is True  # 1st call
        assert cb.allow_request() is True  # 2nd call
        assert cb.allow_request() is False  # 3rd call rejected

    def test_half_open_success_closes_circuit(self):
        """Success in half-open state should close circuit."""
        cb = CircuitBreaker()
        cb._state = CircuitState.HALF_OPEN
        cb.record_success()
        assert cb._state == CircuitState.CLOSED

    def test_half_open_failure_opens_circuit(self):
        """Failure in half-open state should open circuit."""
        cb = CircuitBreaker()
        cb._state = CircuitState.HALF_OPEN
        cb.record_failure()
        assert cb._state == CircuitState.OPEN

    def test_auto_reset_after_timeout(self):
        """Circuit should transition to half-open after reset timeout."""
        config = CircuitBreakerConfig(reset_timeout_s=0.01)  # 10ms
        cb = CircuitBreaker(config)
        cb._state = CircuitState.OPEN
        cb._last_failure_time = time.monotonic() - 0.02  # 20ms ago

        # Accessing state should trigger transition
        assert cb.state == CircuitState.HALF_OPEN

    def test_reset_method(self):
        """Manual reset should restore initial state."""
        cb = CircuitBreaker()
        cb._state = CircuitState.OPEN
        cb._failure_count = 5
        cb._last_failure_time = time.monotonic()
        cb._half_open_calls = 3

        cb.reset()

        assert cb._state == CircuitState.CLOSED
        assert cb._failure_count == 0
        assert cb._last_failure_time is None
        assert cb._half_open_calls == 0


class TestTimeoutManager:
    """Tests for TimeoutManager class."""

    def test_default_initialization(self):
        """Should initialize with default configs."""
        tm = TimeoutManager()
        assert tm.timeout_config is not None
        assert tm.circuit_breaker is not None
        assert tm._fallbacks == {}

    def test_custom_initialization(self):
        """Should accept custom configs."""
        timeout_config = TimeoutConfig(cache_ms=200)
        circuit_config = CircuitBreakerConfig(failure_threshold=5)
        tm = TimeoutManager(timeout_config, circuit_config)

        assert tm.timeout_config.cache_ms == 200
        assert tm.circuit_breaker.config.failure_threshold == 5

    def test_register_fallback(self):
        """Should register fallback functions."""
        tm = TimeoutManager()
        tm.register_fallback("test", lambda: "fallback_value")
        assert "test" in tm._fallbacks

    def test_get_fallback_exists(self):
        """Should return fallback value when key exists."""
        tm = TimeoutManager()
        tm.register_fallback("test", lambda: "fallback_value")
        assert tm.get_fallback("test") == "fallback_value"

    def test_get_fallback_not_exists(self):
        """Should return None when key doesn't exist."""
        tm = TimeoutManager()
        assert tm.get_fallback("nonexistent") is None

    @pytest.mark.asyncio
    async def test_execute_with_timeout_success(self):
        """Should return success result for fast operations."""
        tm = TimeoutManager()

        async def fast_operation():
            return "result"

        result = await tm.execute_with_timeout(
            fast_operation(),
            TimeoutLevel.T2_FILE,
        )

        assert result.success is True
        assert result.value == "result"
        assert result.error is None

    @pytest.mark.asyncio
    async def test_execute_with_timeout_timeout(self):
        """Should return failure result on timeout."""
        tm = TimeoutManager()

        async def slow_operation():
            await asyncio.sleep(1)
            return "result"

        result = await tm.execute_with_timeout(
            slow_operation(),
            TimeoutLevel.T1_CACHE,  # 100ms timeout
        )

        assert result.success is False
        assert "Timeout" in result.error

    @pytest.mark.asyncio
    async def test_execute_with_timeout_custom_timeout(self):
        """Should respect custom timeout_ms parameter."""
        tm = TimeoutManager()

        async def medium_operation():
            await asyncio.sleep(0.15)
            return "result"

        # Should fail with 100ms timeout
        result = await tm.execute_with_timeout(
            medium_operation(),
            TimeoutLevel.T1_CACHE,
            timeout_ms=100,
        )
        assert result.success is False

        # Should succeed with 500ms timeout
        result = await tm.execute_with_timeout(
            medium_operation(),
            TimeoutLevel.T1_CACHE,
            timeout_ms=500,
        )
        assert result.success is True

    @pytest.mark.asyncio
    async def test_execute_with_timeout_fallback(self):
        """Should use fallback on timeout when registered."""
        tm = TimeoutManager()
        tm.register_fallback("slow_op", lambda: "fallback_result")

        async def slow_operation():
            await asyncio.sleep(1)
            return "result"

        result = await tm.execute_with_timeout(
            slow_operation(),
            TimeoutLevel.T1_CACHE,
            fallback_key="slow_op",
        )

        assert result.success is False
        assert result.value == "fallback_result"
        assert result.fallback_used is True

    @pytest.mark.asyncio
    async def test_execute_with_timeout_exception(self):
        """Should handle exceptions gracefully."""
        tm = TimeoutManager()

        async def failing_operation():
            raise ValueError("Test error")

        result = await tm.execute_with_timeout(
            failing_operation(),
            TimeoutLevel.T2_FILE,
        )

        assert result.success is False
        assert "Test error" in result.error

    @pytest.mark.asyncio
    async def test_execute_with_timeout_circuit_breaker_open(self):
        """Should use fallback when circuit breaker is open."""
        tm = TimeoutManager()
        tm.register_fallback("test", lambda: "cb_fallback")
        tm.circuit_breaker._state = CircuitState.OPEN
        tm.circuit_breaker._last_failure_time = time.monotonic()

        async def operation():
            return "result"

        # TimeoutManager now automatically closes the coroutine when circuit breaker is open
        result = await tm.execute_with_timeout(
            operation(),
            TimeoutLevel.T2_FILE,
            fallback_key="test",
        )

        assert result.success is False
        assert result.value == "cb_fallback"
        assert "Circuit breaker open" in result.error

    @pytest.mark.asyncio
    async def test_timeout_decorator(self):
        """Timeout decorator should wrap async functions."""
        tm = TimeoutManager()

        @tm.timeout_decorator(TimeoutLevel.T2_FILE)
        async def decorated_function():
            return "decorated_result"

        result = await decorated_function()

        assert result.success is True
        assert result.value == "decorated_result"

    @pytest.mark.asyncio
    async def test_timeout_decorator_with_timeout(self):
        """Timeout decorator should handle timeouts."""
        tm = TimeoutManager()

        @tm.timeout_decorator(TimeoutLevel.T1_CACHE)
        async def slow_decorated():
            await asyncio.sleep(1)
            return "result"

        result = await slow_decorated()

        assert result.success is False
        assert "Timeout" in result.error


class TestConvenienceFunctions:
    """Tests for module-level convenience functions."""

    def test_get_default_timeout_manager(self):
        """Should return pre-configured manager."""
        tm = get_default_timeout_manager()

        assert isinstance(tm, TimeoutManager)
        assert tm.get_fallback("core") is not None
        assert tm.get_fallback("index") is not None

    def test_get_default_timeout_manager_core_fallback(self):
        """Core fallback should contain Xin-Da-Ya."""
        tm = get_default_timeout_manager()
        core_content = tm.get_fallback("core")

        assert "Xin-Da-Ya" in core_content
        assert "信达雅" in core_content

    def test_get_timeout_manager_singleton(self):
        """Should return singleton instance."""
        import timeout_manager as tm_module

        # Reset singleton
        tm_module._default_manager = None

        tm1 = get_timeout_manager()
        tm2 = get_timeout_manager()

        assert tm1 is tm2

    def test_embedded_core_content(self):
        """EMBEDDED_CORE should contain essential content."""
        assert "Xin-Da-Ya" in EMBEDDED_CORE
        assert "5 Critical Questions" in EMBEDDED_CORE
        assert "Autonomy Levels" in EMBEDDED_CORE
        assert "Emergency Fallback" in EMBEDDED_CORE
