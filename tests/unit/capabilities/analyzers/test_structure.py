"""
Tests for structure checker module.

Tests cover:
- StructureIssue dataclass
- StructureReport dataclass
- StructureChecker class
- check_structure convenience function
"""

from pathlib import Path

from sage.capabilities.analyzers.structure import (
    StructureChecker,
    StructureIssue,
    StructureReport,
    check_structure,
)


class TestStructureIssue:
    """Tests for StructureIssue dataclass."""

    def test_create_issue(self):
        """Test creating a structure issue."""
        issue = StructureIssue(
            severity="error",
            category="missing",
            path="test/path",
            message="Test message",
            suggestion="Test suggestion",
        )
        assert issue.severity == "error"
        assert issue.category == "missing"
        assert issue.path == "test/path"
        assert issue.message == "Test message"
        assert issue.suggestion == "Test suggestion"

    def test_create_issue_without_suggestion(self):
        """Test creating issue without suggestion."""
        issue = StructureIssue(
            severity="warning",
            category="naming",
            path="file.md",
            message="Naming issue",
        )
        assert issue.suggestion == ""

    def test_to_dict(self):
        """Test converting issue to dictionary."""
        issue = StructureIssue(
            severity="info",
            category="content",
            path="doc.md",
            message="Info message",
            suggestion="Do something",
        )
        result = issue.to_dict()
        assert result == {
            "severity": "info",
            "category": "content",
            "path": "doc.md",
            "message": "Info message",
            "suggestion": "Do something",
        }

    def test_to_dict_empty_suggestion(self):
        """Test to_dict with empty suggestion."""
        issue = StructureIssue(
            severity="error",
            category="missing",
            path="file.md",
            message="Missing file",
        )
        result = issue.to_dict()
        assert result["suggestion"] == ""


class TestStructureReport:
    """Tests for StructureReport dataclass."""

    def test_default_values(self):
        """Test default report values."""
        report = StructureReport()
        assert report.valid is True
        assert report.issues == []
        assert report.stats == {}

    def test_error_count_empty(self):
        """Test error count with no issues."""
        report = StructureReport()
        assert report.error_count == 0

    def test_warning_count_empty(self):
        """Test warning count with no issues."""
        report = StructureReport()
        assert report.warning_count == 0

    def test_add_warning_issue(self):
        """Test adding a warning issue."""
        report = StructureReport()
        issue = StructureIssue(
            severity="warning",
            category="naming",
            path="test.md",
            message="Warning",
        )
        report.add_issue(issue)
        assert len(report.issues) == 1
        assert report.valid is True  # Warnings don't invalidate
        assert report.warning_count == 1
        assert report.error_count == 0

    def test_add_error_issue(self):
        """Test adding an error issue invalidates report."""
        report = StructureReport()
        issue = StructureIssue(
            severity="error",
            category="missing",
            path="required.md",
            message="Missing required file",
        )
        report.add_issue(issue)
        assert len(report.issues) == 1
        assert report.valid is False
        assert report.error_count == 1
        assert report.warning_count == 0

    def test_add_multiple_issues(self):
        """Test adding multiple issues of different severities."""
        report = StructureReport()
        report.add_issue(StructureIssue("error", "missing", "a.md", "Error 1"))
        report.add_issue(StructureIssue("warning", "naming", "b.md", "Warning 1"))
        report.add_issue(StructureIssue("error", "missing", "c.md", "Error 2"))
        report.add_issue(StructureIssue("info", "content", "d.md", "Info 1"))
        report.add_issue(StructureIssue("warning", "naming", "e.md", "Warning 2"))

        assert len(report.issues) == 5
        assert report.error_count == 2
        assert report.warning_count == 2
        assert report.valid is False

    def test_to_dict(self):
        """Test converting report to dictionary."""
        report = StructureReport()
        report.stats = {"directories": 5, "files": 10}
        report.add_issue(StructureIssue("error", "missing", "x.md", "Missing"))

        result = report.to_dict()
        assert result["valid"] is False
        assert result["error_count"] == 1
        assert result["warning_count"] == 0
        assert len(result["issues"]) == 1
        assert result["stats"] == {"directories": 5, "files": 10}

    def test_to_dict_empty_report(self):
        """Test to_dict on empty report."""
        report = StructureReport()
        result = report.to_dict()
        assert result == {
            "valid": True,
            "error_count": 0,
            "warning_count": 0,
            "issues": [],
            "stats": {},
        }


