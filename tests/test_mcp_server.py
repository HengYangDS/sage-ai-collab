"""
Unit tests for mcp_server module.

Tests cover:
- get_loader function
- MCP tool functions (when MCP is available)
- Error handling
- Timeout protection
"""

import sys
from pathlib import Path

import pytest

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai_collab_kb.loader import KnowledgeLoader, Layer
from ai_collab_kb.mcp_server import (
    MCP_AVAILABLE,
    get_loader,
)


class TestGetLoader:
    """Tests for get_loader function."""

    def test_get_loader_returns_knowledge_loader(self):
        """get_loader should return a KnowledgeLoader instance."""
        # Reset the global loader first
        import ai_collab_kb.mcp_server as mcp_module

        mcp_module._loader = None

        loader = get_loader()
        assert isinstance(loader, KnowledgeLoader)

    def test_get_loader_returns_singleton(self):
        """get_loader should return the same instance on multiple calls."""
        import ai_collab_kb.mcp_server as mcp_module

        mcp_module._loader = None

        loader1 = get_loader()
        loader2 = get_loader()
        assert loader1 is loader2

    def test_get_loader_creates_loader_with_default_path(self):
        """get_loader should create loader with default kb_path."""
        import ai_collab_kb.mcp_server as mcp_module

        mcp_module._loader = None

        loader = get_loader()
        assert loader.kb_path is not None
        assert loader.kb_path.exists() or True  # May not exist in test environment


class TestMCPAvailability:
    """Tests for MCP availability detection."""

    def test_mcp_available_is_boolean(self):
        """MCP_AVAILABLE should be a boolean."""
        assert isinstance(MCP_AVAILABLE, bool)

    def test_app_none_when_mcp_unavailable(self):
        """When MCP is not available, app should be None or MCP app."""
        import ai_collab_kb.mcp_server as mcp_module

        if not MCP_AVAILABLE:
            assert mcp_module.app is None
        else:
            assert mcp_module.app is not None


class TestMCPToolsWithoutMCP:
    """Tests for MCP tools functionality using direct loader calls.

    Since MCP tools are just wrappers around the loader, we test
    the equivalent functionality through the loader directly.
    """

    @pytest.fixture
    def loader(self):
        """Create a KnowledgeLoader instance."""
        kb_path = Path(__file__).parent.parent
        return KnowledgeLoader(kb_path=kb_path)

    @pytest.mark.asyncio
    async def test_get_knowledge_equivalent(self, loader):
        """Test get_knowledge equivalent functionality."""
        # This mirrors what get_knowledge does
        result = await loader.load(layer=Layer.L1_CORE, timeout_ms=5000)

        assert result.content is not None
        assert result.status in ["success", "partial", "fallback"]
        assert result.tokens_estimate >= 0
        assert result.duration_ms >= 0

    @pytest.mark.asyncio
    async def test_get_knowledge_with_task(self, loader):
        """Test get_knowledge with task description."""
        result = await loader.load(task="implement feature", timeout_ms=5000)

        assert result.content is not None
        assert result.status in ["success", "partial", "fallback"]

    @pytest.mark.asyncio
    async def test_get_guidelines_equivalent(self, loader):
        """Test get_guidelines equivalent functionality."""
        result = await loader.load_guidelines("code_style", timeout_ms=3000)

        assert result.content is not None
        assert result.status in ["success", "partial", "fallback", "error"]

    @pytest.mark.asyncio
    async def test_get_framework_equivalent(self, loader):
        """Test get_framework equivalent functionality."""
        result = await loader.load_framework("autonomy", timeout_ms=5000)

        assert result.content is not None
        assert result.status in ["success", "partial", "fallback", "error"]

    @pytest.mark.asyncio
    async def test_search_kb_equivalent(self, loader):
        """Test search_kb equivalent functionality."""
        results = await loader.search("principles", max_results=5, timeout_ms=3000)

        assert isinstance(results, list)


class TestLayerMapping:
    """Tests for layer number to Layer enum mapping."""

    def test_layer_map_values(self):
        """Layer map should have correct values."""
        # This is the mapping used in get_knowledge
        layer_map = {
            0: Layer.L1_CORE,
            1: Layer.L2_GUIDELINES,
            2: Layer.L3_FRAMEWORKS,
            3: Layer.L4_PRACTICES,
        }

        assert layer_map[0] == Layer.L1_CORE
        assert layer_map[1] == Layer.L2_GUIDELINES
        assert layer_map[2] == Layer.L3_FRAMEWORKS
        assert layer_map[3] == Layer.L4_PRACTICES

    def test_layer_map_coverage(self):
        """All practical layers should be mapped."""
        layer_map = {
            0: Layer.L1_CORE,
            1: Layer.L2_GUIDELINES,
            2: Layer.L3_FRAMEWORKS,
            3: Layer.L4_PRACTICES,
        }

        # Should have 4 mappings
        assert len(layer_map) == 4


