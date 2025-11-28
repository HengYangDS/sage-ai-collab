"""
Quality Analyzer - Code and documentation quality scoring.

This module provides:
- QualityScore: Structured quality score with multiple dimensions
- QualityAnalyzer: Analyzer for code and documentation quality

Author: AI Collaboration KB Team
Version: 2.0.0
"""

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class QualityScore:
    """Structured quality score with multiple dimensions."""

    # Core dimensions (0-100)
    correctness: int = 0
    completeness: int = 0
    clarity: int = 0
    efficiency: int = 0
    testability: int = 0

    # Metadata
    file_path: str = ""
    analysis_type: str = ""  # "code" or "documentation"
    issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)

    @property
    def overall(self) -> float:
        """Calculate overall weighted score."""
        weights = {
            "correctness": 0.25,
            "completeness": 0.20,
            "clarity": 0.25,
            "efficiency": 0.15,
            "testability": 0.15,
        }
        total = sum(getattr(self, dim) * weight for dim, weight in weights.items())
        return round(total, 2)

    @property
    def grade(self) -> str:
        """Get letter grade based on overall score."""
        score = self.overall
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "file_path": self.file_path,
            "analysis_type": self.analysis_type,
            "scores": {
                "correctness": self.correctness,
                "completeness": self.completeness,
                "clarity": self.clarity,
                "efficiency": self.efficiency,
                "testability": self.testability,
            },
            "overall": self.overall,
            "grade": self.grade,
            "issues": self.issues,
            "suggestions": self.suggestions,
        }


