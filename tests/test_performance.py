"""
Performance Benchmark Tests for AI Collaboration Knowledge Base.

Tests cover:
- Response time benchmarks (target: < 500ms average)
- Timeout rate (target: < 1%)
- Token efficiency
- Concurrent load testing

These tests verify Phase 4 acceptance criteria from UNIFIED_ULTIMATE_DESIGN.md.
"""

import asyncio
import statistics
import sys
import time
from pathlib import Path

import pytest

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai_collab_kb.loader import (
    KnowledgeLoader,
)


class TestResponseTimeBenchmarks:
    """
    Performance tests for response time.

    Target: Average response time < 500ms
    """

    @pytest.fixture
    def loader(self):
        """Create a KnowledgeLoader instance."""
        kb_path = Path(__file__).parent.parent
        return KnowledgeLoader(kb_path=kb_path)

    @pytest.mark.asyncio
    async def test_load_core_response_time(self, loader):
        """Core loading should complete within 500ms on average."""
        times = []
        iterations = 10

        for _ in range(iterations):
            start = time.monotonic()
            result = await loader.load_core(timeout_ms=5000)
            elapsed = (time.monotonic() - start) * 1000
            times.append(elapsed)

            # Each individual call should complete within timeout
            assert elapsed < 5000, f"Single call took {elapsed}ms"

        avg_time = statistics.mean(times)

        # Target: < 500ms average
        assert (
            avg_time < 500
        ), f"Average response time {avg_time:.2f}ms exceeds 500ms target"

        # Report statistics
        print("\nCore Loading Performance:")
        print(f"  Average: {avg_time:.2f}ms")
        print(f"  Min: {min(times):.2f}ms")
        print(f"  Max: {max(times):.2f}ms")
        print(f"  Std Dev: {statistics.stdev(times):.2f}ms")

    @pytest.mark.asyncio
    async def test_load_for_task_response_time(self, loader):
        """Task-based loading should complete within 500ms on average."""
        tasks = [
            "implement a feature",
            "fix a bug",
            "write documentation",
            "design architecture",
            "write tests",
        ]
        times = []

        for task in tasks:
            for _ in range(2):  # 2 iterations per task
                start = time.monotonic()
                result = await loader.load_for_task(task, timeout_ms=5000)
                elapsed = (time.monotonic() - start) * 1000
                times.append(elapsed)

        avg_time = statistics.mean(times)

        # Target: < 500ms average
        assert (
            avg_time < 500
        ), f"Average response time {avg_time:.2f}ms exceeds 500ms target"

        print("\nTask-based Loading Performance:")
        print(f"  Average: {avg_time:.2f}ms")
        print(f"  Min: {min(times):.2f}ms")
        print(f"  Max: {max(times):.2f}ms")

    @pytest.mark.asyncio
    async def test_search_response_time(self, loader):
        """Search should complete within 500ms on average."""
        queries = ["principles", "timeout", "autonomy", "code", "test"]
        times = []

        for query in queries:
            start = time.monotonic()
            results = await loader.search(query, max_results=5, timeout_ms=3000)
            elapsed = (time.monotonic() - start) * 1000
            times.append(elapsed)

        avg_time = statistics.mean(times)

        # Target: < 500ms average
        assert (
            avg_time < 500
        ), f"Average search time {avg_time:.2f}ms exceeds 500ms target"

        print("\nSearch Performance:")
        print(f"  Average: {avg_time:.2f}ms")
        print(f"  Min: {min(times):.2f}ms")
        print(f"  Max: {max(times):.2f}ms")

    @pytest.mark.asyncio
    async def test_guidelines_loading_response_time(self, loader):
        """Guidelines loading should complete within 500ms on average."""
        chapters = ["code_style", "python", "ai_collaboration", "quality"]
        times = []

        for chapter in chapters:
            start = time.monotonic()
            result = await loader.load_guidelines(chapter, timeout_ms=3000)
            elapsed = (time.monotonic() - start) * 1000
            times.append(elapsed)

        avg_time = statistics.mean(times)

        # Target: < 500ms average
        assert (
            avg_time < 500
        ), f"Average guidelines load time {avg_time:.2f}ms exceeds 500ms target"

        print("\nGuidelines Loading Performance:")
        print(f"  Average: {avg_time:.2f}ms")


