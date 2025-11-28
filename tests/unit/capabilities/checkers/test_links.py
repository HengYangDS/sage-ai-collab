"""Tests for LinkChecker.

Version: 0.1.0
"""

import pytest
from pathlib import Path

from sage.capabilities.checkers.links import (
    LinkChecker,
    LinkType,
    LinkStatus,
    LinkResult,
    LinkReport,
    check_links,
)


class TestLinkType:
    """Tests for LinkType enum."""

    def test_link_types_exist(self):
        """Test that all link types exist."""
        assert LinkType.INTERNAL is not None
        assert LinkType.EXTERNAL is not None
        assert LinkType.ANCHOR is not None
        assert LinkType.IMAGE is not None
        assert LinkType.UNKNOWN is not None


class TestLinkStatus:
    """Tests for LinkStatus enum."""

    def test_link_statuses_exist(self):
        """Test that all link statuses exist."""
        assert LinkStatus.VALID is not None
        assert LinkStatus.BROKEN is not None
        assert LinkStatus.WARNING is not None
        assert LinkStatus.SKIPPED is not None
        assert LinkStatus.ERROR is not None


class TestLinkResult:
    """Tests for LinkResult dataclass."""

    def test_link_result_creation(self):
        """Test creating a LinkResult."""
        result = LinkResult(
            source_file="test.md",
            line_number=10,
            link_text="Other Document",
            link_target="./other.md",
            link_type=LinkType.INTERNAL,
            status=LinkStatus.VALID,
        )
        assert result.source_file == "test.md"
        assert result.line_number == 10
        assert result.link_target == "./other.md"
        assert result.link_type == LinkType.INTERNAL
        assert result.status == LinkStatus.VALID

    def test_to_dict(self):
        """Test conversion to dictionary."""
        result = LinkResult(
            source_file="test.md",
            line_number=10,
            link_text="Other Document",
            link_target="./other.md",
            link_type=LinkType.INTERNAL,
            status=LinkStatus.VALID,
        )
        d = result.to_dict()
        assert isinstance(d, dict)
        assert d["source_file"] == "test.md"
        assert d["link_type"] == "internal"
        assert d["status"] == "valid"


class TestLinkReport:
    """Tests for LinkReport dataclass."""

    def test_link_report_creation(self):
        """Test creating a LinkReport."""
        results = [
            LinkResult("a.md", 1, "B", "b.md", LinkType.INTERNAL, LinkStatus.VALID),
            LinkResult("a.md", 2, "C", "c.md", LinkType.INTERNAL, LinkStatus.BROKEN),
        ]
        report = LinkReport(
            total_links=2,
            valid_count=1,
            broken_count=1,
            warning_count=0,
            skipped_count=0,
            results=results,
            files_checked=1,
            duration_ms=10.5,
        )
        assert report.total_links == 2
        assert report.valid_count == 1
        assert report.broken_count == 1

    def test_broken_rate(self):
        """Test broken link rate calculation (returns percentage)."""
        report = LinkReport(
            total_links=10,
            valid_count=7,
            broken_count=3,
            warning_count=0,
            skipped_count=0,
            results=[],
            files_checked=1,
            duration_ms=10.0,
        )
        # broken_rate returns percentage (0-100)
        assert report.broken_rate == pytest.approx(30.0, rel=0.01)

    def test_broken_rate_zero_links(self):
        """Test broken rate with no links."""
        report = LinkReport(
            total_links=0,
            valid_count=0,
            broken_count=0,
            warning_count=0,
            skipped_count=0,
            results=[],
            files_checked=0,
            duration_ms=0.0,
        )
        assert report.broken_rate == 0.0

    def test_to_dict(self):
        """Test conversion to dictionary."""
        report = LinkReport(
            total_links=5,
            valid_count=4,
            broken_count=1,
            warning_count=0,
            skipped_count=0,
            results=[],
            files_checked=2,
            duration_ms=15.5,
        )
        d = report.to_dict()
        assert isinstance(d, dict)
        assert d["total_links"] == 5
        assert "broken_rate" in d
        assert "files_checked" in d