class QualityAnalyzer:
    """
    Analyzer for code and documentation quality.

    Features:
    - Multi-dimensional quality scoring
    - Code pattern detection
    - Documentation completeness checking
    - Issue identification and suggestions
    """

    def __init__(self):
        """Initialize the quality analyzer."""
        self._code_patterns = self._load_code_patterns()
        self._doc_patterns = self._load_doc_patterns()

    def analyze_file(self, file_path: Path) -> QualityScore:
        """
        Analyze a single file for quality.

        Args:
            file_path: Path to the file to analyze

        Returns:
            QualityScore with analysis results
        """
        if not file_path.exists():
            return QualityScore(file_path=str(file_path), issues=["File not found"])

        content = file_path.read_text(encoding="utf-8")

        if file_path.suffix == ".py":
            return self._analyze_python(file_path, content)
        elif file_path.suffix == ".md":
            return self._analyze_markdown(file_path, content)
        else:
            return QualityScore(
                file_path=str(file_path),
                issues=[f"Unsupported file type: {file_path.suffix}"],
            )

    def analyze_directory(
        self, dir_path: Path, extensions: list[str] | None = None
    ) -> list[QualityScore]:
        """
        Analyze all files in a directory.

        Args:
            dir_path: Path to directory
            extensions: File extensions to analyze (default: .py, .md)

        Returns:
            List of QualityScore for each analyzed file
        """
        extensions = extensions or [".py", ".md"]
        results = []

        for ext in extensions:
            for file_path in dir_path.rglob(f"*{ext}"):
                # Skip cache and hidden directories
                if "__pycache__" in str(file_path) or "/.git/" in str(file_path):
                    continue
                try:
                    score = self.analyze_file(file_path)
                    results.append(score)
                except Exception as e:
                    logger.error(f"Error analyzing {file_path}: {e}")

        return results

    def _analyze_python(self, file_path: Path, content: str) -> QualityScore:
        """Analyze Python file for quality."""
        issues = []
        suggestions = []

        lines = content.split("\n")
        total_lines = len(lines)

        # Correctness checks
        correctness = 100

        # Check for syntax patterns that might indicate issues
        if "except:" in content and "except Exception" not in content:
            issues.append("Bare except clause found")
            correctness -= 10

        if "import *" in content:
            issues.append("Wildcard import found")
            correctness -= 5

        # Completeness checks
        completeness = 100

        # Check for docstrings
        has_module_docstring = content.strip().startswith(
            '"""'
        ) or content.strip().startswith("'''")
        if not has_module_docstring:
            issues.append("Missing module docstring")
            completeness -= 15

        # Check for type hints
        func_pattern = r"def \w+\([^)]*\):"
        typed_func_pattern = r"def \w+\([^)]*\)\s*->\s*\w+"
        funcs = len(re.findall(func_pattern, content))
        typed_funcs = len(re.findall(typed_func_pattern, content))

        if funcs > 0:
            type_hint_ratio = typed_funcs / funcs
            if type_hint_ratio < 0.5:
                issues.append(f"Low type hint coverage: {type_hint_ratio:.0%}")
                completeness -= int((1 - type_hint_ratio) * 20)

        # Clarity checks
        clarity = 100

        # Check line length
        long_lines = sum(1 for line in lines if len(line) > 100)
        if long_lines > 0:
            issues.append(f"{long_lines} lines exceed 100 characters")
            clarity -= min(20, long_lines * 2)

        # Check function length
        in_function = False
        func_lines = 0
        for line in lines:
            if line.strip().startswith("def "):
                if in_function and func_lines > 50:
                    issues.append("Function exceeds 50 lines")
                    clarity -= 10
                in_function = True
                func_lines = 0
            elif in_function:
                func_lines += 1

        # Efficiency checks
        efficiency = 100

        # Check for common inefficiencies
        if "for i in range(len(" in content:
            suggestions.append("Consider using enumerate() instead of range(len())")
            efficiency -= 5

        if ".append(" in content and "for " in content:
            suggestions.append("Consider list comprehension instead of append in loop")

        # Testability checks
        testability = 100

        # Check for global state
        global_pattern = r"^[A-Z_]+\s*=\s*[^#\n]+"
        globals_count = len(re.findall(global_pattern, content, re.MULTILINE))
        if globals_count > 5:
            issues.append(f"High global state count: {globals_count}")
            testability -= 10

        return QualityScore(
            file_path=str(file_path),
            analysis_type="code",
            correctness=max(0, correctness),
            completeness=max(0, completeness),
            clarity=max(0, clarity),
            efficiency=max(0, efficiency),
            testability=max(0, testability),
            issues=issues,
            suggestions=suggestions,
        )

    def _analyze_markdown(self, file_path: Path, content: str) -> QualityScore:
        """Analyze Markdown file for quality."""
        issues = []
        suggestions = []

        lines = content.split("\n")
        total_lines = len(lines)

        # Correctness checks
        correctness = 100

        # Check for broken links (simple check)
        link_pattern = r"\[([^\]]+)\]\(([^)]+)\)"
        links = re.findall(link_pattern, content)
        # Note: Full link validation would require HTTP requests

        # Completeness checks
        completeness = 100

        # Check for title
        if not content.strip().startswith("# "):
            issues.append("Missing document title (H1)")
            completeness -= 20

        # Check for sections
        h2_count = len(re.findall(r"^## ", content, re.MULTILINE))
        if h2_count < 2 and total_lines > 50:
            issues.append("Long document with few sections")
            completeness -= 10

        # Clarity checks
        clarity = 100

        # Check for code blocks
        code_blocks = len(re.findall(r"```", content))
        if code_blocks % 2 != 0:
            issues.append("Unclosed code block")
            clarity -= 15

        # Check line length in non-code sections
        in_code = False
        for line in lines:
            if line.startswith("```"):
                in_code = not in_code
            elif not in_code and len(line) > 120:
                clarity -= 2

        # Efficiency checks (token efficiency)
        efficiency = 100

        # Estimate tokens (rough: 1 token ≈ 4 chars)
        estimated_tokens = len(content) // 4
        tokens_per_line = estimated_tokens / max(1, total_lines)

        if tokens_per_line > 30:
            suggestions.append("Consider more concise content for token efficiency")
            efficiency -= 10

        # Testability (verifiability for docs)
        testability = 100

        # Check for examples
        if "```" not in content and total_lines > 30:
            suggestions.append("Consider adding code examples")
            testability -= 15

        return QualityScore(
            file_path=str(file_path),
            analysis_type="documentation",
            correctness=max(0, correctness),
            completeness=max(0, completeness),
            clarity=max(0, clarity),
            efficiency=max(0, efficiency),
            testability=max(0, testability),
            issues=issues,
            suggestions=suggestions,
        )

    def _load_code_patterns(self) -> dict[str, Any]:
        """Load code analysis patterns."""
        return {
            "anti_patterns": [
                (r"except:\s*$", "Bare except clause"),
                (r"from .+ import \*", "Wildcard import"),
                (r"print\(", "Debug print statement"),
            ],
            "good_patterns": [
                (r"def \w+\([^)]*\)\s*->", "Type-annotated function"),
                (r'"""[\s\S]*?"""', "Docstring"),
                (r"@pytest\.", "Test decorator"),
            ],
        }

    def _load_doc_patterns(self) -> dict[str, Any]:
        """Load documentation analysis patterns."""
        return {
            "required_sections": [
                "Overview",
                "Usage",
                "Example",
            ],
            "good_patterns": [
                (r"```\w+", "Language-specified code block"),
                (r"\| .+ \|", "Table"),
                (r"- \[[ x]\]", "Checklist"),
            ],
        }


def analyze_quality(path: Path) -> QualityScore:
    """Convenience function to analyze a single file."""
    analyzer = QualityAnalyzer()
    return analyzer.analyze_file(path)