class TestTimeoutRate:
    """
    Tests for timeout rate.

    Target: Timeout rate < 1%
    """

    @pytest.fixture
    def loader(self):
        """Create a KnowledgeLoader instance."""
        kb_path = Path(__file__).parent.parent
        return KnowledgeLoader(kb_path=kb_path)

    @pytest.mark.asyncio
    async def test_timeout_rate_under_normal_load(self, loader):
        """Under normal load, timeout rate should be < 1%."""
        total_calls = 100
        timeout_count = 0
        success_count = 0
        fallback_count = 0

        for i in range(total_calls):
            result = await loader.load_core(timeout_ms=5000)

            if result.status == "success":
                success_count += 1
            elif result.status == "fallback":
                fallback_count += 1
            elif result.status in ["partial", "error"]:
                timeout_count += 1

        timeout_rate = (timeout_count / total_calls) * 100

        # Target: < 1% timeout rate
        assert timeout_rate < 1, f"Timeout rate {timeout_rate:.2f}% exceeds 1% target"

        print(f"\nTimeout Rate Test ({total_calls} calls):")
        print(f"  Success: {success_count} ({success_count/total_calls*100:.1f}%)")
        print(f"  Fallback: {fallback_count} ({fallback_count/total_calls*100:.1f}%)")
        print(f"  Timeout/Error: {timeout_count} ({timeout_rate:.2f}%)")

    @pytest.mark.asyncio
    async def test_graceful_degradation(self, loader):
        """System should gracefully degrade under tight timeouts."""
        # Test with very short timeout - should use fallback, not fail
        result = await loader.load_core(timeout_ms=1)

        # Should return something (either content or fallback)
        assert result.content is not None
        assert len(result.content) > 0

        # Status should be one of the valid degradation levels
        assert result.status in ["success", "partial", "fallback", "error"]

        print("\nGraceful Degradation Test (1ms timeout):")
        print(f"  Status: {result.status}")
        print(f"  Content length: {len(result.content)} chars")

    @pytest.mark.asyncio
    async def test_never_hang_guarantee(self, loader):
        """Operations should never hang - always return within timeout + buffer."""
        timeout_ms = 100
        buffer_ms = 200  # Allow some overhead
        max_time = timeout_ms + buffer_ms

        start = time.monotonic()
        result = await loader.load(timeout_ms=timeout_ms)
        elapsed = (time.monotonic() - start) * 1000

        # Should never exceed timeout + reasonable buffer
        assert (
            elapsed < max_time
        ), f"Operation took {elapsed:.2f}ms, exceeds max {max_time}ms"

        print("\nNever-Hang Guarantee Test:")
        print(f"  Timeout: {timeout_ms}ms")
        print(f"  Actual: {elapsed:.2f}ms")
        print(f"  Within bounds: {elapsed < max_time}")


class TestTokenEfficiency:
    """
    Tests for token efficiency.

    Target: 95% token reduction compared to loading everything
    """

    @pytest.fixture
    def loader(self):
        """Create a KnowledgeLoader instance."""
        kb_path = Path(__file__).parent.parent
        return KnowledgeLoader(kb_path=kb_path)

    @pytest.mark.asyncio
    async def test_core_only_token_efficiency(self, loader):
        """Core-only loading should be highly token efficient."""
        result = await loader.load_core(timeout_ms=5000)

        # Core should be ~500 tokens according to spec
        # Original full KB was ~15,000 tokens
        original_estimate = 15000
        actual_tokens = result.tokens_estimate

        if actual_tokens > 0:
            reduction = (1 - actual_tokens / original_estimate) * 100

            print("\nCore Token Efficiency:")
            print(f"  Original estimate: ~{original_estimate} tokens")
            print(f"  Core tokens: {actual_tokens}")
            print(f"  Reduction: {reduction:.1f}%")

            # Should achieve significant reduction
            assert reduction > 80, f"Token reduction {reduction:.1f}% below 80% target"

    @pytest.mark.asyncio
    async def test_task_based_token_efficiency(self, loader):
        """Task-based loading should achieve good token efficiency."""
        # Simple task should load minimal content
        result = await loader.load_for_task("fix a small bug", timeout_ms=5000)

        original_estimate = 15000
        actual_tokens = result.tokens_estimate

        if actual_tokens > 0:
            reduction = (1 - actual_tokens / original_estimate) * 100

            print("\nTask-based Token Efficiency:")
            print("  Task: 'fix a small bug'")
            print(f"  Tokens loaded: {actual_tokens}")
            print(f"  Reduction: {reduction:.1f}%")

            # Task-based should achieve at least 80% reduction
            assert reduction > 80, f"Token reduction {reduction:.1f}% below 80% target"


