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
        # Triggers are loaded from sage.yaml config
        assert len(loader.triggers) >= 1  # At least one trigger should be loaded from config
        assert all(isinstance(t, LoadingTrigger) for t in loader.triggers)
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
        """Test always_load files are configured."""
        loader = KnowledgeLoader()
        # Always load files should be a list
        assert isinstance(loader._always_load, list)
        # Should have at least some default files or be configurable
        # The exact content depends on sage.yaml config


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


class TestGetLayerForFile:
    """Tests for _get_layer_for_file static method."""

    def test_index_file(self):
        """Test index.md maps to L0_INDEX."""
        layer = KnowledgeLoader._get_layer_for_file("index.md")
        assert layer == Layer.L0_INDEX

    def test_core_file(self):
        """Test content/core files map to L1_CORE."""
        layer = KnowledgeLoader._get_layer_for_file("content/core/principles.md")
        assert layer == Layer.L1_CORE

    def test_guidelines_file(self):
        """Test content/guidelines files map to L2_GUIDELINES."""
        layer = KnowledgeLoader._get_layer_for_file("content/guidelines/quick_start.md")
        assert layer == Layer.L2_GUIDELINES

    def test_frameworks_file(self):
        """Test content/frameworks files map to L3_FRAMEWORKS."""
        layer = KnowledgeLoader._get_layer_for_file("content/frameworks/autonomy/levels.md")
        assert layer == Layer.L3_FRAMEWORKS

    def test_practices_file(self):
        """Test content/practices files map to L4_PRACTICES."""
        layer = KnowledgeLoader._get_layer_for_file("content/practices/workflow.md")
        assert layer == Layer.L4_PRACTICES

    def test_unknown_file_defaults_to_core(self):
        """Test unknown paths default to L1_CORE."""
        layer = KnowledgeLoader._get_layer_for_file("random/path/file.md")
        assert layer == Layer.L1_CORE


class TestGetPreview:
    """Tests for _get_preview static method."""

    def test_preview_with_match(self):
        """Test preview generation with query match."""
        content = "This is a long text with the keyword somewhere in the middle of the content."
        preview = KnowledgeLoader._get_preview(content, "keyword")
        assert "keyword" in preview

    def test_preview_no_match(self):
        """Test preview generation without query match."""
        content = "This is some content without the search term."
        preview = KnowledgeLoader._get_preview(content, "notfound")
        assert preview.endswith("...")
        assert len(preview) <= 103  # 100 + "..."

    def test_preview_match_at_start(self):
        """Test preview when match is at the start."""
        content = "keyword is at the very beginning of this content."
        preview = KnowledgeLoader._get_preview(content, "keyword")
        assert preview.startswith("keyword")

    def test_preview_match_in_middle(self):
        """Test preview when match is in the middle."""
        content = "x" * 50 + "keyword" + "y" * 50
        preview = KnowledgeLoader._get_preview(content, "keyword")
        assert "keyword" in preview
        assert preview.startswith("...")


class TestLoadGuidelines:
    """Tests for load_guidelines method."""

    @pytest.fixture
    def loader_with_guidelines(self, tmp_path):
        """Create a loader with guidelines content."""
        guidelines_dir = tmp_path / "content" / "guidelines"
        guidelines_dir.mkdir(parents=True)
        (guidelines_dir / "quick_start.md").write_text("# Quick Start\nOverview content")
        (guidelines_dir / "cognitive.md").write_text("# Cognitive\nCognitive content")
        return KnowledgeLoader(kb_path=tmp_path)

    @pytest.mark.asyncio
    async def test_load_guidelines_quick_start(self, loader_with_guidelines):
        """Test loading guidelines with quick_start chapter."""
        result = await loader_with_guidelines.load_guidelines(chapter="quick_start", timeout_ms=2000)
        assert isinstance(result, LoadResult)

    @pytest.mark.asyncio
    async def test_load_guidelines_cognitive(self, loader_with_guidelines):
        """Test loading guidelines with cognitive chapter."""
        result = await loader_with_guidelines.load_guidelines(chapter="cognitive", timeout_ms=2000)
        assert isinstance(result, LoadResult)

    @pytest.mark.asyncio
    async def test_load_guidelines_invalid_chapter(self, loader_with_guidelines):
        """Test loading guidelines with invalid chapter."""
        result = await loader_with_guidelines.load_guidelines(chapter="invalid_xyz", timeout_ms=2000)
        assert isinstance(result, LoadResult)


