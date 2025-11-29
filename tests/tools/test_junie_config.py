"""
Junie Configuration Validation Tests

Tests for validating .junie/ configuration files:
- mcp.json syntax and schema compliance
- YAML configuration file syntax
- Schema file validity

Run with: pytest tests/tools/test_junie_config.py -v
"""

import json
from pathlib import Path

import pytest
import yaml

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
JUNIE_DIR = PROJECT_ROOT / ".junie"


class TestMcpConfiguration:
    """Tests for MCP configuration files."""

    def test_mcp_json_exists(self) -> None:
        """Verify mcp.json exists."""
        mcp_json = JUNIE_DIR / "mcp" / "mcp.json"
        assert mcp_json.exists(), f"mcp.json not found at {mcp_json}"

    def test_mcp_json_valid_syntax(self) -> None:
        """Verify mcp.json has valid JSON syntax."""
        mcp_json = JUNIE_DIR / "mcp" / "mcp.json"
        with open(mcp_json, encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, dict), "mcp.json should be a JSON object"

    def test_mcp_json_has_servers(self) -> None:
        """Verify mcp.json contains mcpServers key."""
        mcp_json = JUNIE_DIR / "mcp" / "mcp.json"
        with open(mcp_json, encoding="utf-8") as f:
            data = json.load(f)
        assert "mcpServers" in data, "mcp.json should contain 'mcpServers' key"

    def test_mcp_servers_have_required_fields(self) -> None:
        """Verify each MCP server has required fields."""
        mcp_json = JUNIE_DIR / "mcp" / "mcp.json"
        with open(mcp_json, encoding="utf-8") as f:
            data = json.load(f)

        servers = data.get("mcpServers", {})
        for server_name, server_config in servers.items():
            assert (
                "command" in server_config
            ), f"Server '{server_name}' missing 'command'"
            assert "args" in server_config, f"Server '{server_name}' missing 'args'"
            assert isinstance(
                server_config["args"], list
            ), f"Server '{server_name}' args should be a list"

    def test_mcp_servers_have_metadata(self) -> None:
        """Verify each MCP server has _meta with description and priority."""
        mcp_json = JUNIE_DIR / "mcp" / "mcp.json"
        with open(mcp_json, encoding="utf-8") as f:
            data = json.load(f)

        servers = data.get("mcpServers", {})
        for server_name, server_config in servers.items():
            meta = server_config.get("_meta", {})
            assert (
                "description" in meta
            ), f"Server '{server_name}' missing '_meta.description'"
            assert (
                "priority" in meta
            ), f"Server '{server_name}' missing '_meta.priority'"
            assert meta["priority"] in [
                "P0",
                "P1",
                "P2",
                "P3",
            ], f"Server '{server_name}' has invalid priority"

    def test_mcp_schema_exists(self) -> None:
        """Verify mcp.schema.json exists."""
        schema_file = JUNIE_DIR / "mcp" / "mcp.schema.json"
        assert schema_file.exists(), f"mcp.schema.json not found at {schema_file}"

    def test_mcp_schema_valid_syntax(self) -> None:
        """Verify mcp.schema.json has valid JSON syntax."""
        schema_file = JUNIE_DIR / "mcp" / "mcp.schema.json"
        with open(schema_file, encoding="utf-8") as f:
            schema = json.load(f)
        assert "$schema" in schema, "Schema file should have $schema property"


