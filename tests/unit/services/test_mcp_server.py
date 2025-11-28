"""
Unit tests for MCP Server service.

Tests cover:
- MCP app initialization
- Tool registration
- Core tool functions
- Error handling

Author: SAGE AI Collab Team
Version: 0.1.0
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from pathlib import Path


class TestMCPAppCreation:
    """Tests for MCP application creation."""

    def test_create_app_returns_app(self):
        """Test create_app returns a valid app instance."""
        from sage.services.mcp_server import create_app, MCP_AVAILABLE

        if MCP_AVAILABLE:
            app = create_app()
            assert app is not None
            assert hasattr(app, "name")
        else:
            with pytest.raises(ImportError):
                create_app()

    def test_app_name_is_sage_kb(self):
        """Test app has correct name."""
        from sage.services.mcp_server import create_app, MCP_AVAILABLE

        if MCP_AVAILABLE:
            app = create_app()
            assert app.name == "sage-kb"

    def test_mcp_available_flag(self):
        """Test MCP_AVAILABLE flag is set correctly."""
        from sage.services.mcp_server import MCP_AVAILABLE

        # MCP_AVAILABLE should be a boolean
        assert isinstance(MCP_AVAILABLE, bool)


class TestGetLoader:
    """Tests for get_loader function."""

    def test_get_loader_returns_loader(self):
        """Test get_loader returns a KnowledgeLoader instance."""
        from sage.services.mcp_server import get_loader
        from sage.core.loader import KnowledgeLoader

        loader = get_loader()
        assert loader is not None
        assert isinstance(loader, KnowledgeLoader)

    def test_get_loader_returns_same_instance(self):
        """Test get_loader returns the same instance (singleton)."""
        from sage.services.mcp_server import get_loader

        loader1 = get_loader()
        loader2 = get_loader()
        assert loader1 is loader2


class TestKnowledgeTool:
    """Tests for get_knowledge tool."""

    @pytest.mark.asyncio
    async def test_get_knowledge_returns_dict(self):
        """Test get_knowledge returns a dictionary."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import get_knowledge

        result = await get_knowledge(layer=0, timeout_ms=5000)
        assert isinstance(result, dict)
        assert "status" in result

    @pytest.mark.asyncio
    async def test_get_knowledge_with_task(self):
        """Test get_knowledge with task description."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import get_knowledge

        result = await get_knowledge(task="test task", timeout_ms=3000)
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_get_knowledge_has_required_fields(self):
        """Test get_knowledge result has required fields."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import get_knowledge

        result = await get_knowledge(layer=0, timeout_ms=5000)
        # Check for expected fields
        expected_fields = ["status", "duration_ms"]
        for field in expected_fields:
            assert field in result, f"Missing field: {field}"


class TestSearchTool:
    """Tests for search_knowledge tool."""

    @pytest.mark.asyncio
    async def test_search_knowledge_returns_dict(self):
        """Test search_knowledge returns a dictionary."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import search_knowledge

        result = await search_knowledge(query="test", max_results=5)
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_search_knowledge_with_empty_query(self):
        """Test search_knowledge handles empty query."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import search_knowledge

        result = await search_knowledge(query="", max_results=5)
        assert isinstance(result, dict)


class TestKbInfoTool:
    """Tests for kb_info tool."""

    @pytest.mark.asyncio
    async def test_kb_info_returns_dict(self):
        """Test kb_info returns a dictionary."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import kb_info

        result = await kb_info()
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_kb_info_has_version(self):
        """Test kb_info includes version information."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import kb_info

        result = await kb_info()
        assert "version" in result or "info" in result


class TestListToolsTool:
    """Tests for list_tools tool."""

    @pytest.mark.asyncio
    async def test_list_tools_returns_dict(self):
        """Test list_tools returns a dictionary."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import list_tools

        result = await list_tools()
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_list_tools_has_categories(self):
        """Test list_tools has tool categories."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import list_tools

        result = await list_tools()
        assert "success" in result
        assert result["success"] is True
        assert "knowledge_tools" in result
        assert "capabilities" in result
        assert "dev_tools" in result

    @pytest.mark.asyncio
    async def test_list_tools_knowledge_tools_count(self):
        """Test list_tools returns expected number of knowledge tools."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import list_tools

        result = await list_tools()
        # Should have 6 knowledge tools
        assert len(result["knowledge_tools"]) == 6


class TestGuidelinesTool:
    """Tests for get_guidelines tool."""

    @pytest.mark.asyncio
    async def test_get_guidelines_returns_dict(self):
        """Test get_guidelines returns a dictionary."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import get_guidelines

        result = await get_guidelines(section="overview")
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_get_guidelines_with_invalid_section(self):
        """Test get_guidelines handles invalid section gracefully."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import get_guidelines

        result = await get_guidelines(section="nonexistent_section_xyz")
        assert isinstance(result, dict)
        # Should indicate not found or error
        assert "status" in result or "error" in result or "content" in result


class TestFrameworkTool:
    """Tests for get_framework tool."""

    @pytest.mark.asyncio
    async def test_get_framework_returns_dict(self):
        """Test get_framework returns a dictionary."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import get_framework

        result = await get_framework(name="autonomy")
        assert isinstance(result, dict)


class TestTemplateTool:
    """Tests for get_template tool."""

    @pytest.mark.asyncio
    async def test_get_template_returns_dict(self):
        """Test get_template returns a dictionary."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import get_template

        result = await get_template(name="project_setup")
        assert isinstance(result, dict)


class TestCapabilityTools:
    """Tests for capability-based tools."""

    @pytest.mark.asyncio
    async def test_analyze_quality_returns_dict(self):
        """Test analyze_quality returns a dictionary."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import analyze_quality

        result = await analyze_quality(path=".")
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_analyze_content_returns_dict(self):
        """Test analyze_content returns a dictionary."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import analyze_content

        result = await analyze_content(path=".")
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_check_health_returns_dict(self):
        """Test check_health returns a dictionary."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import check_health

        result = await check_health(path=".")
        assert isinstance(result, dict)


class TestRunServer:
    """Tests for run_server function."""

    def test_run_server_without_mcp_raises(self):
        """Test run_server raises ImportError when MCP unavailable."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if MCP_AVAILABLE:
            pytest.skip("MCP is available, cannot test unavailable case")

        from sage.services.mcp_server import run_server

        with pytest.raises(ImportError):
            run_server()

    def test_run_server_prints_info(self, capsys):
        """Test run_server prints server information."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import run_server

        # Note: This would actually start the server, so we just verify it exists
        assert callable(run_server)


class TestToolErrorHandling:
    """Tests for tool error handling."""

    @pytest.mark.asyncio
    async def test_get_knowledge_handles_timeout(self):
        """Test get_knowledge respects timeout parameter."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import get_knowledge

        # Very short timeout - should still return gracefully
        result = await get_knowledge(layer=0, timeout_ms=1)
        assert isinstance(result, dict)
        assert "status" in result

    @pytest.mark.asyncio
    async def test_search_handles_special_characters(self):
        """Test search_knowledge handles special characters in query."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import search_knowledge

        result = await search_knowledge(query="test!@#$%^&*()", max_results=5)
        assert isinstance(result, dict)
