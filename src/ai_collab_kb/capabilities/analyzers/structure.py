"""
Structure Checker - Directory and file structure validation.

This module provides:
- StructureReport: Validation report with issues and suggestions
- StructureChecker: Validator for knowledge base structure

Author: AI Collaboration KB Team
Version: 2.0.0
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class StructureIssue:
    """A single structure validation issue."""

    severity: str  # "error", "warning", "info"
    category: str  # "missing", "extra", "naming", "content"
    path: str
    message: str
    suggestion: str = ""

    def to_dict(self) -> dict[str, str]:
        """Convert to dictionary."""
        return {
            "severity": self.severity,
            "category": self.category,
            "path": self.path,
            "message": self.message,
            "suggestion": self.suggestion,
        }


@dataclass
class StructureReport:
    """Report from structure validation."""

    valid: bool = True
    issues: list[StructureIssue] = field(default_factory=list)
    stats: dict[str, int] = field(default_factory=dict)

    @property
    def error_count(self) -> int:
        """Count of error-level issues."""
        return sum(1 for i in self.issues if i.severity == "error")

    @property
    def warning_count(self) -> int:
        """Count of warning-level issues."""
        return sum(1 for i in self.issues if i.severity == "warning")

    def add_issue(self, issue: StructureIssue) -> None:
        """Add an issue to the report."""
        self.issues.append(issue)
        if issue.severity == "error":
            self.valid = False

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "valid": self.valid,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "issues": [i.to_dict() for i in self.issues],
            "stats": self.stats,
        }


class StructureChecker:
    """
    Validator for knowledge base directory structure.

    Features:
    - Required directory validation
    - Required file validation
    - Naming convention checking
    - Structure completeness verification
    """

    # Expected directory structure
    REQUIRED_DIRS = [
        "01_core",
        "02_guidelines",
        "03_frameworks",
        "04_practices",
        "05_tools",
        "06_templates",
        "07_scenarios",
        "08_archive",
    ]

    REQUIRED_FILES = [
        "index.md",
        "aikb.yaml",
        "README.md",
        "01_core/principles.md",
        "01_core/quick_reference.md",
    ]

    EXPECTED_GUIDELINES = [
        "00_quick_start.md",
        "01_planning_design.md",
        "02_code_style.md",
        "03_engineering.md",
        "04_documentation.md",
        "05_python.md",
        "06_ai_collaboration.md",
        "07_cognitive.md",
        "08_quality.md",
        "09_success.md",
    ]

    def __init__(self, root_path: Path | None = None):
        """
        Initialize the structure checker.

        Args:
            root_path: Root path of knowledge base (default: current dir)
        """
        self.root_path = root_path or Path.cwd()

    def check(self) -> StructureReport:
        """
        Perform full structure validation.

        Returns:
            StructureReport with validation results
        """
        report = StructureReport()

        # Check required directories
        self._check_directories(report)

        # Check required files
        self._check_required_files(report)

        # Check guidelines structure
        self._check_guidelines(report)

        # Check naming conventions
        self._check_naming(report)

        # Collect statistics
        report.stats = self._collect_stats()

        return report

    def _check_directories(self, report: StructureReport) -> None:
        """Check required directories exist."""
        for dir_name in self.REQUIRED_DIRS:
            dir_path = self.root_path / dir_name
            if not dir_path.exists():
                report.add_issue(
                    StructureIssue(
                        severity="error",
                        category="missing",
                        path=dir_name,
                        message=f"Required directory missing: {dir_name}",
                        suggestion=f"Create directory: mkdir {dir_name}",
                    )
                )
            elif not dir_path.is_dir():
                report.add_issue(
                    StructureIssue(
                        severity="error",
                        category="content",
                        path=dir_name,
                        message=f"Expected directory but found file: {dir_name}",
                    )
                )

    def _check_required_files(self, report: StructureReport) -> None:
        """Check required files exist."""
        for file_path in self.REQUIRED_FILES:
            full_path = self.root_path / file_path
            if not full_path.exists():
                report.add_issue(
                    StructureIssue(
                        severity="error",
                        category="missing",
                        path=file_path,
                        message=f"Required file missing: {file_path}",
                        suggestion=f"Create file: {file_path}",
                    )
                )

    def _check_guidelines(self, report: StructureReport) -> None:
        """Check guidelines structure."""
        guidelines_dir = self.root_path / "02_guidelines"

        if not guidelines_dir.exists():
            return  # Already reported as missing directory

        existing_files = {f.name for f in guidelines_dir.glob("*.md")}

        for expected in self.EXPECTED_GUIDELINES:
            if expected not in existing_files:
                report.add_issue(
                    StructureIssue(
                        severity="warning",
                        category="missing",
                        path=f"02_guidelines/{expected}",
                        message=f"Expected guideline file missing: {expected}",
                        suggestion=f"Create guideline: 02_guidelines/{expected}",
                    )
                )

    def _check_naming(self, report: StructureReport) -> None:
        """Check naming conventions."""
        # Check for files that don't follow convention
        for md_file in self.root_path.rglob("*.md"):
            # Skip archive
            if "08_archive" in str(md_file):
                continue

            name = md_file.name

            # Check for spaces in names
            if " " in name:
                report.add_issue(
                    StructureIssue(
                        severity="warning",
                        category="naming",
                        path=str(md_file.relative_to(self.root_path)),
                        message="File name contains spaces",
                        suggestion="Use underscores instead of spaces",
                    )
                )

            # Check for uppercase in names (except README)
            if name != "README.md" and any(c.isupper() for c in name):
                report.add_issue(
                    StructureIssue(
                        severity="info",
                        category="naming",
                        path=str(md_file.relative_to(self.root_path)),
                        message="File name contains uppercase letters",
                        suggestion="Consider using lowercase with underscores",
                    )
                )

    def _collect_stats(self) -> dict[str, int]:
        """Collect structure statistics."""
        stats = {
            "directories": 0,
            "markdown_files": 0,
            "python_files": 0,
            "total_files": 0,
        }

        for item in self.root_path.rglob("*"):
            # Skip hidden and cache
            if any(part.startswith(".") for part in item.parts):
                continue
            if "__pycache__" in str(item):
                continue

            if item.is_dir():
                stats["directories"] += 1
            elif item.is_file():
                stats["total_files"] += 1
                if item.suffix == ".md":
                    stats["markdown_files"] += 1
                elif item.suffix == ".py":
                    stats["python_files"] += 1

        return stats

    def fix_issues(self, report: StructureReport, dry_run: bool = True) -> list[str]:
        """
        Attempt to fix reported issues.

        Args:
            report: StructureReport with issues
            dry_run: If True, only report what would be done

        Returns:
            List of actions taken (or would be taken)
        """
        actions = []

        for issue in report.issues:
            if issue.category == "missing" and issue.severity == "error":
                path = self.root_path / issue.path

                if issue.path.endswith("/") or "/" not in issue.path:
                    # Directory
                    action = f"Create directory: {issue.path}"
                    if not dry_run:
                        path.mkdir(parents=True, exist_ok=True)
                else:
                    # File
                    action = f"Create file: {issue.path}"
                    if not dry_run:
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.touch()

                actions.append(action)

        return actions


def check_structure(path: Path | None = None) -> StructureReport:
    """Convenience function to check structure."""
    checker = StructureChecker(path)
    return checker.check()