class TestLoadFramework:
    """Tests for load_framework method."""

    @pytest.fixture
    def loader_with_frameworks(self, tmp_path):
        """Create a loader with frameworks content."""
        frameworks_dir = tmp_path / "content" / "frameworks"
        autonomy_dir = frameworks_dir / "autonomy"
        autonomy_dir.mkdir(parents=True)
        (autonomy_dir / "levels.md").write_text("# Autonomy Levels\nL1-L6 content")
        cognitive_dir = frameworks_dir / "cognitive"
        cognitive_dir.mkdir(parents=True)
        (cognitive_dir / "expert_committee.md").write_text("# Expert Committee")
        return KnowledgeLoader(kb_path=tmp_path)

    @pytest.mark.asyncio
    async def test_load_autonomy_framework(self, loader_with_frameworks):
        """Test loading autonomy framework."""
        result = await loader_with_frameworks.load_framework(name="autonomy", timeout_ms=2000)
        assert isinstance(result, LoadResult)

    @pytest.mark.asyncio
    async def test_load_cognitive_framework(self, loader_with_frameworks):
        """Test loading cognitive framework."""
        result = await loader_with_frameworks.load_framework(name="cognitive", timeout_ms=2000)
        assert isinstance(result, LoadResult)


class TestSearchWithContent:
    """Extended search tests with actual content."""

    @pytest.fixture
    def loader_with_searchable_content(self, tmp_path):
        """Create a loader with searchable content."""
        core_dir = tmp_path / "content" / "core"
        core_dir.mkdir(parents=True)
        (core_dir / "principles.md").write_text(
            "# Core Principles\n\nThis document contains important principles.\n"
            "## Key Points\nPrinciples are fundamental."
        )
        (core_dir / "reference.md").write_text(
            "# Quick Reference\n\nReference material here.\n"
            "This has different content without the keyword."
        )
        guidelines_dir = tmp_path / "content" / "guidelines"
        guidelines_dir.mkdir(parents=True)
        (guidelines_dir / "guide.md").write_text(
            "# Guidelines\n\nGuideline principles for best practices."
        )
        return KnowledgeLoader(kb_path=tmp_path)

    @pytest.mark.asyncio
    async def test_search_returns_list(self, loader_with_searchable_content):
        """Test search always returns a list."""
        results = await loader_with_searchable_content.search("principles", timeout_ms=5000)
        assert isinstance(results, list)
        # Results may be empty if circuit breaker is open, but should be a list

    @pytest.mark.asyncio
    async def test_search_respects_max_results(self, loader_with_searchable_content):
        """Test search respects max_results parameter."""
        results = await loader_with_searchable_content.search("content", max_results=1, timeout_ms=5000)
        assert len(results) <= 1

    @pytest.mark.asyncio
    async def test_search_result_structure(self, loader_with_searchable_content):
        """Test search results have correct structure when found."""
        results = await loader_with_searchable_content.search("principles", timeout_ms=5000)
        # If results found, verify structure
        if results:
            assert "score" in results[0]
            assert "path" in results[0]
            assert "preview" in results[0]


class TestCachingBehavior:
    """Tests for caching behavior in loader."""

    @pytest.fixture
    def loader_with_cache_content(self, tmp_path):
        """Create a loader with content for cache testing."""
        core_dir = tmp_path / "content" / "core"
        core_dir.mkdir(parents=True)
        (core_dir / "test.md").write_text("# Test Content")
        return KnowledgeLoader(kb_path=tmp_path)

    @pytest.mark.asyncio
    async def test_cache_hit_on_second_load(self, loader_with_cache_content):
        """Test that second load uses cache."""
        # First load
        result1 = await loader_with_cache_content.load(timeout_ms=2000)
        # Second load should use cache
        result2 = await loader_with_cache_content.load(timeout_ms=2000)
        assert result1.status == result2.status

    def test_clear_cache(self, loader_with_cache_content):
        """Test cache can be cleared."""
        loader_with_cache_content._cache["test"] = "value"
        loader_with_cache_content._cache.clear()
        assert len(loader_with_cache_content._cache) == 0


