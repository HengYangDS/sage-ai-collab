"""
Documentation Checker - Validate documentation against SAGE standards.

This module provides:
- DocIssue: Individual documentation issue
- DocReport: Comprehensive documentation check report
- DocumentationChecker: Validate against documentation_standards.md

Rules implemented:
- FORMAT-001: H1 title required
- FORMAT-002: TOC required (>60 lines or >3 H2)
- FORMAT-003: Heading numbering (1., 1.1, etc.)
- STRUCT-001: Related section required
- STRUCT-002: Footer required
- METRIC-001: Lines per file (<300)
- METRIC-002: Nesting depth (≤4)
- METRIC-003: H2 count (recommended 5-15)
- METRIC-004: Related links count (3-5)
- NAMING-001: File naming convention (snake_case)

Author: SAGE AI Collab Team
Version: 0.1.0
"""

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class Severity(Enum):
    """Issue severity levels."""

    ERROR = "error"  # Must fix
    WARNING = "warning"  # Should fix
    INFO = "info"  # Consider fixing


@dataclass
class DocIssue:
    """Individual documentation issue."""

    file: str
    line: int
    rule: str
    message: str
    severity: Severity
    auto_fixable: bool = False
    suggestion: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "file": self.file,
            "line": self.line,
            "rule": self.rule,
            "message": self.message,
            "severity": self.severity.value,
            "auto_fixable": self.auto_fixable,
            "suggestion": self.suggestion,
        }


@dataclass
class DocReport:
    """Documentation check report."""

    total_files: int
    error_count: int
    warning_count: int
    info_count: int
    issues: list[DocIssue]
    files_checked: list[str]
    duration_ms: float
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return self.error_count > 0

    @property
    def pass_rate(self) -> float:
        """Percentage of files without errors."""
        files_with_errors = len(
            set(i.file for i in self.issues if i.severity == Severity.ERROR)
        )
        return (
            (self.total_files - files_with_errors) / self.total_files * 100
            if self.total_files > 0
            else 100
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_files": self.total_files,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "info_count": self.info_count,
            "pass_rate": round(self.pass_rate, 2),
            "duration_ms": round(self.duration_ms, 2),
            "timestamp": self.timestamp.isoformat(),
            "issues": [i.to_dict() for i in self.issues],
        }


