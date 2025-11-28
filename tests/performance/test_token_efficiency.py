"""Token efficiency measurement tests.

This module measures the actual token saving efficiency of SAGE's
TokenBudget system by simulating real AI conversation scenarios.

Version: 0.1.0
"""

from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path

from sage.core.memory.store import MemoryPriority, MemoryStore, MemoryType
from sage.core.memory.token_budget import (
    TokenBudget,
    TokenBudgetConfig,
    TokenWarningLevel,
)


@dataclass
class EfficiencyResult:
    """Token efficiency measurement result."""

    scenario: str
    original_tokens: int
    optimized_tokens: int
    saved_tokens: int
    saving_percentage: float
    entries_before: int
    entries_after: int
    pruned_entries: int


def estimate_tokens(text: str) -> int:
    """Estimate token count for text (approx 4 chars per token)."""
    return max(1, len(text) // 4)


def create_conversation_entries() -> list[dict]:
    """Create simulated conversation entries with realistic token distribution.

    Design rationale (方案 3):
    - Low priority entries (EPHEMERAL/LOW) are verbose logs and routine messages
    - High priority entries (NORMAL/HIGH/CRITICAL) are concise, distilled information

    This reflects real-world AI collaboration where:
    - Debug logs and routine interactions are verbose but low-value
    - Important decisions and critical context are concise but high-value

    Expected token distribution:
    - EPHEMERAL: ~100 tokens/entry × 20 = 2000 tokens (40%)
    - LOW: ~80 tokens/entry × 15 = 1200 tokens (24%)
    - NORMAL: ~50 tokens/entry × 25 = 1250 tokens (25%)
    - HIGH: ~30 tokens/entry × 10 = 300 tokens (6%)
    - CRITICAL: ~20 tokens/entry × 5 = 100 tokens (2%)
    - Total: ~4850 tokens

    Pruning EPHEMERAL + LOW should save: 3200/4850 = ~66%
    """
    entries = []

    # Ephemeral entries (verbose debug logs, ~100 tokens each)
    for i in range(20):
        content = (
            f"Debug log {i}: Processing request at step {i}. "
            f"Current system state: memory_usage=45.2%, cpu_load=23.1%, "
            f"active_connections=142, pending_tasks=7. "
            f"Request details: method=POST, endpoint=/api/v2/process, "
            f"payload_size=2.3KB, auth_token=valid, rate_limit_remaining=847. "
            f"Processing pipeline: validation_passed=true, preprocessing_time=12ms, "
            f"queue_position=3, estimated_completion=250ms. "
            f"No errors detected in this iteration. Status: OK."
        )
        entries.append({
            "type": MemoryType.CONVERSATION,
            "content": content,
            "priority": MemoryPriority.EPHEMERAL,
            "tokens": estimate_tokens(content),
        })

    # Low priority entries (routine messages, ~80 tokens each)
    for i in range(15):
        content = (
            f"User inquiry #{i}: Asked about feature configuration options. "
            f"Provided comprehensive response covering: installation steps, "
            f"configuration parameters, common use cases, troubleshooting tips, "
            f"and links to documentation sections 3.2, 4.1, and 5.7. "
            f"User confirmed understanding. No follow-up questions. "
            f"Session duration: 3m 24s. Satisfaction: not rated."
        )
        entries.append({
            "type": MemoryType.CONVERSATION,
            "content": content,
            "priority": MemoryPriority.LOW,
            "tokens": estimate_tokens(content),
        })

    # Normal priority entries (concise context, ~50 tokens each)
    for i in range(25):
        content = (
            f"Context {i}: Module handles edge case with error retry. "
            f"Uses exponential backoff. Max 3 attempts. Logs failures."
        )
        entries.append({
            "type": MemoryType.CONTEXT,
            "content": content,
            "priority": MemoryPriority.NORMAL,
            "tokens": estimate_tokens(content),
        })

    # High priority entries (key decisions, ~30 tokens each)
    for i in range(10):
        content = (
            f"Decision {i}: Use async processing for better scalability. "
            f"Approved by architecture review."
        )
        entries.append({
            "type": MemoryType.DECISION,
            "content": content,
            "priority": MemoryPriority.HIGH,
            "tokens": estimate_tokens(content),
        })

    # Critical entries (essential facts, ~20 tokens each)
    for i in range(5):
        content = f"CRITICAL {i}: API key rotation required every 90 days."
        entries.append({
            "type": MemoryType.CONTEXT,
            "content": content,
            "priority": MemoryPriority.CRITICAL,
            "tokens": estimate_tokens(content),
        })

    return entries


def measure_no_optimization() -> tuple[int, int]:
    """Measure token usage without any optimization."""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = MemoryStore(base_path=Path(tmpdir), auto_save=False)
        entries = create_conversation_entries()

        for entry in entries:
            store.add(**entry, session_id="test-session")

        total_tokens = store.get_total_tokens()
        entry_count = len(store.query())

        return total_tokens, entry_count


def measure_with_auto_prune(budget_tokens: int) -> tuple[int, int, int]:
    """Measure token usage with auto-pruning enabled.

    Args:
        budget_tokens: Maximum token budget (triggers pruning when exceeded).

    Returns:
        Tuple of (final_tokens, final_entry_count, pruned_count).
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        store = MemoryStore(base_path=Path(tmpdir), auto_save=False)

        # Configure small budget to trigger pruning
        config = TokenBudgetConfig(
            max_tokens=budget_tokens + 100,  # +100 for reserved
            reserved_tokens=100,
            warning_threshold=0.60,
            caution_threshold=0.70,
            critical_threshold=0.80,
            overflow_threshold=0.90,
            auto_summarize=False,  # Disable for this test
            auto_prune=True,
        )
        budget = TokenBudget(store, config)

        entries = create_conversation_entries()
        initial_count = len(entries)

        for entry in entries:
            store.add(**entry, session_id="test-session")
            # Check budget after each add to trigger pruning if needed
            usage = budget.get_usage("test-session")
            if usage.level == TokenWarningLevel.OVERFLOW:
                # Prune will be triggered automatically
                pass

        final_tokens = store.get_total_tokens()
        final_count = len(store.query())
        pruned_count = initial_count - final_count

        return final_tokens, final_count, pruned_count


def measure_manual_prune_by_priority() -> EfficiencyResult:
    """Measure efficiency when pruning by priority levels."""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = MemoryStore(base_path=Path(tmpdir), auto_save=False)
        entries = create_conversation_entries()

        for entry in entries:
            store.add(**entry, session_id="test-session")

        original_tokens = store.get_total_tokens()
        original_count = len(store.query())

        # Prune EPHEMERAL entries
        store.prune(max_priority=MemoryPriority.EPHEMERAL, session_id="test-session")

        # Prune LOW priority entries
        store.prune(max_priority=MemoryPriority.LOW, session_id="test-session")

        optimized_tokens = store.get_total_tokens()
        optimized_count = len(store.query())

        saved = original_tokens - optimized_tokens
        percentage = (saved / original_tokens * 100) if original_tokens > 0 else 0

        return EfficiencyResult(
            scenario="Priority-based pruning (EPHEMERAL + LOW)",
            original_tokens=original_tokens,
            optimized_tokens=optimized_tokens,
            saved_tokens=saved,
            saving_percentage=percentage,
            entries_before=original_count,
            entries_after=optimized_count,
            pruned_entries=original_count - optimized_count,
        )


def measure_summarization_simulation() -> EfficiencyResult:
    """Simulate summarization by replacing multiple entries with one summary."""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = MemoryStore(base_path=Path(tmpdir), auto_save=False)
        entries = create_conversation_entries()

        for entry in entries:
            store.add(**entry, session_id="test-session")

        original_tokens = store.get_total_tokens()
        original_count = len(store.query())

        # Simulate summarization: remove EPHEMERAL and LOW, add summary
        ephemeral_entries = store.query(
            max_priority=MemoryPriority.LOW,
            session_id="test-session",
        )

        # Calculate tokens being summarized
        summarized_tokens = sum(e.tokens for e in ephemeral_entries)

        # Delete original entries
        for mem_entry in ephemeral_entries:
            store.delete(mem_entry.id)

        # Add a summary (typically 10-20% of original size)
        summary_content = (
            "Summary of 35 routine interactions: User inquiries about features 0-14 "
            "were addressed with standard documentation. Debug logs 0-19 showed "
            "normal operation with no errors. All systems functioning correctly."
        )
        summary_tokens = estimate_tokens(summary_content)

        store.add(
            type=MemoryType.SUMMARY,
            content=summary_content,
            priority=MemoryPriority.NORMAL,
            tokens=summary_tokens,
            session_id="test-session",
        )

        optimized_tokens = store.get_total_tokens()
        optimized_count = len(store.query())

        saved = original_tokens - optimized_tokens
        percentage = (saved / original_tokens * 100) if original_tokens > 0 else 0

        return EfficiencyResult(
            scenario="Summarization simulation (EPHEMERAL + LOW → Summary)",
            original_tokens=original_tokens,
            optimized_tokens=optimized_tokens,
            saved_tokens=saved,
            saving_percentage=percentage,
            entries_before=original_count,
            entries_after=optimized_count,
            pruned_entries=original_count - optimized_count,
        )


def run_efficiency_measurements() -> list[EfficiencyResult]:
    """Run all efficiency measurements."""
    results = []

    # Scenario 1: Priority-based pruning
    result1 = measure_manual_prune_by_priority()
    results.append(result1)

    # Scenario 2: Summarization simulation
    result2 = measure_summarization_simulation()
    results.append(result2)

    # Scenario 3: Compare with baseline (no optimization)
    baseline_tokens, baseline_count = measure_no_optimization()

    # Get optimized metrics from pruning scenario
    optimized_tokens = result1.optimized_tokens
    saved = baseline_tokens - optimized_tokens
    percentage = (saved / baseline_tokens * 100) if baseline_tokens > 0 else 0

    results.append(EfficiencyResult(
        scenario="Baseline comparison (no optimization vs pruning)",
        original_tokens=baseline_tokens,
        optimized_tokens=optimized_tokens,
        saved_tokens=saved,
        saving_percentage=percentage,
        entries_before=baseline_count,
        entries_after=result1.entries_after,
        pruned_entries=baseline_count - result1.entries_after,
    ))

    return results


def print_results(results: list[EfficiencyResult]) -> None:
    """Print efficiency measurement results."""
    print("\n" + "=" * 70)
    print("SAGE Token Efficiency Measurement Report")
    print("=" * 70)

    for result in results:
        print(f"\n### {result.scenario}")
        print("-" * 50)
        print(f"  Original tokens:    {result.original_tokens:,}")
        print(f"  Optimized tokens:   {result.optimized_tokens:,}")
        print(f"  Saved tokens:       {result.saved_tokens:,}")
        print(f"  Saving percentage:  {result.saving_percentage:.1f}%")
        print(f"  Entries before:     {result.entries_before}")
        print(f"  Entries after:      {result.entries_after}")
        print(f"  Pruned entries:     {result.pruned_entries}")

    # Summary
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    avg_saving = sum(r.saving_percentage for r in results) / len(results)
    max_saving = max(r.saving_percentage for r in results)
    print(f"  Average token saving: {avg_saving:.1f}%")
    print(f"  Maximum token saving: {max_saving:.1f}%")
    print("=" * 70 + "\n")


# Pytest tests
class TestTokenEfficiency:
    """Token efficiency measurement tests."""

    def test_priority_based_pruning_saves_tokens(self):
        """Test that priority-based pruning actually saves tokens."""
        result = measure_manual_prune_by_priority()

        assert result.saved_tokens > 0, "Should save some tokens"
        assert result.saving_percentage > 0, "Should have positive saving percentage"
        assert result.pruned_entries > 0, "Should prune some entries"
        print(f"\n  Priority pruning saved {result.saving_percentage:.1f}% tokens")

    def test_summarization_saves_more_tokens(self):
        """Test that summarization saves significant tokens."""
        result = measure_summarization_simulation()

        assert result.saved_tokens > 0, "Should save tokens"
        assert result.saving_percentage > 30, "Summarization should save >30% tokens"
        print(f"\n  Summarization saved {result.saving_percentage:.1f}% tokens")

    def test_ephemeral_entries_are_pruned_first(self):
        """Test that EPHEMERAL priority entries are pruned first."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = MemoryStore(base_path=Path(tmpdir), auto_save=False)

            # Add entries with different priorities
            store.add(
                type=MemoryType.CONTEXT,
                content="Ephemeral content",
                priority=MemoryPriority.EPHEMERAL,
                tokens=100,
            )
            store.add(
                type=MemoryType.CONTEXT,
                content="Critical content",
                priority=MemoryPriority.CRITICAL,
                tokens=100,
            )

            initial_tokens = store.get_total_tokens()
            assert initial_tokens == 200

            # Prune only EPHEMERAL
            pruned = store.prune(max_priority=MemoryPriority.EPHEMERAL)

            assert pruned == 1, "Should prune 1 EPHEMERAL entry"
            assert store.get_total_tokens() == 100, "Should have 100 tokens left"

            # Critical entry should remain
            entries = store.query(min_priority=MemoryPriority.CRITICAL)
            assert len(entries) == 1, "Critical entry should remain"

    def test_token_budget_triggers_at_threshold(self):
        """Test that TokenBudget triggers warnings at correct thresholds."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = MemoryStore(base_path=Path(tmpdir), auto_save=False)

            config = TokenBudgetConfig(
                max_tokens=1000,
                reserved_tokens=100,
                warning_threshold=0.70,
                overflow_threshold=0.95,
            )
            budget = TokenBudget(store, config)

            # Add tokens to reach 75% (should be CAUTION)
            store.add(
                type=MemoryType.CONTEXT,
                content="Test",
                tokens=675,  # 675/900 = 75%
            )

            usage = budget.get_usage()
            assert usage.level == TokenWarningLevel.CAUTION
            print(f"\n  75% usage → {usage.level.value} level (correct)")

    def test_full_efficiency_measurement(self):
        """Run full efficiency measurement and verify savings."""
        results = run_efficiency_measurements()

        assert len(results) == 3, "Should have 3 measurement scenarios"

        for result in results:
            assert result.original_tokens > 0, "Should have original tokens"

        # At least one scenario should save >30% tokens
        max_saving = max(r.saving_percentage for r in results)
        assert max_saving > 30, f"Should achieve >30% savings, got {max_saving:.1f}%"

        print_results(results)


if __name__ == "__main__":
    # Run measurements directly
    results = run_efficiency_measurements()
    print_results(results)