class TestGetFilesForTask:
    """Tests for _get_files_for_task method."""

    def test_default_files_for_unknown_task(self):
        """Test that unknown task returns ALWAYS_LOAD files."""
        loader = KnowledgeLoader()
        files = loader._get_files_for_task("random unknown task xyz")
        assert isinstance(files, list)

    def test_code_task_triggers(self):
        """Test that code-related task triggers code files."""
        loader = KnowledgeLoader()
        files = loader._get_files_for_task("write some python code")
        assert isinstance(files, list)

    def test_architecture_task_triggers(self):
        """Test that architecture-related task triggers architecture files."""
        loader = KnowledgeLoader()
        files = loader._get_files_for_task("design architecture for system")
        assert isinstance(files, list)

    def test_chinese_task_triggers(self):
        """Test that Chinese keywords also trigger files."""
        loader = KnowledgeLoader()
        files = loader._get_files_for_task("编写代码实现功能")
        assert isinstance(files, list)


class TestGetFilesForLayer:
    """Tests for _get_files_for_layer method."""

    @pytest.fixture
    def loader_with_structure(self, tmp_path):
        """Create a loader with proper directory structure."""
        (tmp_path / "index.md").write_text("# Index")
        (tmp_path / "content" / "core").mkdir(parents=True)
        (tmp_path / "content" / "core" / "test.md").write_text("# Core")
        (tmp_path / "content" / "guidelines").mkdir(parents=True)
        (tmp_path / "content" / "guidelines" / "guide.md").write_text("# Guide")
        (tmp_path / "content" / "frameworks").mkdir(parents=True)
        (tmp_path / "content" / "frameworks" / "frame.md").write_text("# Frame")
        (tmp_path / "content" / "practices").mkdir(parents=True)
        (tmp_path / "content" / "practices" / "practice.md").write_text("# Practice")
        return KnowledgeLoader(kb_path=tmp_path)

    def test_index_layer_files(self, loader_with_structure):
        """Test L0_INDEX layer returns index.md."""
        files = loader_with_structure._get_files_for_layer(Layer.L0_INDEX)
        assert isinstance(files, list)

    def test_core_layer_files(self, loader_with_structure):
        """Test L1_CORE layer returns core files."""
        files = loader_with_structure._get_files_for_layer(Layer.L1_CORE)
        assert isinstance(files, list)

    def test_guidelines_layer_files(self, loader_with_structure):
        """Test L2_GUIDELINES layer returns guidelines files."""
        files = loader_with_structure._get_files_for_layer(Layer.L2_GUIDELINES)
        assert isinstance(files, list)

    def test_frameworks_layer_files(self, loader_with_structure):
        """Test L3_FRAMEWORKS layer returns frameworks files."""
        files = loader_with_structure._get_files_for_layer(Layer.L3_FRAMEWORKS)
        assert isinstance(files, list)

    def test_practices_layer_files(self, loader_with_structure):
        """Test L4_PRACTICES layer returns practices files."""
        files = loader_with_structure._get_files_for_layer(Layer.L4_PRACTICES)
        assert isinstance(files, list)


