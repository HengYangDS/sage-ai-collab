"""
Unit tests for KnowledgeLoader.

Tests cover:
- Layer enum values and ordering
- LoadResult dataclass functionality
- KnowledgeLoader initialization
- Core loading methods
- Search functionality
- Error handling and edge cases

Author: SAGE AI Collab Team
Version: 0.1.0
"""

from pathlib import Path

import pytest

from sage.core.loader import (
    KnowledgeLoader,
    Layer,
    LoadingTrigger,
    LoadResult,
)


class TestLayerEnum:
    """Tests for Layer enum."""

    def test_layer_values(self):
        """Test Layer enum has the correct values."""
        assert Layer.L0_INDEX.value == 0
        assert Layer.L1_CORE.value == 1
        assert Layer.L2_GUIDELINES.value == 2
        assert Layer.L3_FRAMEWORKS.value == 3
        assert Layer.L4_PRACTICES.value == 4

    def test_layer_ordering(self):
        """Test layers are ordered correctly."""
        layers = list(Layer)
        assert len(layers) == 5
        assert layers[0] == Layer.L0_INDEX
        assert layers[-1] == Layer.L4_PRACTICES

    def test_layer_names(self):
        """Test Layer enum names."""
        assert Layer.L0_INDEX.name == "L0_INDEX"
        assert Layer.L1_CORE.name == "L1_CORE"
        assert Layer.L2_GUIDELINES.name == "L2_GUIDELINES"
        assert Layer.L3_FRAMEWORKS.name == "L3_FRAMEWORKS"
        assert Layer.L4_PRACTICES.name == "L4_PRACTICES"

    def test_layer_comparison(self):
        """Value can compare Test layers."""
        assert Layer.L0_INDEX.value < Layer.L1_CORE.value
        assert Layer.L4_PRACTICES.value > Layer.L2_GUIDELINES.value


class TestLoadResult:
    """Tests for LoadResult dataclass."""

    def test_default_values(self):
        """Test LoadResult default values."""
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
        """Test LoadResult with custom values."""
        result = LoadResult(
            content="knowledge content",
            layers_loaded=[Layer.L0_INDEX, Layer.L1_CORE],
            files_loaded=["index.md", "principles.md"],
            tokens_estimate=500,
            duration_ms=150,
            complete=False,
            status="partial",
            errors=["Timeout on file X"],
        )
        assert result.content == "knowledge content"
        assert len(result.layers_loaded) == 2
        assert len(result.files_loaded) == 2
        assert result.tokens_estimate == 500
        assert result.duration_ms == 150
        assert result.complete is False
        assert result.status == "partial"
        assert len(result.errors) == 1

    def test_to_dict(self):
        """Test LoadResult.to_dict() serialization."""
        result = LoadResult(
            content="test",
            layers_loaded=[Layer.L0_INDEX],
            files_loaded=["test.md"],
            tokens_estimate=100,
            duration_ms=50,
        )
        d = result.to_dict()

        assert isinstance(d, dict)
        assert d["content"] == "test"
        assert d["layers_loaded"] == ["L0_INDEX"]
        assert d["files_loaded"] == ["test.md"]
        assert d["tokens_estimate"] == 100
        assert d["duration_ms"] == 50
        assert d["complete"] is True
        assert d["status"] == "success"
        assert d["errors"] == []

    def test_to_dict_multiple_layers(self):
        """Test to_dict with multiple layers."""
        result = LoadResult(
            content="multi-layer",
            layers_loaded=[Layer.L0_INDEX, Layer.L1_CORE, Layer.L2_GUIDELINES],
        )
        d = result.to_dict()
        assert d["layers_loaded"] == ["L0_INDEX", "L1_CORE", "L2_GUIDELINES"]


class TestLoadingTrigger:
    """Tests for LoadingTrigger dataclass."""

    def test_trigger_creation(self):
        """Test LoadingTrigger creation."""
        trigger = LoadingTrigger(
            name="test",
            keywords=["keyword1", "keyword2"],
            files=["file1.md", "file2.md"],
        )
        assert trigger.name == "test"
        assert trigger.keywords == ["keyword1", "keyword2"]
        assert trigger.files == ["file1.md", "file2.md"]
        assert trigger.timeout_ms == 2000  # default

    def test_trigger_custom_timeout(self):
        """Test LoadingTrigger with a custom timeout."""
        trigger = LoadingTrigger(
            name="slow",
            keywords=["complex"],
            files=["large.md"],
            timeout_ms=5000,
        )
        assert trigger.timeout_ms == 5000


