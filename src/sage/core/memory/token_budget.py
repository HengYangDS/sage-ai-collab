"""Token budget management for memory persistence.

This module provides token usage tracking and automatic actions when
thresholds are exceeded (summarization, pruning, handoff).

Version: 0.1.0
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, Optional

if TYPE_CHECKING:
    from sage.core.memory.store import MemoryStore

logger = logging.getLogger(__name__)


class TokenWarningLevel(str, Enum):
    """Warning levels for token usage.

    Levels indicate the urgency of action needed based on
    current token consumption relative to budget.
    """

    NORMAL = "normal"  # < 70% - No action needed
    CAUTION = "caution"  # 70-80% - Suggest summarization
    WARNING = "warning"  # 80-90% - Recommend summarization
    CRITICAL = "critical"  # 90-95% - Auto-summarize
    OVERFLOW = "overflow"  # > 95% - Force pruning


@dataclass
class TokenBudgetConfig:
    """Configuration for token budget management.

    Attributes:
        max_tokens: Maximum tokens in model context window.
        reserved_tokens: Tokens reserved for response generation.
        warning_threshold: Threshold for CAUTION level (default: 70%).
        caution_threshold: Threshold for WARNING level (default: 80%).
        critical_threshold: Threshold for CRITICAL level (default: 90%).
        overflow_threshold: Threshold for OVERFLOW level (default: 95%).
        auto_summarize: Whether to auto-summarize at CRITICAL level.
        auto_prune: Whether to auto-prune at OVERFLOW level.
    """

    max_tokens: int = 128000  # Model context window
    reserved_tokens: int = 4000  # Reserved for response
    warning_threshold: float = 0.70  # 70% - start monitoring
    caution_threshold: float = 0.80  # 80% - suggest summarization
    critical_threshold: float = 0.90  # 90% - auto-summarize
    overflow_threshold: float = 0.95  # 95% - force pruning
    auto_summarize: bool = True
    auto_prune: bool = True

    @property
    def available_tokens(self) -> int:
        """Get available tokens after reserving for response."""
        return self.max_tokens - self.reserved_tokens


@dataclass
class TokenUsage:
    """Current token usage statistics.

    Attributes:
        total_tokens: Total tokens currently used.
        available_tokens: Maximum available tokens.
        used_percentage: Percentage of budget used.
        level: Current warning level.
        remaining_tokens: Tokens remaining before overflow.
    """

    total_tokens: int
    available_tokens: int
    used_percentage: float
    level: TokenWarningLevel
    remaining_tokens: int
    session_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "total_tokens": self.total_tokens,
            "available_tokens": self.available_tokens,
            "used_percentage": round(self.used_percentage * 100, 1),
            "level": self.level.value,
            "remaining_tokens": self.remaining_tokens,
            "session_id": self.session_id,
            "timestamp": self.timestamp.isoformat(),
        }


class TokenBudget:
    """Token budget controller with automatic actions.

    Monitors token usage and triggers appropriate actions when
    thresholds are exceeded:
    - CAUTION: Suggests summarization
    - WARNING: Recommends summarization and task handoff
    - CRITICAL: Auto-summarizes if enabled
    - OVERFLOW: Force prunes low-priority entries

    Example:
        >>> store = MemoryStore()
        >>> budget = TokenBudget(store, TokenBudgetConfig(max_tokens=128000))
        >>> usage = budget.get_usage("session_123")
        >>> if usage.level == TokenWarningLevel.WARNING:
        ...     print("Consider summarizing or handing off")
    """

    def __init__(
        self,
        store: MemoryStore,
        config: Optional[TokenBudgetConfig] = None,
        on_warning: Optional[Callable[[TokenUsage], None]] = None,
        on_critical: Optional[Callable[[TokenUsage], None]] = None,
        on_overflow: Optional[Callable[[TokenUsage], None]] = None,
    ) -> None:
        """Initialize the token budget controller.

        Args:
            store: The memory store to monitor.
            config: Budget configuration. Defaults to standard config.
            on_warning: Callback for WARNING level.
            on_critical: Callback for CRITICAL level.
            on_overflow: Callback for OVERFLOW level.
        """
        self._store = store
        self._config = config or TokenBudgetConfig()
        self._on_warning = on_warning
        self._on_critical = on_critical
        self._on_overflow = on_overflow
        self._last_level: dict[str, TokenWarningLevel] = {}

    @property
    def config(self) -> TokenBudgetConfig:
        """Get the budget configuration."""
        return self._config

    def _calculate_level(self, used_percentage: float) -> TokenWarningLevel:
        """Calculate warning level from usage percentage."""
        if used_percentage >= self._config.overflow_threshold:
            return TokenWarningLevel.OVERFLOW
        elif used_percentage >= self._config.critical_threshold:
            return TokenWarningLevel.CRITICAL
        elif used_percentage >= self._config.caution_threshold:
            return TokenWarningLevel.WARNING
        elif used_percentage >= self._config.warning_threshold:
            return TokenWarningLevel.CAUTION
        else:
            return TokenWarningLevel.NORMAL

    def get_usage(self, session_id: Optional[str] = None) -> TokenUsage:
        """Get current token usage statistics.

        Args:
            session_id: Optional session to get usage for.

        Returns:
            Current token usage information.
        """
        total_tokens = self._store.get_total_tokens(session_id)
        available = self._config.available_tokens
        used_percentage = total_tokens / available if available > 0 else 0.0
        level = self._calculate_level(used_percentage)
        remaining = max(0, available - total_tokens)

        usage = TokenUsage(
            total_tokens=total_tokens,
            available_tokens=available,
            used_percentage=used_percentage,
            level=level,
            remaining_tokens=remaining,
            session_id=session_id,
        )

        # Trigger callbacks if level changed
        cache_key = session_id or "_global_"
        last_level = self._last_level.get(cache_key, TokenWarningLevel.NORMAL)

        if level != last_level:
            self._last_level[cache_key] = level
            self._handle_level_change(usage, last_level)

        return usage

    def _handle_level_change(
        self,
        usage: TokenUsage,
        previous_level: TokenWarningLevel,
    ) -> None:
        """Handle level change by triggering appropriate callbacks."""
        level = usage.level

        # Log level changes
        if level.value != previous_level.value:
            logger.info(
                f"Token budget level changed: {previous_level.value} -> {level.value} "
                f"({usage.used_percentage:.1%} used)"
            )

        # Trigger callbacks
        if level == TokenWarningLevel.WARNING and self._on_warning:
            self._on_warning(usage)
        elif level == TokenWarningLevel.CRITICAL:
            if self._on_critical:
                self._on_critical(usage)
            if self._config.auto_summarize:
                self._auto_summarize(usage)
        elif level == TokenWarningLevel.OVERFLOW:
            if self._on_overflow:
                self._on_overflow(usage)
            if self._config.auto_prune:
                self._auto_prune(usage)

    def _auto_summarize(self, usage: TokenUsage) -> None:
        """Auto-summarize when at CRITICAL level.

        This is a placeholder that logs the need for summarization.
        Actual summarization requires AI integration.
        """
        logger.warning(
            f"Token budget CRITICAL ({usage.used_percentage:.1%}). "
            f"Auto-summarization recommended for session: {usage.session_id}"
        )
        # Note: Actual summarization would require AI integration
        # This could emit an event for external handling

    def _auto_prune(self, usage: TokenUsage) -> None:
        """Auto-prune low-priority entries when at OVERFLOW level."""
        from sage.core.memory.store import MemoryPriority

        logger.warning(
            f"Token budget OVERFLOW ({usage.used_percentage:.1%}). "
            f"Auto-pruning low-priority entries for session: {usage.session_id}"
        )

        # Prune EPHEMERAL entries first
        pruned = self._store.prune(
            max_priority=MemoryPriority.EPHEMERAL,
            session_id=usage.session_id,
        )
        logger.info(f"Pruned {pruned} EPHEMERAL entries")

        # Check if more pruning needed
        new_usage = self.get_usage(usage.session_id)
        if new_usage.level == TokenWarningLevel.OVERFLOW:
            # Prune LOW priority entries
            pruned = self._store.prune(
                max_priority=MemoryPriority.LOW,
                session_id=usage.session_id,
            )
            logger.info(f"Pruned {pruned} LOW priority entries")

    def check_budget(
        self,
        additional_tokens: int,
        session_id: Optional[str] = None,
    ) -> tuple[bool, TokenUsage]:
        """Check if adding tokens would exceed budget.

        Args:
            additional_tokens: Number of tokens to potentially add.
            session_id: Optional session to check.

        Returns:
            Tuple of (can_add, current_usage).
        """
        current = self.get_usage(session_id)
        projected_total = current.total_tokens + additional_tokens
        projected_percentage = projected_total / current.available_tokens

        can_add = projected_percentage < self._config.overflow_threshold
        return can_add, current

    def reserve_tokens(
        self,
        tokens: int,
        session_id: Optional[str] = None,
    ) -> bool:
        """Reserve tokens for upcoming content.

        Args:
            tokens: Number of tokens to reserve.
            session_id: Optional session to reserve for.

        Returns:
            True if reservation successful, False if would overflow.
        """
        can_add, usage = self.check_budget(tokens, session_id)

        if not can_add:
            logger.warning(
                f"Cannot reserve {tokens} tokens - would exceed budget "
                f"(current: {usage.used_percentage:.1%})"
            )

        return can_add

    def get_recommendations(
        self,
        session_id: Optional[str] = None,
    ) -> list[str]:
        """Get recommendations based on current usage.

        Args:
            session_id: Optional session to get recommendations for.

        Returns:
            List of recommended actions.
        """
        usage = self.get_usage(session_id)
        recommendations = []

        if usage.level == TokenWarningLevel.NORMAL:
            recommendations.append("Token budget healthy - no action needed")
        elif usage.level == TokenWarningLevel.CAUTION:
            recommendations.append("Consider summarizing older context")
            recommendations.append("Review and remove low-priority memories")
        elif usage.level == TokenWarningLevel.WARNING:
            recommendations.append("Recommend summarizing conversation history")
            recommendations.append("Consider creating a checkpoint")
            recommendations.append("Prepare for potential task handoff")
        elif usage.level == TokenWarningLevel.CRITICAL:
            recommendations.append("URGENT: Summarize context immediately")
            recommendations.append("Create checkpoint before continuing")
            recommendations.append("Prepare handoff package")
        elif usage.level == TokenWarningLevel.OVERFLOW:
            recommendations.append("CRITICAL: Token budget exceeded")
            recommendations.append("Emergency pruning in progress")
            recommendations.append("Immediate task handoff required")

        return recommendations

    def format_status(self, session_id: Optional[str] = None) -> str:
        """Format a human-readable status report.

        Args:
            session_id: Optional session to report on.

        Returns:
            Formatted status string.
        """
        usage = self.get_usage(session_id)
        recommendations = self.get_recommendations(session_id)

        status_icon = {
            TokenWarningLevel.NORMAL: "✅",
            TokenWarningLevel.CAUTION: "⚠️",
            TokenWarningLevel.WARNING: "🟠",
            TokenWarningLevel.CRITICAL: "🔴",
            TokenWarningLevel.OVERFLOW: "💥",
        }

        lines = [
            f"## Token Budget Status {status_icon.get(usage.level, '❓')}",
            "",
            f"**Level**: {usage.level.value.upper()}",
            f"**Used**: {usage.total_tokens:,} / {usage.available_tokens:,} "
            f"({usage.used_percentage:.1%})",
            f"**Remaining**: {usage.remaining_tokens:,} tokens",
            "",
            "### Recommendations",
        ]

        for rec in recommendations:
            lines.append(f"- {rec}")

        return "\n".join(lines)