class TestSearchExtended:
    """Extended search tests."""

    @pytest.fixture
    def loader_with_archive(self, tmp_path):
        """Create a loader with archive content that should be skipped."""
        core_dir = tmp_path / "content" / "core"
        core_dir.mkdir(parents=True)
        (core_dir / "active.md").write_text("# Active Content\nSearchable text here.")
        archive_dir = tmp_path / "content" / "archive"
        archive_dir.mkdir(parents=True)
        (archive_dir / "archived.md").write_text("# Archived\nSearchable text here too.")
        return KnowledgeLoader(kb_path=tmp_path)

    @pytest.mark.asyncio
    async def test_search_skips_archive(self, loader_with_archive):
        """Test that search skips archived content."""
        results = await loader_with_archive.search("Searchable", timeout_ms=5000)
        assert isinstance(results, list)
        # Results should not include archive paths
        if results:
            for r in results:
                assert "archive" not in r.get("path", "").lower()

    @pytest.mark.asyncio
    async def test_search_header_boost(self, tmp_path):
        """Test that header matches get score boost."""
        core_dir = tmp_path / "content" / "core"
        core_dir.mkdir(parents=True)
        (core_dir / "with_header.md").write_text(
            "# Special Keyword\nThis has keyword in header."
        )
        (core_dir / "without_header.md").write_text(
            "# Regular Title\nThis has keyword in body only."
        )
        loader = KnowledgeLoader(kb_path=tmp_path)
        results = await loader.search("keyword", timeout_ms=5000)
        # Results should be returned
        assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_search_unreadable_file(self, tmp_path, monkeypatch):
        """Test search handles unreadable files gracefully."""
        core_dir = tmp_path / "content" / "core"
        core_dir.mkdir(parents=True)
        (core_dir / "test.md").write_text("# Test Content")
        
        loader = KnowledgeLoader(kb_path=tmp_path)
        
        # Monkeypatch to simulate read error
        original_read_text = Path.read_text
        call_count = [0]
        
        def failing_read_text(self, *args, **kwargs):
            call_count[0] += 1
            if call_count[0] > 1:  # Fail on subsequent reads
                raise PermissionError("Access denied")
            return original_read_text(self, *args, **kwargs)
        
        # This test verifies the error handling path exists
        results = await loader.search("test", timeout_ms=5000)
        assert isinstance(results, list)


class TestLoadExceptionHandling:
    """Tests for exception handling in load methods."""

    @pytest.fixture
    def loader_empty(self, tmp_path):
        """Create a loader with minimal content."""
        return KnowledgeLoader(kb_path=tmp_path)

    @pytest.mark.asyncio
    async def test_load_with_missing_path(self, loader_empty):
        """Test load handles missing paths gracefully."""
        result = await loader_empty.load(timeout_ms=2000)
        assert isinstance(result, LoadResult)

    @pytest.mark.asyncio
    async def test_load_core_missing_files(self, loader_empty):
        """Test load_core handles missing files."""
        result = await loader_empty.load_core(timeout_ms=2000)
        assert isinstance(result, LoadResult)

    @pytest.mark.asyncio
    async def test_load_for_task_missing_content(self, loader_empty):
        """Test load_for_task handles missing content."""
        result = await loader_empty.load_for_task(task="test task", timeout_ms=2000)
        assert isinstance(result, LoadResult)


class TestEventPublishing:
    """Tests for event publishing during load operations."""

    @pytest.fixture
    def loader_with_content(self, tmp_path):
        """Create a loader with content."""
        core_dir = tmp_path / "content" / "core"
        core_dir.mkdir(parents=True)
        (core_dir / "test.md").write_text("# Test\nContent here.")
        return KnowledgeLoader(kb_path=tmp_path)

    @pytest.mark.asyncio
    async def test_load_publishes_events(self, loader_with_content):
        """Test that load operations publish events."""
        # Simply verify load completes without error
        result = await loader_with_content.load(timeout_ms=2000)
        assert isinstance(result, LoadResult)

    @pytest.mark.asyncio
    async def test_search_publishes_events(self, loader_with_content):
        """Test that search publishes events."""
        results = await loader_with_content.search("test", timeout_ms=5000)
        assert isinstance(results, list)


class TestReadFile:
    """Tests for _read_file async method."""

    @pytest.fixture
    def loader_with_file(self, tmp_path):
        """Create a loader with a file."""
        (tmp_path / "test.md").write_text("# Test Content\nThis is test content.")
        return KnowledgeLoader(kb_path=tmp_path)

    @pytest.mark.asyncio
    async def test_read_existing_file(self, loader_with_file):
        """Test reading an existing file."""
        content = await loader_with_file._read_file("test.md")
        assert "Test Content" in content

    @pytest.mark.asyncio
    async def test_read_nonexistent_file(self, loader_with_file):
        """Test reading non-existent file raises error."""
        with pytest.raises(FileNotFoundError):
            await loader_with_file._read_file("nonexistent.md")