class TestYamlConfiguration:
    """Tests for YAML configuration files."""

    def test_generic_config_exists(self) -> None:
        """Verify generic/config.yaml exists."""
        config_file = JUNIE_DIR / "generic" / "config.yaml"
        assert config_file.exists(), f"config.yaml not found at {config_file}"

    def test_generic_config_valid_syntax(self) -> None:
        """Verify generic/config.yaml has valid YAML syntax."""
        config_file = JUNIE_DIR / "generic" / "config.yaml"
        with open(config_file, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        assert isinstance(data, dict), "config.yaml should be a YAML mapping"

    def test_generic_config_has_schema_version(self) -> None:
        """Verify generic/config.yaml has schema_version."""
        config_file = JUNIE_DIR / "generic" / "config.yaml"
        with open(config_file, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        assert "schema_version" in data, "config.yaml should have schema_version"

    def test_project_config_exists(self) -> None:
        """Verify project/config.yaml exists."""
        config_file = JUNIE_DIR / "project" / "config.yaml"
        assert config_file.exists(), f"project/config.yaml not found at {config_file}"

    def test_project_config_valid_syntax(self) -> None:
        """Verify project/config.yaml has valid YAML syntax."""
        config_file = JUNIE_DIR / "project" / "config.yaml"
        with open(config_file, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        assert isinstance(data, dict), "project/config.yaml should be a YAML mapping"

    def test_project_config_has_schema_version(self) -> None:
        """Verify project/config.yaml has schema_version."""
        config_file = JUNIE_DIR / "project" / "config.yaml"
        with open(config_file, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        assert (
            "schema_version" in data
        ), "project/config.yaml should have schema_version"

    def test_config_schema_exists(self) -> None:
        """Verify config.schema.json exists."""
        schema_file = JUNIE_DIR / "generic" / "config.schema.json"
        assert schema_file.exists(), f"config.schema.json not found at {schema_file}"

    def test_schema_versions_synchronized(self) -> None:
        """Verify schema_version is synchronized across config files."""
        generic_config = JUNIE_DIR / "generic" / "config.yaml"
        project_config = JUNIE_DIR / "project" / "config.yaml"

        with open(generic_config, encoding="utf-8") as f:
            generic_data = yaml.safe_load(f)
        with open(project_config, encoding="utf-8") as f:
            project_data = yaml.safe_load(f)

        generic_version = generic_data.get("schema_version")
        project_version = project_data.get("schema_version")

        assert (
            generic_version == project_version
        ), f"Schema versions mismatch: generic={generic_version}, project={project_version}"

    def test_schema_version_format_valid(self) -> None:
        """Verify schema_version matches expected format (MAJOR.MINOR or MAJOR.MINOR.PATCH)."""
        import re

        version_pattern = re.compile(r"^\d+\.\d+(\.\d+)?$")

        generic_config = JUNIE_DIR / "generic" / "config.yaml"
        with open(generic_config, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        schema_version = data.get("schema_version", "")
        assert version_pattern.match(
            schema_version
        ), f"Invalid schema_version format: {schema_version}"

    def test_context_loading_paths_format(self) -> None:
        """Verify context_loading paths are properly formatted (no dangerous patterns)."""
        config_file = JUNIE_DIR / "generic" / "config.yaml"
        with open(config_file, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        context_loading = data.get("context_loading", {})

        def is_valid_path(path: str) -> bool:
            """Check if path is valid (relative from project root or hidden dir)."""
            # Valid: starts with . (hidden/relative), /, or alphanumeric (project-relative)
            # Invalid: contains .., starts with ~, or contains dangerous chars
            if ".." in path:
                return False
            if path.startswith("~"):
                return False
            if any(c in path for c in ["<", ">", "|", "*", "?"]):
                return False
            return True

        # Check priority paths format
        priority_paths = context_loading.get("priority", [])
        for path in priority_paths:
            assert is_valid_path(path), f"Invalid priority path format: {path}"

        # Check lazy_load paths format
        lazy_load_paths = context_loading.get("lazy_load", [])
        for path in lazy_load_paths:
            assert is_valid_path(path), f"Invalid lazy_load path format: {path}"

        # Check exclude paths format
        exclude_paths = context_loading.get("exclude", [])
        for path in exclude_paths:
            assert is_valid_path(path), f"Invalid exclude path format: {path}"


class TestGuidelinesAndDocs:
    """Tests for guidelines and documentation files."""

    def test_guidelines_exists(self) -> None:
        """Verify guidelines.md exists."""
        guidelines = JUNIE_DIR / "guidelines.md"
        assert guidelines.exists(), f"guidelines.md not found at {guidelines}"

    def test_readme_exists(self) -> None:
        """Verify README.md exists."""
        readme = JUNIE_DIR / "README.md"
        assert readme.exists(), f"README.md not found at {readme}"

    def test_quickref_files_exist(self) -> None:
        """Verify quickref.md files exist in generic and project directories."""
        generic_quickref = JUNIE_DIR / "generic" / "quickref.md"
        project_quickref = JUNIE_DIR / "project" / "quickref.md"
        assert generic_quickref.exists(), "generic/quickref.md not found"
        assert project_quickref.exists(), "project/quickref.md not found"


class TestDirectoryStructure:
    """Tests for .junie directory structure."""

    def test_required_directories_exist(self) -> None:
        """Verify required subdirectories exist."""
        required_dirs = ["generic", "project", "docs", "mcp"]
        for dir_name in required_dirs:
            dir_path = JUNIE_DIR / dir_name
            assert dir_path.is_dir(), f"Directory '{dir_name}' not found in .junie/"

    def test_docs_structure_exist(self) -> None:
        """Verify documentation directory structure exists."""
        docs_dir = JUNIE_DIR / "docs"
        
        # Check main README
        assert (docs_dir / "README.md").exists(), "docs/README.md not found"
        
        # Check subdirectories exist
        expected_subdirs = ["guides", "mcp", "operations", "reference", "vision"]
        for subdir in expected_subdirs:
            subdir_path = docs_dir / subdir
            assert subdir_path.is_dir(), f"docs/{subdir}/ directory not found"

    def test_docs_guides_exist(self) -> None:
        """Verify guides documentation files exist."""
        guides_dir = JUNIE_DIR / "docs" / "guides"
        expected_files = ["quick-start.md", "action-allowlist.md"]
        for filename in expected_files:
            file_path = guides_dir / filename
            assert file_path.exists(), f"guides/{filename} not found"

    def test_docs_mcp_exist(self) -> None:
        """Verify MCP documentation files exist."""
        mcp_dir = JUNIE_DIR / "docs" / "mcp"
        expected_files = ["overview.md", "configuration.md", "servers.md", "memory.md", "troubleshooting.md"]
        for filename in expected_files:
            file_path = mcp_dir / filename
            assert file_path.exists(), f"mcp/{filename} not found"

    def test_docs_operations_exist(self) -> None:
        """Verify operations documentation files exist."""
        ops_dir = JUNIE_DIR / "docs" / "operations"
        expected_files = ["maintenance.md", "migration.md", "metrics.md", "recovery.md"]
        for filename in expected_files:
            file_path = ops_dir / filename
            assert file_path.exists(), f"operations/{filename} not found"

    def test_docs_reference_exist(self) -> None:
        """Verify reference documentation files exist."""
        ref_dir = JUNIE_DIR / "docs" / "reference"
        expected_files = ["glossary.md", "regex.md", "rules-windows.md", "rules-unix.md"]
        for filename in expected_files:
            file_path = ref_dir / filename
            assert file_path.exists(), f"reference/{filename} not found"

    def test_docs_vision_exist(self) -> None:
        """Verify vision documentation files exist."""
        vision_dir = JUNIE_DIR / "docs" / "vision"
        expected_files = ["future-protocols.md"]
        for filename in expected_files:
            file_path = vision_dir / filename
            assert file_path.exists(), f"vision/{filename} not found"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
