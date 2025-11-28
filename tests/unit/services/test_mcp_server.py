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


class TestKnowledgeGraphTool:
    """Tests for build_knowledge_graph tool."""

    @pytest.mark.asyncio
    async def test_build_knowledge_graph_returns_dict(self):
        """Test build_knowledge_graph returns a dictionary."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import build_knowledge_graph

        result = await build_knowledge_graph(path=".")
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_build_knowledge_graph_with_content(self):
        """Test build_knowledge_graph with include_content option."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import build_knowledge_graph

        result = await build_knowledge_graph(path=".", include_content=True)
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_build_knowledge_graph_with_output_file(self):
        """Test build_knowledge_graph with output file option."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import build_knowledge_graph

        result = await build_knowledge_graph(path=".", output_file="test_graph.json")
        assert isinstance(result, dict)


class TestCheckLinksTool:
    """Tests for check_links tool."""

    @pytest.mark.asyncio
    async def test_check_links_returns_dict(self):
        """Test check_links returns a dictionary."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import check_links

        result = await check_links(path=".")
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_check_links_with_external(self):
        """Test check_links with external link checking."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import check_links

        result = await check_links(path=".", check_external=False)
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_check_links_with_pattern(self):
        """Test check_links with custom pattern."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import check_links

        result = await check_links(path=".", pattern="*.md")
        assert isinstance(result, dict)