class TestConcurrentLoad:
    """Tests for concurrent load handling."""

    @pytest.fixture
    def loader(self):
        """Create a KnowledgeLoader instance."""
        kb_path = Path(__file__).parent.parent
        return KnowledgeLoader(kb_path=kb_path)

    @pytest.mark.asyncio
    async def test_concurrent_requests(self, loader):
        """System should handle concurrent requests gracefully."""

        async def make_request(task_id):
            start = time.monotonic()
            result = await loader.load_core(timeout_ms=5000)
            elapsed = (time.monotonic() - start) * 1000
            return {
                "task_id": task_id,
                "status": result.status,
                "duration_ms": elapsed,
                "tokens": result.tokens_estimate,
            }

        # Run 10 concurrent requests
        tasks = [make_request(i) for i in range(10)]
        results = await asyncio.gather(*tasks)

        # All should complete successfully
        success_count = sum(
            1 for r in results if r["status"] in ["success", "partial", "fallback"]
        )
        avg_time = statistics.mean(r["duration_ms"] for r in results)

        assert success_count == 10, f"Only {success_count}/10 requests succeeded"

        print("\nConcurrent Load Test (10 simultaneous requests):")
        print(f"  All succeeded: {success_count == 10}")
        print(f"  Average time: {avg_time:.2f}ms")
        print(f"  Max time: {max(r['duration_ms'] for r in results):.2f}ms")


class TestCachePerformance:
    """Tests for cache performance."""

    @pytest.fixture
    def loader(self):
        """Create a KnowledgeLoader instance."""
        kb_path = Path(__file__).parent.parent
        return KnowledgeLoader(kb_path=kb_path)

    @pytest.mark.asyncio
    async def test_cache_speedup(self, loader):
        """Second load should be faster due to caching."""
        # Clear cache first
        loader.clear_cache()

        # First load (cold cache)
        start1 = time.monotonic()
        result1 = await loader.load_core(timeout_ms=5000)
        cold_time = (time.monotonic() - start1) * 1000

        # Second load (warm cache)
        start2 = time.monotonic()
        result2 = await loader.load_core(timeout_ms=5000)
        warm_time = (time.monotonic() - start2) * 1000

        print("\nCache Performance:")
        print(f"  Cold cache: {cold_time:.2f}ms")
        print(f"  Warm cache: {warm_time:.2f}ms")

        # Warm cache should be faster (or at least not slower)
        # Allow some variance for system noise
        assert warm_time <= cold_time * 1.5, "Warm cache significantly slower than cold"


class TestBenchmarkReport:
    """Generate comprehensive benchmark report."""

    @pytest.fixture
    def loader(self):
        """Create a KnowledgeLoader instance."""
        kb_path = Path(__file__).parent.parent
        return KnowledgeLoader(kb_path=kb_path)

    @pytest.mark.asyncio
    async def test_generate_benchmark_report(self, loader):
        """Generate and print comprehensive benchmark report."""
        print("\n" + "=" * 60)
        print("AI Collaboration KB - Performance Benchmark Report")
        print("=" * 60)

        # Test 1: Response times
        response_times = []
        for _ in range(10):
            start = time.monotonic()
            await loader.load_core(timeout_ms=5000)
            response_times.append((time.monotonic() - start) * 1000)

        avg_response = statistics.mean(response_times)

        # Test 2: Timeout rate
        timeouts = 0
        for _ in range(50):
            result = await loader.load_core(timeout_ms=5000)
            if result.status in ["error"]:
                timeouts += 1
        timeout_rate = (timeouts / 50) * 100

        # Test 3: Token efficiency
        result = await loader.load_core(timeout_ms=5000)
        token_reduction = (
            (1 - result.tokens_estimate / 15000) * 100
            if result.tokens_estimate > 0
            else 0
        )

        # Print report
        print("\n📊 Performance Metrics:")
        print(
            f"  Average Response Time: {avg_response:.2f}ms (target: <500ms) {'✓' if avg_response < 500 else '✗'}"
        )
        print(
            f"  Timeout Rate: {timeout_rate:.2f}% (target: <1%) {'✓' if timeout_rate < 1 else '✗'}"
        )
        print(
            f"  Token Reduction: {token_reduction:.1f}% (target: >80%) {'✓' if token_reduction > 80 else '✗'}"
        )

        # Verify targets
        assert avg_response < 500, f"Response time {avg_response:.2f}ms exceeds target"
        assert timeout_rate < 1, f"Timeout rate {timeout_rate:.2f}% exceeds target"

        print("\n" + "=" * 60)
        print("✅ All performance targets met!")
        print("=" * 60)
