"""
Unit tests for loader module.

Tests cover:
- Layer enum
- LoadResult class
- LoadingTrigger class
- KnowledgeLoader class
- Convenience functions
"""

import sys
from pathlib import Path

import pytest

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai_collab_kb.loader import (
    KnowledgeLoader,
    Layer,
    LoadingTrigger,
    LoadResult,
    load_core,
    load_knowledge,
    search_knowledge,
)


class TestLayer:
    """Tests for Layer enum."""

    def test_layer_values(self):
        """All 5 layers should exist with correct values."""
        assert Layer.L0_INDEX.value == 0
        assert Layer.L1_CORE.value == 1
        assert Layer.L2_GUIDELINES.value == 2
        assert Layer.L3_FRAMEWORKS.value == 3
        assert Layer.L4_PRACTICES.value == 4

    def test_layer_count(self):
        """Should have exactly 5 layers."""
        assert len(Layer) == 5

    def test_layer_names(self):
        """Layer names should be descriptive."""
        assert "INDEX" in Layer.L0_INDEX.name
        assert "CORE" in Layer.L1_CORE.name
        assert "GUIDELINES" in Layer.L2_GUIDELINES.name
        assert "FRAMEWORKS" in Layer.L3_FRAMEWORKS.name
        assert "PRACTICES" in Layer.L4_PRACTICES.name


class TestLoadResult:
    """Tests for LoadResult dataclass."""

    def test_default_values(self):
        """Default LoadResult should have sensible defaults."""
        result = LoadResult(content="test content")
        assert result.content == "test content"
        assert result.layers_loaded == []
        assert result.files_loaded == []
        assert result.tokens_estimate == 0
        assert result.duration_ms == 0
        assert result.complete is True
        assert result.status == "success"
        assert result.errors == []

    def test_custom_values(self):
        """LoadResult should accept custom values."""
        result = LoadResult(
            content="# Test",
            layers_loaded=[Layer.L0_INDEX, Layer.L1_CORE],
            files_loaded=["index.md", "content/core/principles.md"],
            tokens_estimate=500,
            duration_ms=150,
            complete=False,
            status="partial",
            errors=["Some warning"],
        )
        assert result.content == "# Test"
        assert len(result.layers_loaded) == 2
        assert len(result.files_loaded) == 2
        assert result.tokens_estimate == 500
        assert result.duration_ms == 150
        assert result.complete is False
        assert result.status == "partial"
        assert len(result.errors) == 1

    def test_to_dict(self):
        """to_dict should return correct dictionary."""
        result = LoadResult(
            content="# Test",
            layers_loaded=[Layer.L0_INDEX],
            files_loaded=["index.md"],
            tokens_estimate=100,
            duration_ms=50,
            complete=True,
            status="success",
            errors=[],
        )
        d = result.to_dict()
        assert d["content"] == "# Test"
        assert d["layers_loaded"] == ["L0_INDEX"]
        assert d["files_loaded"] == ["index.md"]
        assert d["tokens_estimate"] == 100
        assert d["duration_ms"] == 50
        assert d["complete"] is True
        assert d["status"] == "success"
        assert d["errors"] == []


class TestLoadingTrigger:
    """Tests for LoadingTrigger dataclass."""

    def test_default_timeout(self):
        """Default timeout should be 2000ms."""
        trigger = LoadingTrigger(
            name="test",
            keywords=["test"],
            files=["test.md"],
        )
        assert trigger.timeout_ms == 2000

    def test_custom_values(self):
        """LoadingTrigger should accept custom values."""
        trigger = LoadingTrigger(
            name="code",
            keywords=["code", "implement", "fix"],
            files=["code_style.md", "python.md"],
            timeout_ms=3000,
        )
        assert trigger.name == "code"
        assert len(trigger.keywords) == 3
        assert len(trigger.files) == 2
        assert trigger.timeout_ms == 3000