class TestLinkChecker:
    """Tests for LinkChecker class."""

    @pytest.fixture
    def checker(self, tmp_path):
        """Create LinkChecker instance with temp path."""
        return LinkChecker(kb_path=tmp_path, check_external=False)

    def test_init(self, checker):
        """Test checker initialization."""
        assert checker is not None

    def test_classify_internal_link(self, checker):
        """Test classification of internal links."""
        link_type = checker._classify_link("./other.md")
        assert link_type == LinkType.INTERNAL

    def test_classify_external_link(self, checker):
        """Test classification of external links."""
        link_type = checker._classify_link("https://example.com")
        assert link_type == LinkType.EXTERNAL

    def test_classify_anchor_link(self, checker):
        """Test classification of anchor links."""
        link_type = checker._classify_link("#section-1")
        assert link_type == LinkType.ANCHOR

    def test_check_file_with_valid_links(self, checker, tmp_path):
        """Test checking a file with valid internal links."""
        # Create target file
        (tmp_path / "target.md").write_text("# Target\n\nContent.")

        # Create source file with link to target
        source = tmp_path / "source.md"
        source.write_text("# Source\n\nSee [Target](target.md).\n")

        results = checker.check_file(source)
        assert isinstance(results, list)
        assert len(results) >= 1

    def test_check_file_with_broken_link(self, checker, tmp_path):
        """Test checking a file with broken links."""
        source = tmp_path / "source.md"
        source.write_text("# Source\n\nSee [Missing](nonexistent.md).\n")

        results = checker.check_file(source)
        broken = [r for r in results if r.status == LinkStatus.BROKEN]
        assert len(broken) >= 1

    def test_check_file_with_anchor(self, checker, tmp_path):
        """Test checking a file with anchor links."""
        source = tmp_path / "source.md"
        source.write_text("# Title\n\n## Section\n\nSee [Section](#section).\n")

        results = checker.check_file(source)
        assert isinstance(results, list)

    def test_check_file_not_found(self, checker, tmp_path):
        """Test checking non-existent file."""
        fake_path = tmp_path / "nonexistent.md"
        results = checker.check_file(fake_path)
        assert isinstance(results, list)

    def test_check_all(self, checker, tmp_path):
        """Test checking all files in directory."""
        (tmp_path / "file1.md").write_text("# File 1\n\n[Link](file2.md)")
        (tmp_path / "file2.md").write_text("# File 2\n\nContent.")

        report = checker.check_all()
        assert isinstance(report, LinkReport)
        assert report.total_links >= 1

    def test_get_broken_links(self, checker, tmp_path):
        """Test getting only broken links."""
        (tmp_path / "source.md").write_text("# Source\n\n[Broken](missing.md)")

        checker.check_all()
        broken = checker.get_broken_links()
        assert isinstance(broken, list)

    def test_clear_cache(self, checker, tmp_path):
        """Test clearing the cache."""
        (tmp_path / "file.md").write_text("# Test\n\nContent.")
        checker.check_all()
        checker.clear_cache()
        # Should not raise an error
        assert True

    def test_normalize_anchor(self, checker):
        """Test anchor normalization."""
        normalized = checker._normalize_anchor("Hello World!")
        assert isinstance(normalized, str)
        # Normalized anchor should be lowercase with hyphens
        assert normalized == normalized.lower()


class TestCheckLinksFunction:
    """Tests for standalone check_links function."""

    def test_check_links_function(self, tmp_path):
        """Test the standalone function."""
        (tmp_path / "test.md").write_text("# Test\n\n[Link](#test)")
        report = check_links(tmp_path)
        assert report is not None
        assert isinstance(report, LinkReport)