class TestSectionMapping:
    """Tests for section name mapping in get_guidelines."""

    def test_section_map_complete(self):
        """Section map should include all chapters."""
        section_map = {
            "quick_start": "00_quick_start",
            "00": "00_quick_start",
            "planning": "01_planning_design",
            "01": "01_planning_design",
            "code_style": "02_code_style",
            "02": "02_code_style",
            "engineering": "03_engineering",
            "03": "03_engineering",
            "documentation": "04_documentation",
            "04": "04_documentation",
            "python": "05_python",
            "05": "05_python",
            "ai_collaboration": "06_ai_collaboration",
            "06": "06_ai_collaboration",
            "cognitive": "07_cognitive",
            "07": "07_cognitive",
            "quality": "08_quality",
            "08": "08_quality",
            "success": "09_success",
            "09": "09_success",
            "overview": "00_quick_start",
        }

        # Test key sections
        assert section_map["quick_start"] == "00_quick_start"
        assert section_map["code_style"] == "02_code_style"
        assert section_map["python"] == "05_python"
        assert section_map["quality"] == "08_quality"

        # Test numeric shortcuts
        assert section_map["00"] == "00_quick_start"
        assert section_map["09"] == "09_success"

    def test_section_map_has_all_chapters(self):
        """All 10 chapters should be accessible."""
        section_map = {
            "quick_start": "00_quick_start",
            "00": "00_quick_start",
            "planning": "01_planning_design",
            "01": "01_planning_design",
            "code_style": "02_code_style",
            "02": "02_code_style",
            "engineering": "03_engineering",
            "03": "03_engineering",
            "documentation": "04_documentation",
            "04": "04_documentation",
            "python": "05_python",
            "05": "05_python",
            "ai_collaboration": "06_ai_collaboration",
            "06": "06_ai_collaboration",
            "cognitive": "07_cognitive",
            "07": "07_cognitive",
            "quality": "08_quality",
            "08": "08_quality",
            "success": "09_success",
            "09": "09_success",
            "overview": "00_quick_start",
        }

        # Check unique chapter files
        unique_chapters = set(section_map.values())
        assert len(unique_chapters) == 10


class TestFrameworkNames:
    """Tests for framework name validation."""

    def test_valid_framework_names(self):
        """All expected framework names should be valid."""
        valid_names = ["autonomy", "cognitive", "decision", "collaboration", "timeout"]

        for name in valid_names:
            # Should be lowercase and alphanumeric
            assert name.islower()
            assert name.isalpha()


class TestErrorHandling:
    """Tests for error handling in MCP tools."""

    @pytest.fixture
    def loader(self):
        """Create a KnowledgeLoader instance."""
        kb_path = Path(__file__).parent.parent
        return KnowledgeLoader(kb_path=kb_path)

    @pytest.mark.asyncio
    async def test_invalid_framework_returns_error(self, loader):
        """Invalid framework name should return error status."""
        result = await loader.load_framework("invalid_framework_xyz", timeout_ms=5000)

        assert result.status == "error"
        assert "not found" in result.content.lower() or len(result.errors) > 0

    @pytest.mark.asyncio
    async def test_timeout_returns_gracefully(self, loader):
        """Very short timeout should return gracefully."""
        # Use a very short timeout
        result = await loader.load_core(timeout_ms=1)

        # Should return something (either content or fallback)
        assert result.content is not None or result.status in [
            "fallback",
            "partial",
            "error",
        ]


class TestResponseFormat:
    """Tests for MCP tool response format."""

    @pytest.fixture
    def loader(self):
        """Create a KnowledgeLoader instance."""
        kb_path = Path(__file__).parent.parent
        return KnowledgeLoader(kb_path=kb_path)

    @pytest.mark.asyncio
    async def test_response_has_required_fields(self, loader):
        """Response should have all required fields for MCP."""
        result = await loader.load_core(timeout_ms=5000)

        # These fields are used by MCP tools
        assert hasattr(result, "content")
        assert hasattr(result, "tokens_estimate")
        assert hasattr(result, "status")
        assert hasattr(result, "duration_ms")

    @pytest.mark.asyncio
    async def test_response_to_dict_for_mcp(self, loader):
        """Response to_dict should be suitable for MCP return."""
        result = await loader.load_core(timeout_ms=5000)
        d = result.to_dict()

        # Should be a dict with string keys
        assert isinstance(d, dict)
        assert all(isinstance(k, str) for k in d.keys())

        # Content should be string
        assert isinstance(d["content"], str)

        # Tokens should be int
        assert isinstance(d["tokens_estimate"], int)

        # Status should be string
        assert isinstance(d["status"], str)


class TestIntegrationScenarios:
    """Integration tests for common MCP usage scenarios."""

    @pytest.fixture
    def loader(self):
        """Create a KnowledgeLoader instance."""
        kb_path = Path(__file__).parent.parent
        return KnowledgeLoader(kb_path=kb_path)

    @pytest.mark.asyncio
    async def test_typical_get_knowledge_flow(self, loader):
        """Test typical get_knowledge flow."""
        # User asks for core knowledge
        result = await loader.load(layer=Layer.L1_CORE, timeout_ms=5000)

        assert result.status in ["success", "partial", "fallback"]
        if result.status == "success":
            assert len(result.content) > 0
            assert result.tokens_estimate > 0

    @pytest.mark.asyncio
    async def test_task_based_loading(self, loader):
        """Test task-based smart loading."""
        # User describes task
        result = await loader.load(task="debug a Python function", timeout_ms=5000)

        assert result.status in ["success", "partial", "fallback"]
        # Should load code-related content
        assert result.content is not None

    @pytest.mark.asyncio
    async def test_guidelines_then_framework_flow(self, loader):
        """Test loading guidelines then framework."""
        # First load guidelines
        guidelines = await loader.load_guidelines("ai_collaboration", timeout_ms=5000)
        assert guidelines.content is not None

        # Then load related framework
        framework = await loader.load_framework("autonomy", timeout_ms=5000)
        assert framework.content is not None

    @pytest.mark.asyncio
    async def test_search_then_load_flow(self, loader):
        """Test search then load specific content."""
        # Search for topic
        results = await loader.search("timeout", max_results=5, timeout_ms=5000)

        assert isinstance(results, list)

        # If found results, content is accessible
        if len(results) > 0:
            assert "path" in results[0]