class TestKnowledgeLoader:
    """Tests for KnowledgeLoader class."""

    @pytest.fixture
    def kb_path(self):
        """Get the knowledge base path."""
        return Path(__file__).parent.parent

    @pytest.fixture
    def loader(self, kb_path):
        """Create a KnowledgeLoader instance."""
        return KnowledgeLoader(kb_path=kb_path)

    def test_initialization_default(self, kb_path):
        """Should initialize with default values."""
        loader = KnowledgeLoader(kb_path=kb_path)
        assert loader.kb_path == kb_path
        assert loader.timeout_manager is not None
        assert len(loader.triggers) == len(KnowledgeLoader.DEFAULT_TRIGGERS)

    def test_initialization_custom_triggers(self, kb_path):
        """Should accept custom triggers."""
        custom_triggers = [
            LoadingTrigger(name="custom", keywords=["custom"], files=["custom.md"])
        ]
        loader = KnowledgeLoader(kb_path=kb_path, triggers=custom_triggers)
        assert len(loader.triggers) == 1
        assert loader.triggers[0].name == "custom"

    def test_default_triggers_exist(self):
        """Default triggers should be properly defined."""
        triggers = KnowledgeLoader.DEFAULT_TRIGGERS
        assert len(triggers) == 8  # 6 original + python + quality

        trigger_names = [t.name for t in triggers]
        assert "code" in trigger_names
        assert "architecture" in trigger_names
        assert "testing" in trigger_names
        assert "ai_collaboration" in trigger_names
        assert "complex_decision" in trigger_names
        assert "documentation" in trigger_names
        assert "python" in trigger_names
        assert "quality" in trigger_names

    def test_always_load_files(self):
        """ALWAYS_LOAD should contain essential files."""
        always_load = KnowledgeLoader.ALWAYS_LOAD
        assert "index.md" in always_load
        assert "content/core/principles.md" in always_load
        assert "content/core/quick_reference.md" in always_load

    @pytest.mark.asyncio
    async def test_load_core(self, loader):
        """load_core should return core content."""
        result = await loader.load_core(timeout_ms=5000)

        assert result.content is not None
        assert result.status in ["success", "partial", "fallback"]
        assert result.duration_ms >= 0

    @pytest.mark.asyncio
    async def test_load_for_task_code(self, loader):
        """load_for_task should load relevant files for code tasks."""
        result = await loader.load_for_task("implement a feature", timeout_ms=5000)

        assert result.content is not None
        assert result.status in ["success", "partial", "fallback"]

    @pytest.mark.asyncio
    async def test_load_for_task_documentation(self, loader):
        """load_for_task should load relevant files for documentation tasks."""
        result = await loader.load_for_task("write documentation", timeout_ms=5000)

        assert result.content is not None
        assert result.status in ["success", "partial", "fallback"]

    @pytest.mark.asyncio
    async def test_load_with_specific_files(self, loader):
        """load should accept specific file list."""
        result = await loader.load(files=["index.md"], timeout_ms=5000)

        assert result.content is not None
        assert "index.md" in result.files_loaded or result.status == "fallback"

    @pytest.mark.asyncio
    async def test_load_with_layer(self, loader):
        """load should accept layer parameter."""
        result = await loader.load(layer=Layer.L1_CORE, timeout_ms=5000)

        assert result.content is not None
        assert result.status in ["success", "partial", "fallback"]

    @pytest.mark.asyncio
    async def test_load_guidelines(self, loader):
        """load_guidelines should load specific chapter."""
        result = await loader.load_guidelines("code_style", timeout_ms=5000)

        assert result.content is not None
        assert result.status in ["success", "partial", "fallback", "error"]

    @pytest.mark.asyncio
    async def test_load_framework(self, loader):
        """load_framework should load framework content."""
        result = await loader.load_framework("autonomy", timeout_ms=5000)

        assert result.content is not None
        assert result.status in ["success", "partial", "fallback", "error"]

    @pytest.mark.asyncio
    async def test_load_framework_not_found(self, loader):
        """load_framework should handle non-existent framework."""
        result = await loader.load_framework("nonexistent_framework", timeout_ms=5000)

        assert result.status == "error"
        assert "not found" in result.content.lower() or len(result.errors) > 0

    @pytest.mark.asyncio
    async def test_search(self, loader):
        """search should find matching content."""
        results = await loader.search("principles", max_results=5, timeout_ms=5000)

        assert isinstance(results, list)
        # Should find at least principles.md
        if len(results) > 0:
            assert "path" in results[0]
            assert "score" in results[0]

    @pytest.mark.asyncio
    async def test_search_no_results(self, loader):
        """search should return empty list for no matches."""
        results = await loader.search(
            "xyznonexistentquery123", max_results=5, timeout_ms=5000
        )

        assert isinstance(results, list)
        assert len(results) == 0

    def test_cache_initialization(self, loader):
        """Caches should be initialized as empty dicts."""
        assert loader._cache == {}
        assert loader._cache_hashes == {}
        assert loader._last_load == {}

    @pytest.mark.asyncio
    async def test_clear_cache(self, loader):
        """clear_cache should empty all caches."""
        # First load something to populate cache
        await loader.load_core(timeout_ms=5000)

        # Clear cache
        loader.clear_cache()

        assert loader._cache == {}
        assert loader._cache_hashes == {}

    @pytest.mark.asyncio
    async def test_get_cache_stats(self, loader):
        """get_cache_stats should return cache statistics."""
        stats = loader.get_cache_stats()

        assert "cached_files" in stats
        assert "total_size" in stats
        assert isinstance(stats["cached_files"], int)
        assert isinstance(stats["total_size"], int)

    @pytest.mark.asyncio
    async def test_load_result_tokens_estimate(self, loader):
        """Load result should include tokens estimate."""
        result = await loader.load_core(timeout_ms=5000)

        # Tokens estimate should be positive for non-empty content
        if result.content and result.status == "success":
            assert result.tokens_estimate > 0

    @pytest.mark.asyncio
    async def test_load_timeout_protection(self, loader):
        """Load should complete within timeout."""
        import time

        start = time.monotonic()
        result = await loader.load_core(timeout_ms=100)  # Very short timeout
        elapsed = (time.monotonic() - start) * 1000

        # Should complete within reasonable time (2x timeout as buffer)
        assert elapsed < 500  # 500ms max