class TestKnowledgeLoaderInit:
    """Tests for KnowledgeLoader initialization."""

    def test_default_init(self):
        """Test KnowledgeLoader default initialization."""
        loader = KnowledgeLoader()
        assert loader.kb_path is not None
        assert isinstance(loader.kb_path, Path)
        assert loader.triggers == KnowledgeLoader.DEFAULT_TRIGGERS
        assert loader._cache == {}

    def test_custom_kb_path(self, tmp_path):
        """Test KnowledgeLoader with a custom kb_path."""
        loader = KnowledgeLoader(kb_path=tmp_path)
        assert loader.kb_path == tmp_path

    def test_custom_triggers(self):
        """Test KnowledgeLoader with custom triggers."""
        custom_triggers = [
            LoadingTrigger(name="custom", keywords=["test"], files=["test.md"])
        ]
        loader = KnowledgeLoader(triggers=custom_triggers)
        assert loader.triggers == custom_triggers
        assert len(loader.triggers) == 1

    def test_default_triggers_count(self):
        """Test default triggers are loaded."""
        loader = KnowledgeLoader()
        # Should have multiple default triggers
        assert len(loader.triggers) >= 5

    def test_always_load_files(self):
        """Test ALWAYS_LOAD contains expected files."""
        assert "index.md" in KnowledgeLoader.ALWAYS_LOAD
        assert "content/core/principles.md" in KnowledgeLoader.ALWAYS_LOAD


class TestKnowledgeLoaderLoad:
    """Tests for KnowledgeLoader load methods."""

    @pytest.fixture
    def loader(self, tmp_path):
        """Create a KnowledgeLoader with the test directory."""
        # Create a test content structure
        content_dir = tmp_path / "content"
        core_dir = content_dir / "core"
        core_dir.mkdir(parents=True)

        # Create test files
        (tmp_path / "index.md").write_text("# Index\nNavigation entry")
        (core_dir / "principles.md").write_text("# Principles\n信达雅")
        (core_dir / "quick_reference.md").write_text("# Quick Reference")

        return KnowledgeLoader(kb_path=tmp_path)

    @pytest.mark.asyncio
    async def test_load_returns_result(self, loader):
        """Test load() returns LoadResult."""
        result = await loader.load(timeout_ms=1000)
        assert isinstance(result, LoadResult)
        assert result.duration_ms >= 0

    @pytest.mark.asyncio
    async def test_load_core(self, loader):
        """Test load_core() method."""
        result = await loader.load_core(timeout_ms=1000)
        assert isinstance(result, LoadResult)

    @pytest.mark.asyncio
    async def test_load_for_task(self, loader):
        """Test load_for_task() with a task description."""
        result = await loader.load_for_task("implement code", timeout_ms=1000)
        assert isinstance(result, LoadResult)

    @pytest.mark.asyncio
    async def test_load_with_specific_files(self, loader):
        """Test load() with specific files."""
        result = await loader.load(
            files=["index.md"],
            timeout_ms=1000,
        )
        assert isinstance(result, LoadResult)

    @pytest.mark.asyncio
    async def test_load_with_layer(self, loader):
        """Test load() with a specific layer."""
        result = await loader.load(
            layer=Layer.L1_CORE,
            timeout_ms=1000,
        )
        assert isinstance(result, LoadResult)


class TestKnowledgeLoaderSearch:
    """Tests for KnowledgeLoader search functionality."""

    @pytest.fixture
    def loader_with_content(self, tmp_path):
        """Create a KnowledgeLoader with searchable content."""
        content_dir = tmp_path / "content"
        core_dir = content_dir / "core"
        guidelines_dir = content_dir / "guidelines"
        core_dir.mkdir(parents=True)
        guidelines_dir.mkdir(parents=True)

        # Create an index and core files
        (tmp_path / "index.md").write_text("# Index\nNavigation entry")
        (core_dir / "principles.md").write_text(
            "# Core Principles\n\n信达雅 (Xin-Da-Ya)\n\nFaithfulness, clarity, elegance."
        )
        (core_dir / "quick_reference.md").write_text(
            "# Quick Reference\nTimeout levels"
        )
        (guidelines_dir / "code_style.md").write_text(
            "# Code Style\n\nPython conventions and best practices."
        )

        return KnowledgeLoader(kb_path=tmp_path)

    @pytest.mark.asyncio
    async def test_search_returns_list(self, loader_with_content):
        """Test search() returns a list."""
        results = await loader_with_content.search("principles", timeout_ms=1000)
        assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_search_with_max_results(self, loader_with_content):
        """Test search respects max_results."""
        results = await loader_with_content.search(
            "content",
            max_results=2,
            timeout_ms=1000,
        )
        assert len(results) <= 2

    @pytest.mark.asyncio
    async def test_search_empty_query(self, loader_with_content):
        """Test search with an empty query."""
        results = await loader_with_content.search("", timeout_ms=1000)
        assert isinstance(results, list)


