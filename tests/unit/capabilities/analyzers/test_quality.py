"""Tests for QualityAnalyzer.

Version: 0.1.0
"""

import pytest
from pathlib import Path

from sage.capabilities.analyzers.quality import (
    QualityAnalyzer,
    QualityScore,
    analyze_quality,
)


class TestQualityScore:
    """Tests for QualityScore dataclass."""

    def test_default_values(self):
        """Test default field values."""
        score = QualityScore()
        assert score.correctness == 0
        assert score.completeness == 0
        assert score.clarity == 0
        assert score.efficiency == 0
        assert score.testability == 0
        assert score.file_path == ""
        assert score.issues == []
        assert score.suggestions == []

    def test_overall_score_calculation(self):
        """Test overall score calculation."""
        score = QualityScore(
            correctness=80,
            completeness=90,
            clarity=70,
            efficiency=85,
            testability=75,
        )
        overall = score.overall
        assert isinstance(overall, float)
        assert 0.0 <= overall <= 100.0

    def test_grade_a(self):
        """Test A grade for high scores."""
        score = QualityScore(
            correctness=95,
            completeness=95,
            clarity=95,
            efficiency=95,
            testability=95,
        )
        assert score.grade == "A"

    def test_grade_b(self):
        """Test B grade for good scores."""
        score = QualityScore(
            correctness=85,
            completeness=85,
            clarity=85,
            efficiency=85,
            testability=85,
        )
        assert score.grade == "B"

    def test_grade_c(self):
        """Test C grade for average scores."""
        score = QualityScore(
            correctness=75,
            completeness=75,
            clarity=75,
            efficiency=75,
            testability=75,
        )
        assert score.grade == "C"

    def test_grade_d(self):
        """Test D grade for below average scores."""
        score = QualityScore(
            correctness=65,
            completeness=65,
            clarity=65,
            efficiency=65,
            testability=65,
        )
        assert score.grade == "D"

    def test_grade_f(self):
        """Test F grade for low scores."""
        score = QualityScore(
            correctness=30,
            completeness=30,
            clarity=30,
            efficiency=30,
            testability=30,
        )
        assert score.grade == "F"

    def test_to_dict(self):
        """Test conversion to dictionary."""
        score = QualityScore(
            file_path="test.py",
            correctness=80,
            completeness=90,
            clarity=70,
            efficiency=85,
            testability=75,
        )
        result = score.to_dict()
        assert isinstance(result, dict)
        assert result["file_path"] == "test.py"
        assert "scores" in result
        assert result["scores"]["correctness"] == 80
        assert "overall" in result
        assert "grade" in result


class TestQualityAnalyzer:
    """Tests for QualityAnalyzer class."""

    @pytest.fixture
    def analyzer(self):
        """Create QualityAnalyzer instance."""
        return QualityAnalyzer()

    def test_init(self, analyzer):
        """Test analyzer initialization."""
        assert analyzer is not None

    def test_analyze_python_file(self, analyzer, tmp_path):
        """Test Python file analysis."""
        py_file = tmp_path / "test.py"
        py_file.write_text(
            '''"""Module docstring."""

def hello(name: str) -> str:
    """Say hello.
    
    Args:
        name: The name to greet.
        
    Returns:
        Greeting string.
    """
    return f"Hello, {name}!"


class MyClass:
    """A sample class."""
    
    def __init__(self):
        """Initialize."""
        self.value = 0
'''
        )
        result = analyzer.analyze_file(py_file)
        assert result is not None
        assert isinstance(result, QualityScore)
        assert result.file_path == str(py_file)
        assert result.analysis_type == "code"

    def test_analyze_markdown_file(self, analyzer, tmp_path):
        """Test Markdown file analysis."""
        md_file = tmp_path / "test.md"
        md_file.write_text(
            """# Title

## Introduction

This is a well-structured document.

## Section 1

Content here with proper formatting.

## Conclusion

Final thoughts.
"""
        )
        result = analyzer.analyze_file(md_file)
        assert result is not None
        assert isinstance(result, QualityScore)
        assert result.analysis_type == "documentation"

    def test_analyze_file_not_found(self, analyzer, tmp_path):
        """Test analysis of non-existent file."""
        fake_path = tmp_path / "nonexistent.py"
        result = analyzer.analyze_file(fake_path)
        # Returns QualityScore with issue, not None
        assert isinstance(result, QualityScore)
        assert "File not found" in result.issues

    def test_analyze_unsupported_extension(self, analyzer, tmp_path):
        """Test analysis of unsupported file type."""
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("Plain text content")
        result = analyzer.analyze_file(txt_file)
        assert isinstance(result, QualityScore)
        assert any("Unsupported" in issue for issue in result.issues)

    def test_analyze_directory(self, analyzer, tmp_path):
        """Test directory analysis."""
        (tmp_path / "file1.py").write_text('"""Doc."""\ndef foo(): pass')
        (tmp_path / "file2.py").write_text('"""Doc."""\ndef bar(): pass')
        (tmp_path / "readme.md").write_text("# README\n\nContent.")

        results = analyzer.analyze_directory(tmp_path, extensions=[".py"])
        assert len(results) == 2
        assert all(isinstance(r, QualityScore) for r in results)

    def test_analyze_empty_python(self, analyzer, tmp_path):
        """Test analysis of empty Python file."""
        py_file = tmp_path / "empty.py"
        py_file.write_text("")
        result = analyzer.analyze_file(py_file)
        assert isinstance(result, QualityScore)

    def test_analyze_python_without_docstrings(self, analyzer, tmp_path):
        """Test Python file without docstrings."""
        py_file = tmp_path / "no_docs.py"
        py_file.write_text(
            """
def foo():
    pass

def bar():
    return 1
"""
        )
        result = analyzer.analyze_file(py_file)
        assert isinstance(result, QualityScore)
        # Should have lower completeness score or issues
        assert result.completeness < 100 or len(result.issues) > 0


class TestAnalyzeQualityFunction:
    """Tests for standalone analyze_quality function."""

    def test_analyze_quality_function(self, tmp_path):
        """Test the standalone function."""
        test_file = tmp_path / "test.py"
        test_file.write_text('"""Module."""\ndef test(): pass')
        result = analyze_quality(test_file)
        assert result is not None
        assert isinstance(result, QualityScore)