class DocumentationChecker:
    """
    Check documentation against SAGE standards.

    Implements rules from .knowledge/practices/documentation/documentation_standards.md
    """

    # Regex patterns
    H1_PATTERN = re.compile(r"^# .+$", re.MULTILINE)
    H2_PATTERN = re.compile(r"^## .+$", re.MULTILINE)
    H3_PATTERN = re.compile(r"^### .+$", re.MULTILINE)
    HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
    NUMBERED_H2_PATTERN = re.compile(r"^## \d+\.\s+.+$", re.MULTILINE)
    TOC_PATTERN = re.compile(r"\[.+\]\(#.+\)")
    RELATED_SECTION_PATTERN = re.compile(r"^## Related", re.MULTILINE)
    FOOTER_PATTERN = re.compile(r"\*Part of SAGE Knowledge Base", re.MULTILINE)
    LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

    # File naming patterns
    SNAKE_CASE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*\.md$")
    ADR_PATTERN = re.compile(r"^ADR-\d{4}-.+\.md$")
    SESSION_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}-.+\.md$")

    def __init__(self, strict: bool = False):
        """
        Initialize documentation checker.

        Args:
            strict: If True, treat warnings as errors
        """
        self.strict = strict

    def check_file(self, file_path: Path) -> list[DocIssue]:
        """
        Check a single file against documentation standards.

        Args:
            file_path: Path to the Markdown file

        Returns:
            List of DocIssue for each issue found
        """
        issues = []

        try:
            content = file_path.read_text(encoding="utf-8")
            lines = content.split("\n")
            total_lines = len(lines)
            file_str = str(file_path)

            # =================================================================
            # FORMAT Rules
            # =================================================================

            # FORMAT-001: H1 title required
            if not self.H1_PATTERN.search(content):
                issues.append(
                    DocIssue(
                        file=file_str,
                        line=1,
                        rule="FORMAT-001",
                        message="Missing H1 title",
                        severity=Severity.ERROR,
                        suggestion="Add '# Title' at the beginning of the document",
                    )
                )

            # FORMAT-002: TOC required for long documents
            h2_count = len(self.H2_PATTERN.findall(content))
            has_toc = bool(self.TOC_PATTERN.search(content[:1000]))

            if (total_lines > 60 or h2_count > 3) and not has_toc:
                issues.append(
                    DocIssue(
                        file=file_str,
                        line=1,
                        rule="FORMAT-002",
                        message=f"Missing TOC ({total_lines} lines, {h2_count} H2 sections)",
                        severity=Severity.WARNING,
                        auto_fixable=True,
                        suggestion="Add Table of Contents with vertical format:\n- [1. Section](#1-section)\n- [2. Section](#2-section)",
                    )
                )

            # FORMAT-003: H2 numbering check (for documents with TOC)
            if has_toc and h2_count > 0:
                numbered_h2_count = len(self.NUMBERED_H2_PATTERN.findall(content))
                # Exclude "Related" section from numbering requirement
                expected_numbered = h2_count - (
                    1 if self.RELATED_SECTION_PATTERN.search(content) else 0
                )
                if numbered_h2_count < expected_numbered - 1:  # Allow some flexibility
                    issues.append(
                        DocIssue(
                            file=file_str,
                            line=1,
                            rule="FORMAT-003",
                            message=f"H2 sections should be numbered (found {numbered_h2_count}/{expected_numbered})",
                            severity=Severity.INFO,
                            suggestion="Number H2 sections: ## 1. Section, ## 2. Section",
                        )
                    )

            # =================================================================
            # STRUCT Rules
            # =================================================================

            # STRUCT-001: Related section required for substantial docs
            if total_lines > 30 and not self.RELATED_SECTION_PATTERN.search(content):
                issues.append(
                    DocIssue(
                        file=file_str,
                        line=total_lines,
                        rule="STRUCT-001",
                        message="Missing '## Related' section",
                        severity=Severity.WARNING,
                        suggestion="Add '## Related' section with 3-5 cross-references",
                    )
                )

            # STRUCT-002: Footer required
            if total_lines > 50 and not self.FOOTER_PATTERN.search(content):
                issues.append(
                    DocIssue(
                        file=file_str,
                        line=total_lines,
                        rule="STRUCT-002",
                        message="Missing SAGE footer",
                        severity=Severity.INFO,
                        suggestion="Add '*Part of SAGE Knowledge Base*' at the end",
                    )
                )

            # =================================================================
            # METRIC Rules
            # =================================================================

            # METRIC-001: Lines per file
            if total_lines > 300:
                issues.append(
                    DocIssue(
                        file=file_str,
                        line=300,
                        rule="METRIC-001",
                        message=f"File too long ({total_lines} > 300 lines)",
                        severity=Severity.INFO,
                        suggestion="Consider splitting into multiple files",
                    )
                )

            # METRIC-002: Heading nesting depth
            max_depth = 0
            for match in self.HEADING_PATTERN.finditer(content):
                depth = len(match.group(1))
                max_depth = max(max_depth, depth)

            if max_depth > 4:
                issues.append(
                    DocIssue(
                        file=file_str,
                        line=1,
                        rule="METRIC-002",
                        message=f"Heading nesting too deep ({max_depth} > 4 levels)",
                        severity=Severity.WARNING,
                        suggestion="Flatten heading structure or split document",
                    )
                )

            # METRIC-003: H2 count recommendation
            if total_lines > 100:
                if h2_count < 3:
                    issues.append(
                        DocIssue(
                            file=file_str,
                            line=1,
                            rule="METRIC-003",
                            message=f"Too few H2 sections ({h2_count} for {total_lines} lines)",
                            severity=Severity.INFO,
                            suggestion="Add more H2 sections (recommended: 5-15)",
                        )
                    )
                elif h2_count > 20:
                    issues.append(
                        DocIssue(
                            file=file_str,
                            line=1,
                            rule="METRIC-003",
                            message=f"Too many H2 sections ({h2_count})",
                            severity=Severity.INFO,
                            suggestion="Consider consolidating or splitting document",
                        )
                    )

            # METRIC-004: Related links count
            if self.RELATED_SECTION_PATTERN.search(content):
                # Find Related section and count links
                related_match = self.RELATED_SECTION_PATTERN.search(content)
                if related_match:
                    related_section = content[related_match.start() :]
                    # Get until next H2 or end
                    next_h2 = self.H2_PATTERN.search(
                        related_section[len("## Related") :]
                    )
                    if next_h2:
                        related_section = related_section[
                            : len("## Related") + next_h2.start()
                        ]

                    related_links = len(self.LINK_PATTERN.findall(related_section))
                    if related_links < 3:
                        issues.append(
                            DocIssue(
                                file=file_str,
                                line=related_match.start(),
                                rule="METRIC-004",
                                message=f"Too few related links ({related_links} < 3)",
                                severity=Severity.INFO,
                                suggestion="Add 3-5 cross-references in Related section",
                            )
                        )

            # =================================================================
            # NAMING Rules
            # =================================================================

            # NAMING-001: File naming convention
            file_name = file_path.name

            # Determine expected pattern based on location
            is_adr = "decisions" in str(file_path) or "ADR" in file_name
            is_session = "history" in str(file_path) or "conversations" in str(
                file_path
            )
            is_index = file_name == "index.md"

            if is_index:
                pass  # index.md is always valid
            elif is_adr:
                if not self.ADR_PATTERN.match(file_name):
                    issues.append(
                        DocIssue(
                            file=file_str,
                            line=0,
                            rule="NAMING-001",
                            message="ADR file should match pattern 'ADR-NNNN-title.md'",
                            severity=Severity.WARNING,
                            suggestion="Rename to ADR-0001-description.md format",
                        )
                    )
            elif is_session:
                if not self.SESSION_PATTERN.match(
                    file_name
                ) and not file_name.startswith("_"):
                    issues.append(
                        DocIssue(
                            file=file_str,
                            line=0,
                            rule="NAMING-001",
                            message="Session file should match pattern 'YYYY-MM-DD-topic.md'",
                            severity=Severity.INFO,
                            suggestion="Rename to 2025-11-30-topic.md format",
                        )
                    )
            else:
                if not self.SNAKE_CASE_PATTERN.match(file_name):
                    # Check if it's a special file (starts with uppercase or _)
                    if not file_name.startswith("_") and not file_name[0].isupper():
                        issues.append(
                            DocIssue(
                                file=file_str,
                                line=0,
                                rule="NAMING-001",
                                message="File name should be snake_case",
                                severity=Severity.INFO,
                                suggestion=f"Rename to {file_name.lower().replace('-', '_')}",
                            )
                        )

        except Exception as e:
            logger.error(f"Error checking file {file_path}: {e}")
            issues.append(
                DocIssue(
                    file=str(file_path),
                    line=0,
                    rule="ERROR",
                    message=f"File read error: {e}",
                    severity=Severity.ERROR,
                )
            )

        return issues

    def check_directory(
        self, dir_path: Path, pattern: str = "**/*.md"
    ) -> list[DocIssue]:
        """
        Check all files in a directory.

        Args:
            dir_path: Directory to check
            pattern: Glob pattern for files

        Returns:
            List of all issues found
        """
        all_issues = []

        for file_path in dir_path.glob(pattern):
            if file_path.is_file():
                issues = self.check_file(file_path)
                all_issues.extend(issues)

        return all_issues

    def check_all(
        self, kb_path: Path, directories: list[str] | None = None
    ) -> DocReport:
        """
        Check all documentation in the knowledge base.

        Args:
            kb_path: Path to knowledge base root
            directories: Specific directories to check (default: content, docs, .context)

        Returns:
            DocReport with all results
        """
        import time

        start_time = time.monotonic()

        if directories is None:
            directories = ["content", "docs", ".context"]

        all_issues = []
        files_checked = []

        for dir_name in directories:
            dir_path = kb_path / dir_name
            if dir_path.exists():
                for file_path in dir_path.glob("**/*.md"):
                    if file_path.is_file():
                        issues = self.check_file(file_path)
                        all_issues.extend(issues)
                        files_checked.append(str(file_path.relative_to(kb_path)))

        duration = (time.monotonic() - start_time) * 1000

        # Count by severity
        errors = sum(1 for i in all_issues if i.severity == Severity.ERROR)
        warnings = sum(1 for i in all_issues if i.severity == Severity.WARNING)
        infos = sum(1 for i in all_issues if i.severity == Severity.INFO)

        return DocReport(
            total_files=len(files_checked),
            error_count=errors,
            warning_count=warnings,
            info_count=infos,
            issues=all_issues,
            files_checked=files_checked,
            duration_ms=duration,
        )