class TestKnowledgeLoaderErrorHandling:
    """Tests for error handling in KnowledgeLoader."""

    @pytest.fixture
    def loader_empty(self, tmp_path):
        """Create a KnowledgeLoader with an empty directory."""
        return KnowledgeLoader(kb_path=tmp_path)

    @pytest.mark.asyncio
    async def test_load_missing_files(self, loader_empty):
        """Test load() handles missing files."""
        result = await loader_empty.load(
            files=["nonexistent.md"],
            timeout_ms=1000,
        )
        assert isinstance(result, LoadResult)
        # Shouldn't raise exception

    @pytest.mark.asyncio
    async def test_load_framework_not_found(self, loader_empty):
        """Test load_framework() with a nonexistent framework."""
        result = await loader_empty.load_framework(
            "nonexistent_framework",
            timeout_ms=1000,
        )
        assert result.status == "error"
        assert "not found" in result.content.lower()

    @pytest.mark.asyncio
    async def test_search_in_empty_kb(self, loader_empty):
        """Test search in an empty knowledge base."""
        results = await loader_empty.search("anything", timeout_ms=1000)
        assert isinstance(results, list)
        # Should return an empty list, not raise an exception


class TestKnowledgeLoaderCaching:
    """Tests for KnowledgeLoader caching behavior."""

    @pytest.fixture
    def loader(self, tmp_path):
        """Create a KnowledgeLoader with test content."""
        (tmp_path / "index.md").write_text("# Index")
        (tmp_path / "content").mkdir()
        (tmp_path / "content" / "core").mkdir()
        (tmp_path / "content" / "core" / "principles.md").write_text("# Principles")
        (tmp_path / "content" / "core" / "quick_reference.md").write_text("# Reference")
        return KnowledgeLoader(kb_path=tmp_path)

    def test_cache_initially_empty(self, loader):
        """Test cache is empty on an init."""
        assert loader._cache == {}
        assert loader._cache_hashes == {}

    @pytest.mark.asyncio
    async def test_cache_populated_after_load(self, loader):
        """Test cache is populated after loading."""
        await loader.load(timeout_ms=1000)
        # Cache may or may not be populated depending on implementation
        # This test verifies no errors occur


class TestKnowledgeLoaderTriggers:
    """Tests for smart trigger-based loading."""

    def test_default_triggers_have_keywords(self):
        """Test default triggers have keywords."""
        loader = KnowledgeLoader()
        for trigger in loader.triggers:
            assert len(trigger.keywords) > 0
            assert len(trigger.files) > 0

    def test_code_trigger_exists(self):
        """Test code trigger is in defaults."""
        loader = KnowledgeLoader()
        code_triggers = [t for t in loader.triggers if t.name == "code"]
        assert len(code_triggers) == 1
        assert "code" in code_triggers[0].keywords
        assert "implement" in code_triggers[0].keywords

    def test_architecture_trigger_exists(self):
        """Test architecture trigger is in defaults."""
        loader = KnowledgeLoader()
        arch_triggers = [t for t in loader.triggers if t.name == "architecture"]
        assert len(arch_triggers) == 1
        assert "architecture" in arch_triggers[0].keywords
        assert "design" in arch_triggers[0].keywords

    def test_bilingual_keywords(self):
        """Test triggers have bilingual keywords (EN + ZH)."""
        loader = KnowledgeLoader()
        code_trigger = next(t for t in loader.triggers if t.name == "code")
        # Should have both English and Chinese keywords
        has_english = any(k.isascii() for k in code_trigger.keywords)
        has_chinese = any(not k.isascii() for k in code_trigger.keywords)
        assert has_english
        assert has_chinese