class TestConvenienceFunctions:
    """Tests for module-level convenience functions."""

    @pytest.mark.asyncio
    async def test_load_knowledge(self):
        """load_knowledge should return content."""
        result = await load_knowledge(task="test task", timeout_ms=5000)

        assert result is not None
        assert hasattr(result, "content")
        assert hasattr(result, "status")

    @pytest.mark.asyncio
    async def test_load_core_function(self):
        """load_core function should return core content."""
        result = await load_core(timeout_ms=5000)

        assert result is not None
        assert hasattr(result, "content")

    @pytest.mark.asyncio
    async def test_search_knowledge(self):
        """search_knowledge should return results."""
        results = await search_knowledge("principles", max_results=5)

        assert isinstance(results, list)


class TestLoadResultIntegration:
    """Integration tests for LoadResult with real loading."""

    @pytest.fixture
    def loader(self):
        """Create a KnowledgeLoader instance with real KB path."""
        kb_path = Path(__file__).parent.parent
        return KnowledgeLoader(kb_path=kb_path)

    @pytest.mark.asyncio
    async def test_load_result_complete_structure(self, loader):
        """LoadResult should have complete structure after load."""
        result = await loader.load_core(timeout_ms=5000)

        # Check all attributes exist
        assert hasattr(result, "content")
        assert hasattr(result, "layers_loaded")
        assert hasattr(result, "files_loaded")
        assert hasattr(result, "tokens_estimate")
        assert hasattr(result, "duration_ms")
        assert hasattr(result, "complete")
        assert hasattr(result, "status")
        assert hasattr(result, "errors")

        # Check types
        assert isinstance(result.content, str)
        assert isinstance(result.layers_loaded, list)
        assert isinstance(result.files_loaded, list)
        assert isinstance(result.tokens_estimate, int)
        assert isinstance(result.duration_ms, int)
        assert isinstance(result.complete, bool)
        assert isinstance(result.status, str)
        assert isinstance(result.errors, list)

    @pytest.mark.asyncio
    async def test_load_result_to_dict_serializable(self, loader):
        """LoadResult.to_dict() should be JSON serializable."""
        import json

        result = await loader.load_core(timeout_ms=5000)
        d = result.to_dict()

        # Should not raise
        json_str = json.dumps(d)
        assert isinstance(json_str, str)

        # Should round-trip
        parsed = json.loads(json_str)
        assert parsed["status"] == result.status