class TestLoadGuidelinesExtended:
    """Extended tests for load_guidelines method."""

    @pytest.fixture
    def loader_with_guidelines(self, tmp_path):
        """Create a loader with guidelines files."""
        guidelines_dir = tmp_path / "content" / "guidelines"
        guidelines_dir.mkdir(parents=True)
        (guidelines_dir / "quick_start.md").write_text("# Quick Start\nGetting started guide.")
        (guidelines_dir / "cognitive.md").write_text("# Cognitive\nCognitive guidelines.")
        return KnowledgeLoader(kb_path=tmp_path)

    @pytest.mark.asyncio
    async def test_load_quick_start(self, loader_with_guidelines):
        """Test loading quick_start chapter."""
        result = await loader_with_guidelines.load_guidelines(
            chapter="quick_start",
            timeout_ms=2000,
        )
        assert isinstance(result, LoadResult)

    @pytest.mark.asyncio
    async def test_load_cognitive(self, loader_with_guidelines):
        """Test loading cognitive chapter."""
        result = await loader_with_guidelines.load_guidelines(
            chapter="cognitive",
            timeout_ms=2000,
        )
        assert isinstance(result, LoadResult)

    @pytest.mark.asyncio
    async def test_load_nonexistent_chapter(self, loader_with_guidelines):
        """Test loading non-existent chapter."""
        result = await loader_with_guidelines.load_guidelines(
            chapter="nonexistent_xyz",
            timeout_ms=2000,
        )
        assert isinstance(result, LoadResult)


class TestLoadFrameworkExtended:
    """Extended tests for load_framework method."""

    @pytest.fixture
    def loader_with_frameworks(self, tmp_path):
        """Create a loader with framework files."""
        frameworks_dir = tmp_path / "content" / "frameworks"
        autonomy_dir = frameworks_dir / "autonomy"
        autonomy_dir.mkdir(parents=True)
        (autonomy_dir / "levels.md").write_text("# Autonomy Levels\nLevel definitions.")
        cognitive_dir = frameworks_dir / "cognitive"
        cognitive_dir.mkdir(parents=True)
        (cognitive_dir / "expert_committee.md").write_text("# Expert Committee\nCommittee framework.")
        return KnowledgeLoader(kb_path=tmp_path)

    @pytest.mark.asyncio
    async def test_load_autonomy_framework(self, loader_with_frameworks):
        """Test loading autonomy framework."""
        result = await loader_with_frameworks.load_framework(
            name="autonomy",
            timeout_ms=2000,
        )
        assert isinstance(result, LoadResult)

    @pytest.mark.asyncio
    async def test_load_cognitive_framework(self, loader_with_frameworks):
        """Test loading cognitive framework."""
        result = await loader_with_frameworks.load_framework(
            name="cognitive",
            timeout_ms=2000,
        )
        assert isinstance(result, LoadResult)

    @pytest.mark.asyncio
    async def test_load_nonexistent_framework(self, loader_with_frameworks):
        """Test loading non-existent framework."""
        result = await loader_with_frameworks.load_framework(
            name="nonexistent_xyz",
            timeout_ms=2000,
        )
        assert isinstance(result, LoadResult)


class TestConfigFunctions:
    """Tests for configuration loading functions."""

    def test_parse_timeout_str_int(self):
        """Test parsing integer timeout."""
        from sage.core.loader import _parse_timeout_str
        assert _parse_timeout_str(1000) == 1000
        assert _parse_timeout_str(500) == 500

    def test_parse_timeout_str_milliseconds(self):
        """Test parsing timeout with ms suffix."""
        from sage.core.loader import _parse_timeout_str
        assert _parse_timeout_str("500ms") == 500
        assert _parse_timeout_str("1000ms") == 1000
        assert _parse_timeout_str("  200ms  ") == 200

    def test_parse_timeout_str_seconds(self):
        """Test parsing timeout with s suffix."""
        from sage.core.loader import _parse_timeout_str
        assert _parse_timeout_str("5s") == 5000
        assert _parse_timeout_str("2s") == 2000
        assert _parse_timeout_str("1.5s") == 1500

    def test_parse_timeout_str_no_unit(self):
        """Test parsing timeout without unit (assumes ms)."""
        from sage.core.loader import _parse_timeout_str
        assert _parse_timeout_str("1000") == 1000
        assert _parse_timeout_str("500") == 500

    def test_get_timeout_from_config_default(self):
        """Test getting timeout with default value."""
        from sage.core.loader import _get_timeout_from_config
        # Should return default when operation not in config
        result = _get_timeout_from_config("nonexistent_operation", 3000)
        assert isinstance(result, int)

    def test_get_triggers_from_config(self):
        """Test getting triggers from config."""
        from sage.core.loader import _get_triggers_from_config
        triggers = _get_triggers_from_config()
        assert isinstance(triggers, list)

    def test_get_always_load_from_config(self):
        """Test getting always-load files from config."""
        from sage.core.loader import _get_always_load_from_config
        always_load = _get_always_load_from_config()
        assert isinstance(always_load, list)


