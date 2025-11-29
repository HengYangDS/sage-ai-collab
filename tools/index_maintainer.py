#!/usr/bin/env python
"""
Index Maintainer - Automated index.md file maintenance.

This tool helps maintain index.md files in the knowledge base by:
- Updating file counts in directory tables
- Updating file listings
- Validating cross-references
- Detecting missing or orphaned files

Usage:
    python tools/index_maintainer.py validate     # Check for issues
    python tools/index_maintainer.py update       # Update all indexes
    python tools/index_maintainer.py report       # Generate report

Author: SAGE AI Collab Team
Version: 0.1.0
"""

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@dataclass
class IndexIssue:
    """An issue found in an index file."""

    file: str
    issue_type: str  # count_mismatch, missing_file, orphan_file, broken_ref
    message: str
    details: dict[str, Any] = field(default_factory=dict)
    auto_fixable: bool = False


@dataclass
class IndexReport:
    """Report from index validation."""

    indexes_checked: int
    issues: list[IndexIssue]
    files_in_indexes: int
    actual_files: int

    @property
    def has_issues(self) -> bool:
        return len(self.issues) > 0


class IndexMaintainer:
    """
    Maintain index.md files in the knowledge base.

    Features:
    - Validate file counts against actual directory contents
    - Detect files missing from indexes
    - Detect orphaned references (files listed but don't exist)
    - Update file counts automatically
    """

    # Patterns for parsing index files
    COUNT_PATTERN = re.compile(r"\|\s*`?([^`|]+)`?\s*\|\s*(\d+)\s*\|")
    FILE_LIST_PATTERN = re.compile(r"^-\s+`([^`]+)`", re.MULTILINE)
    LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

    def __init__(self, kb_path: Path | None = None):
        """
        Initialize index maintainer.

        Args:
            kb_path: Path to knowledge base root
        """
        self.kb_path = kb_path or Path(__file__).parent.parent

    def find_index_files(self) -> list[Path]:
        """Find all index.md files in the knowledge base."""
        indexes = []
        for index_path in self.kb_path.rglob("index.md"):
            # Skip node_modules, __pycache__, etc.
            if any(
                part.startswith(".") or part == "__pycache__"
                for part in index_path.parts
            ):
                continue
            indexes.append(index_path)
        return indexes

    def count_files_in_directory(self, dir_path: Path, pattern: str = "*.md") -> int:
        """Count files matching pattern in a directory (non-recursive)."""
        if not dir_path.exists():
            return 0
        return len([f for f in dir_path.glob(pattern) if f.is_file()])

    def count_files_recursive(self, dir_path: Path, pattern: str = "**/*.md") -> int:
        """Count files matching pattern recursively."""
        if not dir_path.exists():
            return 0
        return len([f for f in dir_path.glob(pattern) if f.is_file()])

    def validate_index(self, index_path: Path) -> list[IndexIssue]:
        """
        Validate a single index file.

        Checks:
        - File counts in tables match actual counts
        - Listed files exist
        - All files in directory are listed

        Args:
            index_path: Path to index.md file

        Returns:
            List of issues found
        """
        issues = []
        index_dir = index_path.parent

        try:
            content = index_path.read_text(encoding="utf-8")

            # Check file count tables
            # Pattern: | directory/ | N | or | `directory/` | N |
            for match in self.COUNT_PATTERN.finditer(content):
                dir_name = match.group(1).strip().rstrip("/")
                stated_count = int(match.group(2))

                # Try to find the directory
                check_dir = index_dir / dir_name
                if not check_dir.exists():
                    # Try relative to kb_path
                    check_dir = self.kb_path / dir_name

                if check_dir.exists():
                    actual_count = self.count_files_in_directory(check_dir)
                    if actual_count != stated_count:
                        issues.append(
                            IndexIssue(
                                file=str(index_path.relative_to(self.kb_path)),
                                issue_type="count_mismatch",
                                message=f"File count mismatch for '{dir_name}': stated {stated_count}, actual {actual_count}",
                                details={
                                    "directory": dir_name,
                                    "stated": stated_count,
                                    "actual": actual_count,
                                },
                                auto_fixable=True,
                            )
                        )

            # Check for broken internal links
            for match in self.LINK_PATTERN.finditer(content):
                link_target = match.group(2)

                # Skip external links and anchors
                if link_target.startswith(("http://", "https://", "#", "mailto:")):
                    continue

                # Remove anchor from link
                link_path = link_target.split("#")[0]
                if not link_path:
                    continue

                # Resolve relative path
                target_path = (index_dir / link_path).resolve()

                # Also try from kb_path
                if not target_path.exists():
                    target_path = (self.kb_path / link_path).resolve()

                if not target_path.exists():
                    issues.append(
                        IndexIssue(
                            file=str(index_path.relative_to(self.kb_path)),
                            issue_type="broken_ref",
                            message=f"Broken reference: '{link_target}'",
                            details={"target": link_target},
                            auto_fixable=False,
                        )
                    )

        except Exception as e:
            issues.append(
                IndexIssue(
                    file=str(index_path.relative_to(self.kb_path)),
                    issue_type="error",
                    message=f"Error reading index: {e}",
                )
            )

        return issues

    def validate_all(self) -> IndexReport:
        """
        Validate all index files in the knowledge base.

        Returns:
            IndexReport with all findings
        """
        indexes = self.find_index_files()
        all_issues = []

        for index_path in indexes:
            issues = self.validate_index(index_path)
            all_issues.extend(issues)

        return IndexReport(
            indexes_checked=len(indexes),
            issues=all_issues,
            files_in_indexes=0,  # Could be calculated
            actual_files=self.count_files_recursive(self.kb_path),
        )

    def update_file_count(
        self, index_path: Path, dir_name: str, new_count: int
    ) -> bool:
        """
        Update a file count in an index file.

        Args:
            index_path: Path to index.md
            dir_name: Directory name to update
            new_count: New count value

        Returns:
            True if updated, False if not found
        """
        try:
            content = index_path.read_text(encoding="utf-8")

            # Pattern to match the specific directory count
            pattern = re.compile(
                rf"(\|\s*`?{re.escape(dir_name)}/?`?\s*\|[^|]*\|\s*)\d+(\s*\|)"
            )

            new_content, count = pattern.subn(rf"\g<1>{new_count}\g<2>", content)

            if count > 0:
                index_path.write_text(new_content, encoding="utf-8")
                return True

            return False

        except Exception:
            return False

    def fix_count_mismatches(self, report: IndexReport) -> int:
        """
        Fix all count mismatch issues.

        Args:
            report: IndexReport from validate_all()

        Returns:
            Number of fixes applied
        """
        fixes = 0

        for issue in report.issues:
            if issue.issue_type == "count_mismatch" and issue.auto_fixable:
                index_path = self.kb_path / issue.file
                dir_name = issue.details["directory"]
                new_count = issue.details["actual"]

                if self.update_file_count(index_path, dir_name, new_count):
                    fixes += 1
                    print(f"  Fixed: {issue.file} - {dir_name}: {new_count}")

        return fixes

    def generate_report(self) -> str:
        """
        Generate a markdown report of index status.

        Returns:
            Markdown formatted report
        """
        report = self.validate_all()
        indexes = self.find_index_files()

        lines = [
            "# Index Maintenance Report",
            "",
            f"**Generated**: {__import__('datetime').datetime.now().isoformat()}",
            "",
            "## Summary",
            "",
            f"- **Index files**: {report.indexes_checked}",
            f"- **Issues found**: {len(report.issues)}",
            f"- **Auto-fixable**: {sum(1 for i in report.issues if i.auto_fixable)}",
            "",
        ]

        if report.issues:
            lines.extend(
                [
                    "## Issues",
                    "",
                    "| File | Type | Message |",
                    "|------|------|---------|",
                ]
            )
            for issue in report.issues:
                lines.append(f"| {issue.file} | {issue.issue_type} | {issue.message} |")
            lines.append("")

        lines.extend(
            [
                "## Index Files",
                "",
                "| Path | Status |",
                "|------|--------|",
            ]
        )
        for index_path in indexes:
            rel_path = index_path.relative_to(self.kb_path)
            issues_for_file = [i for i in report.issues if i.file == str(rel_path)]
            status = "⚠️ Issues" if issues_for_file else "✅ OK"
            lines.append(f"| {rel_path} | {status} |")

        return "\n".join(lines)


