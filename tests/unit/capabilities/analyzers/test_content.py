"""Tests for ContentAnalyzer.

Version: 0.1.0
"""

import pytest
from pathlib import Path

from sage.capabilities.analyzers.content import (
    ContentAnalyzer,
    ContentMetrics,
    analyze_content,
)


class TestContentMetrics:
    """Tests for ContentMetrics dataclass."""

    def test_default_values(self):
        """Test default field values."""
        metrics = ContentMetrics()
        assert metrics.total_lines == 0
        assert metrics.total_chars == 0
        assert metrics.estimated_tokens == 0
        assert metrics.header_count == 0
        assert metrics.code_block_count == 0
        assert metrics.table_count == 0
        assert metrics.file_path == ""
        assert metrics.sections == []

    def test_efficiency_score_zero_tokens(self):
        """Test efficiency score with zero tokens per section."""
        metrics = ContentMetrics(tokens_per_section=0)
        assert metrics.efficiency_score == 100

    def test_efficiency_score_calculation(self):
        """Test efficiency score calculation."""
        metrics = ContentMetrics(tokens_per_section=100)
        score = metrics.efficiency_score
        assert 0 <= score <= 100
        assert isinstance(score, int)

    def test_to_dict(self):
        """Test conversion to dictionary."""
        metrics = ContentMetrics(
            file_path="test.md",
            total_lines=100,
            total_chars=500,
            estimated_tokens=125,
            header_count=5,
            code_block_count=2,
        )
        result = metrics.to_dict()
        assert isinstance(result, dict)
        assert result["file_path"] == "test.md"
        assert "basic" in result
        assert result["basic"]["lines"] == 100
        assert "structure" in result
        assert result["structure"]["headers"] == 5
        assert "efficiency" in result


class TestContentAnalyzer:
    """Tests for ContentAnalyzer class."""

    @pytest.fixture
    def analyzer(self):
        """Create ContentAnalyzer instance."""
        return ContentAnalyzer()

    def test_init(self, analyzer):
        """Test analyzer initialization."""
        assert analyzer is not None

    def test_analyze_content_basic(self, analyzer):
        """Test basic content analysis."""
        content = """# Test Document

This is a test paragraph.

## Section 1

Some content here.

```python
def hello():
    pass
```

| Col1 | Col2 |
|------|------|
| A    | B    |
"""
        metrics = analyzer.analyze_content(content, "test.md")
        assert isinstance(metrics, ContentMetrics)
        assert metrics.total_lines > 0
        assert metrics.header_count >= 2
        assert metrics.code_block_count >= 1
        assert metrics.table_count >= 1

    def test_analyze_content_empty(self, analyzer):
        """Test analysis of empty content."""
        metrics = analyzer.analyze_content("", "empty.md")
        assert metrics.total_lines == 0 or metrics.total_lines == 1
        assert metrics.total_chars == 0

    def test_estimate_tokens(self, analyzer):
        """Test token estimation."""
        text = "Hello world, this is a test."
        tokens = analyzer.estimate_tokens(text)
        assert isinstance(tokens, int)
        assert tokens > 0

    def test_estimate_tokens_empty(self, analyzer):
        """Test token estimation for empty text."""
        tokens = analyzer.estimate_tokens("")
        assert tokens == 0

    def test_suggest_optimizations(self, analyzer):
        """Test optimization suggestions."""
        metrics = ContentMetrics(
            file_path="test.md",
            total_lines=100,
            tokens_per_section=500,
        )
        suggestions = analyzer.suggest_optimizations(metrics)
        assert isinstance(suggestions, list)

    def test_get_summary(self, analyzer):
        """Test summary generation."""
        metrics_list = [
            ContentMetrics(
                file_path="file1.md",
                total_lines=100,
                estimated_tokens=500,
            ),
            ContentMetrics(
                file_path="file2.md",
                total_lines=50,
                estimated_tokens=250,
            ),
        ]
        summary = analyzer.get_summary(metrics_list)
        assert isinstance(summary, dict)
        assert "file_count" in summary
        assert summary["file_count"] == 2

    def test_analyze_file_not_found(self, analyzer, tmp_path):
        """Test analysis of non-existent file returns empty metrics."""
        fake_path = tmp_path / "nonexistent.md"
        result = analyzer.analyze_file(fake_path)
        # Returns ContentMetrics with file_path set, not None
        assert isinstance(result, ContentMetrics)
        assert result.file_path == str(fake_path)

    def test_analyze_file_success(self, analyzer, tmp_path):
        """Test successful file analysis."""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test\n\nContent here.")
        metrics = analyzer.analyze_file(test_file)
        assert metrics is not None
        assert metrics.total_lines == 3

    def test_analyze_directory(self, analyzer, tmp_path):
        """Test directory analysis."""
        (tmp_path / "file1.md").write_text("# File 1\n\nContent.")
        (tmp_path / "file2.md").write_text("# File 2\n\nMore content.")
        (tmp_path / "other.txt").write_text("Not markdown")

        results = analyzer.analyze_directory(tmp_path, extensions=[".md"])
        assert len(results) == 2


class TestAnalyzeContentFunction:
    """Tests for standalone analyze_content function."""

    def test_analyze_content_function(self, tmp_path):
        """Test the standalone function."""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test\n\nContent.")
        result = analyze_content(test_file)
        assert result is not None
        assert isinstance(result, ContentMetrics)