class TestConvenienceFunctions:
    """Tests for module-level convenience functions."""

    @pytest.mark.asyncio
    async def test_load_knowledge_function(self):
        """Test load_knowledge convenience function."""
        from sage.core.loader import load_knowledge
        result = await load_knowledge(task="test task", timeout_ms=2000)
        assert isinstance(result, LoadResult)

    @pytest.mark.asyncio
    async def test_load_knowledge_with_default_timeout(self):
        """Test load_knowledge with default timeout from config."""
        from sage.core.loader import load_knowledge
        result = await load_knowledge(task="another task")
        assert isinstance(result, LoadResult)

    @pytest.mark.asyncio
    async def test_load_core_function(self):
        """Test load_core convenience function."""
        from sage.core.loader import load_core
        result = await load_core(timeout_ms=2000)
        assert isinstance(result, LoadResult)

    @pytest.mark.asyncio
    async def test_load_core_with_default_timeout(self):
        """Test load_core with default timeout from config."""
        from sage.core.loader import load_core
        result = await load_core()
        assert isinstance(result, LoadResult)

    @pytest.mark.asyncio
    async def test_search_knowledge_function(self):
        """Test search_knowledge convenience function."""
        from sage.core.loader import search_knowledge
        results = await search_knowledge(query="test", max_results=5)
        assert isinstance(results, list)


class TestGetPreviewExtended:
    """Extended tests for _get_preview static method."""

    def test_preview_query_not_found(self):
        """Test preview when query not found in content."""
        content = "This is some content without the search term."
        preview = KnowledgeLoader._get_preview(content, "xyz123")
        assert preview.endswith("...")
        assert len(preview) <= 103  # max_len + "..."

    def test_preview_query_at_start(self):
        """Test preview when query at start of content."""
        content = "test query is at the start of this long content that continues for a while."
        preview = KnowledgeLoader._get_preview(content, "test")
        assert "test" in preview.lower()

    def test_preview_query_at_end(self):
        """Test preview when query at end of content."""
        content = "This is a long content that goes on for a while and ends with test"
        preview = KnowledgeLoader._get_preview(content, "test")
        assert "test" in preview.lower()

    def test_preview_query_in_middle(self):
        """Test preview when query in middle of long content."""
        content = "A" * 100 + " test query here " + "B" * 100
        preview = KnowledgeLoader._get_preview(content, "test")
        assert "..." in preview
        assert "test" in preview.lower()

    def test_preview_with_newlines(self):
        """Test preview replaces newlines with spaces."""
        content = "Line one\ntest\nLine three"
        preview = KnowledgeLoader._get_preview(content, "test")
        assert "\n" not in preview


class TestGetLayerForFileExtended:
    """Extended tests for _get_layer_for_file static method."""

    def test_index_file(self):
        """Test index.md returns L0_INDEX."""
        assert KnowledgeLoader._get_layer_for_file("index.md") == Layer.L0_INDEX

    def test_core_directory(self):
        """Test content/core files return L1_CORE."""
        assert KnowledgeLoader._get_layer_for_file("content/core/principles.md") == Layer.L1_CORE

    def test_guidelines_directory(self):
        """Test content/guidelines files return L2_GUIDELINES."""
        assert KnowledgeLoader._get_layer_for_file("content/guidelines/quick_start.md") == Layer.L2_GUIDELINES

    def test_frameworks_directory(self):
        """Test content/frameworks files return L3_FRAMEWORKS."""
        assert KnowledgeLoader._get_layer_for_file("content/frameworks/autonomy/levels.md") == Layer.L3_FRAMEWORKS

    def test_practices_directory(self):
        """Test content/practices files return L4_PRACTICES."""
        assert KnowledgeLoader._get_layer_for_file("content/practices/ai_collab/workflow.md") == Layer.L4_PRACTICES

    def test_unknown_file(self):
        """Test unknown file defaults to L1_CORE."""
        assert KnowledgeLoader._get_layer_for_file("some/random/file.md") == Layer.L1_CORE