class TestStructureChecker:
    """Tests for StructureChecker class."""

    def test_init_default_path(self):
        """Test initialization with default path."""
        checker = StructureChecker()
        assert checker.root_path == Path.cwd()

    def test_init_custom_path(self, tmp_path):
        """Test initialization with custom path."""
        checker = StructureChecker(tmp_path)
        assert checker.root_path == tmp_path

    def test_required_dirs_defined(self):
        """Test REQUIRED_DIRS constant is defined."""
        assert len(StructureChecker.REQUIRED_DIRS) > 0
        assert ".knowledge/core" in StructureChecker.REQUIRED_DIRS

    def test_required_files_defined(self):
        """Test REQUIRED_FILES constant is defined."""
        assert len(StructureChecker.REQUIRED_FILES) > 0
        assert "index.md" in StructureChecker.REQUIRED_FILES

    def test_expected_guidelines_defined(self):
        """Test EXPECTED_GUIDELINES constant is defined."""
        assert len(StructureChecker.EXPECTED_GUIDELINES) > 0

    def test_check_empty_directory(self, tmp_path):
        """Test checking an empty directory reports all missing."""
        checker = StructureChecker(tmp_path)
        report = checker.check()

        assert report.valid is False
        assert report.error_count > 0
        # Should report missing directories and files
        missing_issues = [i for i in report.issues if i.category == "missing"]
        assert len(missing_issues) > 0

    def test_check_directories_missing(self, tmp_path):
        """Test _check_directories reports missing dirs."""
        checker = StructureChecker(tmp_path)
        report = StructureReport()
        checker._check_directories(report)

        # All required dirs should be reported as missing
        assert len(report.issues) == len(StructureChecker.REQUIRED_DIRS)
        for issue in report.issues:
            assert issue.severity == "error"
            assert issue.category == "missing"

    def test_check_directories_exist(self, tmp_path):
        """Test _check_directories passes when dirs exist."""
        # Create all required directories
        for dir_name in StructureChecker.REQUIRED_DIRS:
            (tmp_path / dir_name).mkdir(parents=True)

        checker = StructureChecker(tmp_path)
        report = StructureReport()
        checker._check_directories(report)

        assert len(report.issues) == 0

    def test_check_directories_file_instead_of_dir(self, tmp_path):
        """Test error when file exists instead of directory."""
        # Create parent directory and a file with a directory name
        (tmp_path / "content").mkdir(parents=True)
        (tmp_path / "content" / "core").write_text("not a directory")

        checker = StructureChecker(tmp_path)
        report = StructureReport()
        checker._check_directories(report)

        # Should have error for file instead of directory
        content_issues = [i for i in report.issues if i.category == "content"]
        assert len(content_issues) >= 1

    def test_check_required_files_missing(self, tmp_path):
        """Test _check_required_files reports missing files."""
        checker = StructureChecker(tmp_path)
        report = StructureReport()
        checker._check_required_files(report)

        assert len(report.issues) == len(StructureChecker.REQUIRED_FILES)
        for issue in report.issues:
            assert issue.severity == "error"
            assert issue.category == "missing"

    def test_check_required_files_exist(self, tmp_path):
        """Test _check_required_files passes when files exist."""
        # Create all required files
        for file_path in StructureChecker.REQUIRED_FILES:
            full_path = tmp_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text("")

        checker = StructureChecker(tmp_path)
        report = StructureReport()
        checker._check_required_files(report)

        assert len(report.issues) == 0

    def test_check_guidelines_dir_missing(self, tmp_path):
        """Test _check_guidelines when directory missing."""
        checker = StructureChecker(tmp_path)
        report = StructureReport()
        checker._check_guidelines(report)

        # Should return early without adding issues
        assert len(report.issues) == 0

    def test_check_guidelines_empty_dir(self, tmp_path):
        """Test _check_guidelines with empty guidelines dir."""
        (tmp_path / "content" / "guidelines").mkdir(parents=True)

        checker = StructureChecker(tmp_path)
        report = StructureReport()
        checker._check_guidelines(report)

        # Should report all expected guidelines as missing
        assert len(report.issues) == len(StructureChecker.EXPECTED_GUIDELINES)
        for issue in report.issues:
            assert issue.severity == "warning"

    def test_check_guidelines_partial(self, tmp_path):
        """Test _check_guidelines with some guidelines present."""
        guidelines_dir = tmp_path / "content" / "guidelines"
        guidelines_dir.mkdir(parents=True)
        (guidelines_dir / "quick_start.md").write_text("")
        (guidelines_dir / "planning_design.md").write_text("")

        checker = StructureChecker(tmp_path)
        report = StructureReport()
        checker._check_guidelines(report)

        expected_missing = len(StructureChecker.EXPECTED_GUIDELINES) - 2
        assert len(report.issues) == expected_missing

    def test_check_naming_spaces_in_name(self, tmp_path):
        """Test _check_naming detects spaces in filenames."""
        (tmp_path / "file with spaces.md").write_text("")

        checker = StructureChecker(tmp_path)
        report = StructureReport()
        checker._check_naming(report)

        assert len(report.issues) == 1
        assert report.issues[0].category == "naming"
        assert "spaces" in report.issues[0].message.lower()

    def test_check_naming_uppercase(self, tmp_path):
        """Test _check_naming detects uppercase in filenames."""
        (tmp_path / "MyFile.md").write_text("")

        checker = StructureChecker(tmp_path)
        report = StructureReport()
        checker._check_naming(report)

        assert len(report.issues) == 1
        assert report.issues[0].severity == "info"
        assert "uppercase" in report.issues[0].message.lower()

    def test_check_naming_readme_allowed(self, tmp_path):
        """Test README.md is allowed to have uppercase."""
        (tmp_path / "README.md").write_text("")

        checker = StructureChecker(tmp_path)
        report = StructureReport()
        checker._check_naming(report)

        # README.md should not be flagged
        assert len(report.issues) == 0

    def test_check_naming_skips_archive(self, tmp_path):
        """Test _check_naming skips 08_archive directory."""
        archive_dir = tmp_path / "08_archive"
        archive_dir.mkdir()
        (archive_dir / "File With Spaces.md").write_text("")

        checker = StructureChecker(tmp_path)
        report = StructureReport()
        checker._check_naming(report)

        # Archive files should be skipped
        assert len(report.issues) == 0

    def test_collect_stats_empty(self, tmp_path):
        """Test _collect_stats on empty directory."""
        checker = StructureChecker(tmp_path)
        stats = checker._collect_stats()

        assert stats["directories"] == 0
        assert stats["markdown_files"] == 0
        assert stats["python_files"] == 0
        assert stats["total_files"] == 0

    def test_collect_stats_with_files(self, tmp_path):
        """Test _collect_stats counts files correctly."""
        # Create directories and files
        (tmp_path / "subdir").mkdir()
        (tmp_path / "doc.md").write_text("")
        (tmp_path / "script.py").write_text("")
        (tmp_path / "data.txt").write_text("")
        (tmp_path / "subdir" / "nested.md").write_text("")

        checker = StructureChecker(tmp_path)
        stats = checker._collect_stats()

        assert stats["directories"] == 1
        assert stats["markdown_files"] == 2
        assert stats["python_files"] == 1
        assert stats["total_files"] == 4

    def test_collect_stats_skips_hidden(self, tmp_path):
        """Test _collect_stats skips hidden files/dirs."""
        (tmp_path / ".hidden").mkdir()
        (tmp_path / ".hidden" / "file.md").write_text("")
        (tmp_path / "visible.md").write_text("")

        checker = StructureChecker(tmp_path)
        stats = checker._collect_stats()

        assert stats["markdown_files"] == 1
        assert stats["directories"] == 0

    def test_collect_stats_skips_pycache(self, tmp_path):
        """Test _collect_stats skips __pycache__."""
        (tmp_path / "__pycache__").mkdir()
        (tmp_path / "__pycache__" / "module.pyc").write_text("")
        (tmp_path / "script.py").write_text("")

        checker = StructureChecker(tmp_path)
        stats = checker._collect_stats()

        assert stats["python_files"] == 1
        assert stats["total_files"] == 1

    def test_fix_issues_dry_run(self, tmp_path):
        """Test fix_issues in dry run mode."""
        report = StructureReport()
        report.add_issue(
            StructureIssue(
                severity="error",
                category="missing",
                path="01_core",
                message="Missing directory",
            )
        )

        checker = StructureChecker(tmp_path)
        actions = checker.fix_issues(report, dry_run=True)

        assert len(actions) == 1
        assert "Create directory" in actions[0]
        # Directory should NOT be created in dry run
        assert not (tmp_path / "01_core").exists()

    def test_fix_issues_create_directory(self, tmp_path):
        """Test fix_issues creates missing directory."""
        report = StructureReport()
        report.add_issue(
            StructureIssue(
                severity="error",
                category="missing",
                path="01_core",
                message="Missing directory",
            )
        )

        checker = StructureChecker(tmp_path)
        actions = checker.fix_issues(report, dry_run=False)

        assert len(actions) == 1
        assert (tmp_path / "01_core").exists()
        assert (tmp_path / "01_core").is_dir()

    def test_fix_issues_create_file(self, tmp_path):
        """Test fix_issues creates missing file."""
        report = StructureReport()
        report.add_issue(
            StructureIssue(
                severity="error",
                category="missing",
                path="01_core/principles.md",
                message="Missing file",
            )
        )

        checker = StructureChecker(tmp_path)
        actions = checker.fix_issues(report, dry_run=False)

        assert len(actions) == 1
        assert (tmp_path / "01_core" / "principles.md").exists()

    def test_fix_issues_skips_warnings(self, tmp_path):
        """Test fix_issues only fixes error-level issues."""
        report = StructureReport()
        report.add_issue(
            StructureIssue(
                severity="warning",
                category="missing",
                path="optional.md",
                message="Missing optional file",
            )
        )

        checker = StructureChecker(tmp_path)
        actions = checker.fix_issues(report, dry_run=False)

        assert len(actions) == 0

    def test_fix_issues_skips_non_missing(self, tmp_path):
        """Test fix_issues only fixes missing category."""
        report = StructureReport()
        report.add_issue(
            StructureIssue(
                severity="error",
                category="naming",
                path="BadName.md",
                message="Bad naming",
            )
        )

        checker = StructureChecker(tmp_path)
        actions = checker.fix_issues(report, dry_run=False)

        assert len(actions) == 0

    def test_check_full_valid_structure(self, tmp_path):
        """Test check() on fully valid structure."""
        # Create all required directories
        for dir_name in StructureChecker.REQUIRED_DIRS:
            (tmp_path / dir_name).mkdir(parents=True)

        # Create all required files
        for file_path in StructureChecker.REQUIRED_FILES:
            full_path = tmp_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text("")

        # Create all guidelines
        guidelines_dir = tmp_path / "content" / "guidelines"
        guidelines_dir.mkdir(parents=True, exist_ok=True)
        for guideline in StructureChecker.EXPECTED_GUIDELINES:
            (guidelines_dir / guideline).write_text("")

        checker = StructureChecker(tmp_path)
        report = checker.check()

        assert report.valid is True
        assert report.error_count == 0
        assert report.stats["directories"] > 0


class TestCheckStructureFunction:
    """Tests for check_structure convenience function."""

    def test_check_structure_default(self):
        """Test check_structure uses current directory."""
        report = check_structure()
        assert isinstance(report, StructureReport)

    def test_check_structure_with_path(self, tmp_path):
        """Test check_structure with custom path."""
        report = check_structure(tmp_path)
        assert isinstance(report, StructureReport)
        # Empty tmp_path should have errors
        assert report.error_count > 0