# =============================================================================
# Convenience Functions
# =============================================================================


def check_documentation(kb_path: Path | None = None) -> DocReport:
    """Quick function to check all documentation."""
    if kb_path is None:
        kb_path = Path.cwd()
    checker = DocumentationChecker()
    return checker.check_all(kb_path)


def check_file(file_path: Path) -> list[DocIssue]:
    """Quick function to check a single file."""
    checker = DocumentationChecker()
    return checker.check_file(file_path)


# =============================================================================
# CLI Entry Point (for pre-commit)
# =============================================================================


def main() -> int:
    """
    CLI entry point for pre-commit hook.

    Returns:
        Exit code (0 = success, 1 = errors found)
    """
    import sys

    # Get files from command line args or check all
    files = sys.argv[1:] if len(sys.argv) > 1 else []

    checker = DocumentationChecker()
    all_issues = []

    if files:
        # Check specific files
        for file_str in files:
            file_path = Path(file_str)
            if file_path.exists() and file_path.suffix == ".md":
                issues = checker.check_file(file_path)
                all_issues.extend(issues)
    else:
        # Check all
        report = checker.check_all(Path.cwd())
        all_issues = report.issues

    # Print issues
    errors = [i for i in all_issues if i.severity == Severity.ERROR]
    warnings = [i for i in all_issues if i.severity == Severity.WARNING]

    if errors:
        print(f"\n❌ {len(errors)} error(s) found:")
        for issue in errors:
            print(f"  {issue.file}:{issue.line} [{issue.rule}] {issue.message}")

    if warnings:
        print(f"\n⚠️  {len(warnings)} warning(s) found:")
        for issue in warnings:
            print(f"  {issue.file}:{issue.line} [{issue.rule}] {issue.message}")

    if not errors and not warnings:
        print("✅ All documentation checks passed")

    return 1 if errors else 0


if __name__ == "__main__":
    exit(main())