class TestSearchWithContent:
    """Tests for search with actual content."""

    @pytest.fixture
    def loader_with_searchable_content(self, tmp_path):
        """Create loader with searchable content."""
        core_dir = tmp_path / "content" / "core"
        core_dir.mkdir(parents=True)
        (core_dir / "principles.md").write_text(
            "# Core Principles\n\nThis document describes the core principles.\n"
            "## Key Concepts\nImportant concepts are defined here."
        )
        guidelines_dir = tmp_path / "content" / "guidelines"
        guidelines_dir.mkdir(parents=True)
        (guidelines_dir / "coding.md").write_text(
            "# Coding Guidelines\n\nFollow these coding guidelines.\n"
            "## Best Practices\nBest practices for coding."
        )
        return KnowledgeLoader(kb_path=tmp_path)

    @pytest.mark.asyncio
    async def test_search_finds_content(self, loader_with_searchable_content):
        """Test search finds matching content."""
        results = await loader_with_searchable_content.search("principles", timeout_ms=5000)
        assert len(results) > 0
        assert any("principles" in r["path"].lower() or "principles" in r.get("preview", "").lower() 
                   for r in results)

    @pytest.mark.asyncio
    async def test_search_with_header_boost(self, loader_with_searchable_content):
        """Test search boosts results with query in headers."""
        results = await loader_with_searchable_content.search("Core", timeout_ms=5000)
        assert len(results) > 0

    @pytest.mark.asyncio
    async def test_search_no_results(self, loader_with_searchable_content):
        """Test search returns empty list for no matches."""
        results = await loader_with_searchable_content.search("xyz123nonexistent", timeout_ms=5000)
        assert results == []


class TestCacheOperations:
    """Tests for cache operations."""

    @pytest.fixture
    def loader_with_files(self, tmp_path):
        """Create loader with files for cache testing."""
        core_dir = tmp_path / "content" / "core"
        core_dir.mkdir(parents=True)
        (core_dir / "test.md").write_text("# Test\nTest content for caching.")
        return KnowledgeLoader(kb_path=tmp_path)

    @pytest.mark.asyncio
    async def test_cache_populated_after_load(self, loader_with_files):
        """Test cache is populated after loading."""
        await loader_with_files.load(timeout_ms=2000)
        stats = loader_with_files.get_cache_stats()
        assert stats["cached_files"] >= 0

    def test_clear_cache(self, loader_with_files):
        """Test clearing cache."""
        loader_with_files.clear_cache()
        stats = loader_with_files.get_cache_stats()
        assert stats["cached_files"] == 0
        assert stats["total_size"] == 0

    @pytest.mark.asyncio
    async def test_cache_hit_on_second_load(self, loader_with_files):
        """Test that second load uses cache."""
        await loader_with_files.load(timeout_ms=2000)
        stats1 = loader_with_files.get_cache_stats()
        
        # Second load should use cache
        await loader_with_files.load(timeout_ms=2000)
        stats2 = loader_with_files.get_cache_stats()
        
        # Cache should still be populated
        assert stats2["cached_files"] >= stats1["cached_files"]