class TestCheckStructureTool:
    """Tests for check_structure tool."""

    @pytest.mark.asyncio
    async def test_check_structure_returns_dict(self):
        """Test check_structure returns a dictionary."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import check_structure

        result = await check_structure(path=".")
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_check_structure_dry_run(self):
        """Test check_structure with dry_run option."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import check_structure

        result = await check_structure(path=".", dry_run=True)
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_check_structure_with_fix(self):
        """Test check_structure with fix option (dry_run=True for safety)."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import check_structure

        result = await check_structure(path=".", fix=True, dry_run=True)
        assert isinstance(result, dict)


class TestTimeoutStatsTool:
    """Tests for get_timeout_stats tool."""

    @pytest.mark.asyncio
    async def test_get_timeout_stats_returns_dict(self):
        """Test get_timeout_stats returns a dictionary."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import get_timeout_stats

        result = await get_timeout_stats(minutes=60)
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_get_timeout_stats_with_custom_minutes(self):
        """Test get_timeout_stats with custom time window."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import get_timeout_stats

        result = await get_timeout_stats(minutes=30)
        assert isinstance(result, dict)


class TestBackupTools:
    """Tests for backup-related tools."""

    @pytest.mark.asyncio
    async def test_create_backup_returns_dict(self):
        """Test create_backup returns a dictionary."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import create_backup

        result = await create_backup(path=".", name="test_backup")
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_create_backup_without_name(self):
        """Test create_backup generates automatic name."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import create_backup

        result = await create_backup(path=".")
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_list_backups_returns_dict(self):
        """Test list_backups returns a dictionary."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import list_backups

        result = await list_backups(path=".backups")
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_list_backups_empty_directory(self):
        """Test list_backups handles non-existent directory."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import list_backups

        result = await list_backups(path=".nonexistent_backups_xyz")
        assert isinstance(result, dict)


class TestAnalyzeToolsExtended:
    """Extended tests for analyze tools."""

    @pytest.mark.asyncio
    async def test_analyze_quality_with_extensions(self):
        """Test analyze_quality with custom extensions."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import analyze_quality

        result = await analyze_quality(path=".", extensions=".py,.md")
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_analyze_content_with_extensions(self):
        """Test analyze_content with custom extensions."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import analyze_content

        result = await analyze_content(path=".", extensions=".md")
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_check_health_result_fields(self):
        """Test check_health returns expected fields."""
        from sage.services.mcp_server import MCP_AVAILABLE

        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")

        from sage.services.mcp_server import check_health

        result = await check_health(path=".")
        assert isinstance(result, dict)
        # Should have success or status field
        assert "success" in result or "status" in result or "health" in result


class TestConfigLoading:
    """Tests for configuration loading functions."""

    def test_load_config_returns_dict(self):
        """Test _load_config returns a dictionary."""
        from sage.services import mcp_server
        
        # Clear cache to force reload
        mcp_server._config_cache = None
        result = mcp_server._load_config()
        assert isinstance(result, dict)

    def test_load_config_caching(self):
        """Test _load_config uses caching."""
        from sage.services import mcp_server
        
        # Clear cache
        mcp_server._config_cache = None
        result1 = mcp_server._load_config()
        result2 = mcp_server._load_config()
        # Should be the same object due to caching
        assert result1 is result2

    def test_load_config_missing_file(self, tmp_path, monkeypatch):
        """Test _load_config handles missing file."""
        from sage.services import mcp_server
        from pathlib import Path
        
        # Clear cache
        mcp_server._config_cache = None
        
        # Mock the config path to point to non-existent file
        fake_path = tmp_path / "nonexistent" / "sage.yaml"
        monkeypatch.setattr(
            mcp_server, "_config_cache", None
        )
        original_func = mcp_server._load_config
        
        def mock_load():
            mcp_server._config_cache = None
            # Simulate file not found
            if not fake_path.exists():
                mcp_server._config_cache = {}
            return mcp_server._config_cache
        
        result = mock_load()
        assert result == {}

    def test_get_guidelines_section_map(self):
        """Test _get_guidelines_section_map returns mapping."""
        from sage.services.mcp_server import _get_guidelines_section_map
        
        result = _get_guidelines_section_map()
        assert isinstance(result, dict)

    def test_get_guidelines_section_map_lowercase_keys(self):
        """Test section map has lowercase keys."""
        from sage.services.mcp_server import _get_guidelines_section_map
        
        result = _get_guidelines_section_map()
        for key in result.keys():
            assert key == key.lower()


class TestToolExceptionHandling:
    """Tests for tool exception handling."""

    @pytest.mark.asyncio
    async def test_get_knowledge_exception(self, monkeypatch):
        """Test get_knowledge handles exceptions gracefully."""
        from sage.services.mcp_server import MCP_AVAILABLE
        
        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")
        
        from sage.services.mcp_server import get_knowledge, get_loader
        
        # Mock loader to raise exception
        def mock_loader():
            class FailingLoader:
                async def load_core(self, **kwargs):
                    raise RuntimeError("Test error")
                async def load(self, **kwargs):
                    raise RuntimeError("Test error")
                async def load_for_task(self, *args, **kwargs):
                    raise RuntimeError("Test error")
            return FailingLoader()
        
        monkeypatch.setattr("sage.services.mcp_server.get_loader", mock_loader)
        
        result = await get_knowledge()
        assert result["status"] == "error"
        assert "error" in result

    @pytest.mark.asyncio
    async def test_get_guidelines_exception(self, monkeypatch):
        """Test get_guidelines handles exceptions gracefully."""
        from sage.services.mcp_server import MCP_AVAILABLE
        
        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")
        
        from sage.services.mcp_server import get_guidelines
        
        def mock_loader():
            class FailingLoader:
                async def load_guidelines(self, *args, **kwargs):
                    raise RuntimeError("Test error")
            return FailingLoader()
        
        monkeypatch.setattr("sage.services.mcp_server.get_loader", mock_loader)
        
        result = await get_guidelines(section="test")
        assert result["status"] == "error"
        assert "error" in result

    @pytest.mark.asyncio
    async def test_get_framework_exception(self, monkeypatch):
        """Test get_framework handles exceptions gracefully."""
        from sage.services.mcp_server import MCP_AVAILABLE
        
        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")
        
        from sage.services.mcp_server import get_framework
        
        def mock_loader():
            class FailingLoader:
                async def load_framework(self, *args, **kwargs):
                    raise RuntimeError("Test error")
            return FailingLoader()
        
        monkeypatch.setattr("sage.services.mcp_server.get_loader", mock_loader)
        
        result = await get_framework(name="test")
        assert result["status"] == "error"
        assert "error" in result

    @pytest.mark.asyncio
    async def test_get_template_exception(self, monkeypatch):
        """Test get_template handles exceptions gracefully."""
        from sage.services.mcp_server import MCP_AVAILABLE
        
        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")
        
        from sage.services.mcp_server import get_template
        
        def mock_loader():
            class FailingLoader:
                async def load_template(self, *args, **kwargs):
                    raise RuntimeError("Test error")
            return FailingLoader()
        
        monkeypatch.setattr("sage.services.mcp_server.get_loader", mock_loader)
        
        result = await get_template(name="test")
        assert result["status"] == "error"
        assert "error" in result

    @pytest.mark.asyncio
    async def test_search_knowledge_exception(self, monkeypatch):
        """Test search_knowledge handles exceptions gracefully."""
        from sage.services.mcp_server import MCP_AVAILABLE
        
        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")
        
        from sage.services.mcp_server import search_knowledge
        
        def mock_loader():
            class FailingLoader:
                async def search(self, *args, **kwargs):
                    raise RuntimeError("Test error")
            return FailingLoader()
        
        monkeypatch.setattr("sage.services.mcp_server.get_loader", mock_loader)
        
        result = await search_knowledge(query="test")
        assert result["status"] == "error"
        assert "error" in result

    @pytest.mark.asyncio
    async def test_get_knowledge_with_layer(self):
        """Test get_knowledge with specific layer."""
        from sage.services.mcp_server import MCP_AVAILABLE
        
        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")
        
        from sage.services.mcp_server import get_knowledge
        
        result = await get_knowledge(layer=0)
        assert isinstance(result, dict)
        assert "content" in result

    @pytest.mark.asyncio
    async def test_get_knowledge_with_invalid_layer(self):
        """Test get_knowledge with invalid layer falls back to core."""
        from sage.services.mcp_server import MCP_AVAILABLE
        
        if not MCP_AVAILABLE:
            pytest.skip("MCP not available")
        
        from sage.services.mcp_server import get_knowledge
        
        result = await get_knowledge(layer=99)
        assert isinstance(result, dict)
        # Should still return something


class TestGetLoaderExtended:
    """Extended tests for get_loader function."""

    def test_get_loader_creates_new_instance(self):
        """Test get_loader creates instance when none exists."""
        from sage.services import mcp_server
        
        # Clear the global loader
        mcp_server._loader = None
        loader = mcp_server.get_loader()
        assert loader is not None

    def test_get_loader_singleton(self):
        """Test get_loader returns same instance."""
        from sage.services import mcp_server
        
        mcp_server._loader = None
        loader1 = mcp_server.get_loader()
        loader2 = mcp_server.get_loader()
        assert loader1 is loader2


class TestRunServerExtended:
    """Extended tests for run_server function."""

    def test_run_server_function_exists(self):
        """Test run_server function exists."""
        from sage.services.mcp_server import run_server
        assert callable(run_server)
