"""
Content Analyzer - Document content and token analysis.

This module provides:
- ContentMetrics: Structured metrics for document content
- ContentAnalyzer: Analyzer for token efficiency and structure

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
class ContentMetrics:
    """Metrics for document content analysis."""

    # Basic metrics
    total_lines: int = 0
    total_chars: int = 0
    estimated_tokens: int = 0

    # Structure metrics
    header_count: int = 0
    code_block_count: int = 0
    table_count: int = 0
    link_count: int = 0
    list_item_count: int = 0

    # Efficiency metrics
    tokens_per_section: float = 0.0
    content_density: float = 0.0  # Non-whitespace ratio

    # Metadata
    file_path: str = ""
    sections: list[str] = field(default_factory=list)

    @property
    def efficiency_score(self) -> int:
        """Calculate token efficiency score (0-100)."""
        # Lower tokens per section is better
        if self.tokens_per_section == 0:
            return 100

        # Target: ~100 tokens per section
        target = 100
        ratio = target / max(self.tokens_per_section, 1)

        # Cap at 100
        return min(100, int(ratio * 100))

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "file_path": self.file_path,
            "basic": {
                "lines": self.total_lines,
                "chars": self.total_chars,
                "tokens": self.estimated_tokens,
            },
            "structure": {
                "headers": self.header_count,
                "code_blocks": self.code_block_count,
                "tables": self.table_count,
                "links": self.link_count,
                "list_items": self.list_item_count,
            },
            "efficiency": {
                "tokens_per_section": round(self.tokens_per_section, 2),
                "content_density": round(self.content_density, 2),
                "efficiency_score": self.efficiency_score,
            },
            "sections": self.sections,
        }


class ContentAnalyzer:
    """
    Analyzer for document content and token efficiency.

    Features:
    - Token estimation
    - Structure analysis
    - Efficiency metrics
    - Section extraction
    """

    # Average tokens per character (rough estimate for English)
    TOKENS_PER_CHAR = 0.25

    def __init__(self):
        """Initialize the content analyzer."""
        pass

    def analyze_file(self, file_path: Path) -> ContentMetrics:
        """
        Analyze a file for content metrics.

        Args:
            file_path: Path to the file

        Returns:
            ContentMetrics with analysis results
        """
        if not file_path.exists():
            return ContentMetrics(file_path=str(file_path))

        content = file_path.read_text(encoding="utf-8")
        return self.analyze_content(content, str(file_path))

    def analyze_content(self, content: str, file_path: str = "") -> ContentMetrics:
        """
        Analyze content string for metrics.

        Args:
            content: Content to analyze
            file_path: Optional file path for metadata

        Returns:
            ContentMetrics with analysis results
        """
        lines = content.split("\n")

        # Basic metrics
        total_lines = len(lines)
        total_chars = len(content)
        estimated_tokens = int(total_chars * self.TOKENS_PER_CHAR)

        # Structure metrics
        header_count = len(re.findall(r"^#+\s", content, re.MULTILINE))
        code_block_count = len(re.findall(r"```", content)) // 2
        table_count = self._count_tables(content)
        link_count = len(re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content))
        list_item_count = len(re.findall(r"^[\s]*[-*+]\s", content, re.MULTILINE))

        # Extract sections
        sections = self._extract_sections(content)

        # Efficiency metrics
        section_count = max(1, header_count)
        tokens_per_section = estimated_tokens / section_count

        # Content density (non-whitespace ratio)
        non_whitespace = len(re.sub(r"\s", "", content))
        content_density = non_whitespace / max(1, total_chars)

        return ContentMetrics(
            file_path=file_path,
            total_lines=total_lines,
            total_chars=total_chars,
            estimated_tokens=estimated_tokens,
            header_count=header_count,
            code_block_count=code_block_count,
            table_count=table_count,
            link_count=link_count,
            list_item_count=list_item_count,
            tokens_per_section=tokens_per_section,
            content_density=content_density,
            sections=sections,
        )

    def analyze_directory(
        self, dir_path: Path, extensions: list[str] | None = None
    ) -> dict[str, ContentMetrics]:
        """
        Analyze all matching files in a directory.

        Args:
            dir_path: Path to directory
            extensions: File extensions to analyze

        Returns:
            Dict mapping file paths to ContentMetrics
        """
        extensions = extensions or [".md"]
        results = {}

        for ext in extensions:
            for file_path in dir_path.rglob(f"*{ext}"):
                # Skip hidden directories
                if any(part.startswith(".") for part in file_path.parts):
                    continue
                try:
                    metrics = self.analyze_file(file_path)
                    results[str(file_path)] = metrics
                except Exception as e:
                    logger.error(f"Error analyzing {file_path}: {e}")

        return results

    def get_summary(self, metrics_list: list[ContentMetrics]) -> dict[str, Any]:
        """
        Get summary statistics for multiple files.

        Args:
            metrics_list: List of ContentMetrics

        Returns:
            Summary dictionary
        """
        if not metrics_list:
            return {"error": "No metrics to summarize"}

        total_tokens = sum(m.estimated_tokens for m in metrics_list)
        total_lines = sum(m.total_lines for m in metrics_list)
        avg_efficiency = sum(m.efficiency_score for m in metrics_list) / len(
            metrics_list
        )

        return {
            "file_count": len(metrics_list),
            "total_tokens": total_tokens,
            "total_lines": total_lines,
            "average_efficiency_score": round(avg_efficiency, 1),
            "tokens_by_file": {
                m.file_path: m.estimated_tokens
                for m in sorted(
                    metrics_list, key=lambda x: x.estimated_tokens, reverse=True
                )[:10]
            },
        }

    def _count_tables(self, content: str) -> int:
        """Count markdown tables in content."""
        # Simple heuristic: count lines starting with |
        table_lines = [l for l in content.split("\n") if l.strip().startswith("|")]

        # Estimate tables (at least 3 lines per table)
        return len(table_lines) // 3

    def _extract_sections(self, content: str) -> list[str]:
        """Extract section headers from content."""
        sections = []

        for line in content.split("\n"):
            if line.startswith("#"):
                # Clean the header
                header = re.sub(r"^#+\s*", "", line)
                sections.append(header)

        return sections

    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for text.

        Args:
            text: Text to estimate

        Returns:
            Estimated token count
        """
        return int(len(text) * self.TOKENS_PER_CHAR)

    def suggest_optimizations(self, metrics: ContentMetrics) -> list[str]:
        """
        Suggest optimizations based on metrics.

        Args:
            metrics: ContentMetrics to analyze

        Returns:
            List of optimization suggestions
        """
        suggestions = []

        # Token efficiency
        if metrics.tokens_per_section > 200:
            suggestions.append(
                f"Consider breaking into more sections "
                f"(current: {metrics.tokens_per_section:.0f} tokens/section)"
            )

        # Content density
        if metrics.content_density < 0.5:
            suggestions.append("High whitespace ratio - consider compacting content")

        # Structure
        if metrics.header_count < 3 and metrics.total_lines > 100:
            suggestions.append("Long document with few headers - add more structure")

        if metrics.code_block_count == 0 and metrics.total_lines > 50:
            suggestions.append("No code examples - consider adding examples")

        if metrics.table_count == 0 and metrics.list_item_count > 20:
            suggestions.append(
                "Many list items - consider using tables for structured data"
            )

        return suggestions


def analyze_content(path: Path) -> ContentMetrics:
    """Convenience function to analyze a single file."""
    analyzer = ContentAnalyzer()
    return analyzer.analyze_file(path)