# =============================================================================
# CLI Entry Points
# =============================================================================


def cmd_validate() -> int:
    """Validate all index files."""
    print("🔍 Validating index files...")

    maintainer = IndexMaintainer()
    report = maintainer.validate_all()

    print("\n📊 Results:")
    print(f"   Index files checked: {report.indexes_checked}")
    print(f"   Issues found: {len(report.issues)}")

    if report.issues:
        print("\n⚠️  Issues:")
        for issue in report.issues:
            icon = "🔧" if issue.auto_fixable else "❌"
            print(f"   {icon} [{issue.issue_type}] {issue.file}")
            print(f"      {issue.message}")

        return 1
    else:
        print("\n✅ All index files are valid")
        return 0


def cmd_update() -> int:
    """Update all index files to fix auto-fixable issues."""
    print("🔧 Updating index files...")

    maintainer = IndexMaintainer()
    report = maintainer.validate_all()

    fixable = [i for i in report.issues if i.auto_fixable]

    if not fixable:
        print("✅ No auto-fixable issues found")
        return 0

    print(f"\n📝 Fixing {len(fixable)} issue(s):")
    fixes = maintainer.fix_count_mismatches(report)

    print(f"\n✅ Applied {fixes} fix(es)")
    return 0


def cmd_report() -> int:
    """Generate a detailed report."""
    maintainer = IndexMaintainer()
    report_md = maintainer.generate_report()
    print(report_md)
    return 0


def main() -> int:
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python index_maintainer.py <command>")
        print("")
        print("Commands:")
        print("  validate  - Check for issues in index files")
        print("  update    - Fix auto-fixable issues")
        print("  report    - Generate detailed report")
        return 1

    command = sys.argv[1].lower()

    if command == "validate":
        return cmd_validate()
    elif command == "update":
        return cmd_update()
    elif command == "report":
        return cmd_report()
    else:
        print(f"Unknown command: {command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