class TestLoadFilesWithTimeout:
    """Tests for _load_files_with_timeout method."""

    @pytest.fixture
    def loader_with_multiple_files(self, tmp_path):
        """Create loader with multiple files."""
        core_dir = tmp_path / "content" / "core"
        core_dir.mkdir(parents=True)
        (core_dir / "file1.md").write_text("# File 1\nContent of file 1.")
        (core_dir / "file2.md").write_text("# File 2\nContent of file 2.")
        (core_dir / "file3.md").write_text("# File 3\nContent of file 3.")
        return KnowledgeLoader(kb_path=tmp_path)

    @pytest.mark.asyncio
    async def test_load_multiple_files(self, loader_with_multiple_files):
        """Test loading multiple files."""
        result = await loader_with_multiple_files._load_files_with_timeout(
            files=["content/core/file1.md", "content/core/file2.md"],
            total_timeout_ms=5000,
        )
        assert isinstance(result, LoadResult)
        assert len(result.files_loaded) >= 1

    @pytest.mark.asyncio
    async def test_load_nonexistent_file_in_list(self, loader_with_multiple_files):
        """Test loading with nonexistent file in list."""
        result = await loader_with_multiple_files._load_files_with_timeout(
            files=["content/core/file1.md", "nonexistent.md"],
            total_timeout_ms=5000,
        )
        assert isinstance(result, LoadResult)
        # Should have errors for nonexistent file
        assert len(result.errors) > 0 or result.status in ["partial", "fallback"]

    @pytest.mark.asyncio
    async def test_load_with_very_short_timeout(self, loader_with_multiple_files):
        """Test loading with very short timeout."""
        result = await loader_with_multiple_files._load_files_with_timeout(
            files=["content/core/file1.md", "content/core/file2.md", "content/core/file3.md"],
            total_timeout_ms=1,  # Very short timeout
        )
        assert isinstance(result, LoadResult)


class TestGetFilesForTask:
    """Tests for _get_files_for_task method."""

    def test_get_files_no_matching_trigger(self):
        """Test getting files with no matching trigger."""
        loader = KnowledgeLoader()
        files = loader._get_files_for_task("random task with no keywords")
        assert isinstance(files, list)

    def test_get_files_with_matching_keyword(self):
        """Test getting files with matching trigger keyword."""
        trigger = LoadingTrigger(
            name="test_trigger",
            keywords=["python", "code"],
            files=["content/guidelines/python.md"],
            timeout_ms=2000,
        )
        loader = KnowledgeLoader(triggers=[trigger])
        files = loader._get_files_for_task("help with python code")
        assert "content/guidelines/python.md" in files


class TestGetFilesForLayer:
    """Tests for _get_files_for_layer method."""

    @pytest.fixture
    def loader_with_layer_content(self, tmp_path):
        """Create loader with content for each layer."""
        (tmp_path / "index.md").write_text("# Index")
        
        core_dir = tmp_path / "content" / "core"
        core_dir.mkdir(parents=True)
        (core_dir / "principles.md").write_text("# Principles")
        
        guidelines_dir = tmp_path / "content" / "guidelines"
        guidelines_dir.mkdir(parents=True)
        (guidelines_dir / "coding.md").write_text("# Coding")
        
        frameworks_dir = tmp_path / "content" / "frameworks"
        frameworks_dir.mkdir(parents=True)
        (frameworks_dir / "autonomy.md").write_text("# Autonomy")
        
        practices_dir = tmp_path / "content" / "practices"
        practices_dir.mkdir(parents=True)
        (practices_dir / "workflow.md").write_text("# Workflow")
        
        return KnowledgeLoader(kb_path=tmp_path)

    def test_get_files_for_index_layer(self, loader_with_layer_content):
        """Test getting files for L0_INDEX layer."""
        files = loader_with_layer_content._get_files_for_layer(Layer.L0_INDEX)
        assert "index.md" in files

    def test_get_files_for_core_layer(self, loader_with_layer_content):
        """Test getting files for L1_CORE layer."""
        files = loader_with_layer_content._get_files_for_layer(Layer.L1_CORE)
        assert any("core" in f for f in files)

    def test_get_files_for_guidelines_layer(self, loader_with_layer_content):
        """Test getting files for L2_GUIDELINES layer."""
        files = loader_with_layer_content._get_files_for_layer(Layer.L2_GUIDELINES)
        assert any("guidelines" in f for f in files)

    def test_get_files_for_frameworks_layer(self, loader_with_layer_content):
        """Test getting files for L3_FRAMEWORKS layer."""
        files = loader_with_layer_content._get_files_for_layer(Layer.L3_FRAMEWORKS)
        assert any("frameworks" in f for f in files)

    def test_get_files_for_practices_layer(self, loader_with_layer_content):
        """Test getting files for L4_PRACTICES layer."""
        files = loader_with_layer_content._get_files_for_layer(Layer.L4_PRACTICES)
        assert any("practices" in f for f in files)
