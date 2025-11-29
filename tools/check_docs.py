#!/usr/bin/env python3
"""
Documentation Standards Checker.

Checks markdown documents against SAGE documentation standards:
- Line count limits (<300 lines recommended)
- YAML frontmatter presence
- TOC presence for large documents
- Standard footer
- Section numbering

Usage:
    python scripts/check_docs.py [path]
    python scripts/check_docs.py docs/
    python scripts/check_docs.py .knowledge/
"""

import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Issue:
    """Documentation issue."""
    severity: str  # error, warning, info
    message: str
    line: Optional[int] = None


@dataclass
class CheckResult:
    """Result of checking a document."""
    path: Path
    lines: int
    has_frontmatter: bool
    has_toc: bool
    has_footer: bool
    has_numbered_sections: bool
    issues: List[Issue] = field(default_factory=list)
    
    @property
    def status(self) -> str:
        errors = sum(1 for i in self.issues if i.severity == "error")
        warnings = sum(1 for i in self.issues if i.severity == "warning")
        if errors > 0:
            return "FAIL"
        elif warnings > 0:
            return "WARN"
        return "PASS"


def check_document(path: Path) -> CheckResult:
    """Check a single document against standards."""
    content = path.read_text(encoding="utf-8")
    lines = content.split("\n")
    line_count = len(lines)
    
    result = CheckResult(
        path=path,
        lines=line_count,
        has_frontmatter=content.startswith("---"),
        has_toc="## Table of Contents" in content or "## TOC" in content,
        has_footer="*Part of SAGE Knowledge Base*" in content or "*SAGE Knowledge Base" in content,
        has_numbered_sections="## 1." in content or "## 1 " in content,
    )
    
    # Check line count
    if line_count > 600:
        result.issues.append(Issue(
            severity="error",
            message=f"Document too long: {line_count} lines (max 300, critical >600)"
        ))
    elif line_count > 300:
        result.issues.append(Issue(
            severity="warning", 
            message=f"Document exceeds recommended length: {line_count} lines (recommended <300)"
        ))
    
    # Check frontmatter
    if not result.has_frontmatter:
        result.issues.append(Issue(
            severity="warning",
            message="Missing YAML frontmatter"
        ))
    else:
        # Check frontmatter fields
        frontmatter_end = content.find("---", 3)
        if frontmatter_end > 0:
            frontmatter = content[3:frontmatter_end]
            if "last_updated" not in frontmatter and "date" not in frontmatter:
                result.issues.append(Issue(
                    severity="info",
                    message="Frontmatter missing last_updated field"
                ))
            if "tokens" not in frontmatter:
                result.issues.append(Issue(
                    severity="info",
                    message="Frontmatter missing tokens estimate"
                ))
    
    # Check TOC for large documents
    if line_count > 60 and not result.has_toc:
        # Count H2 headings
        h2_count = sum(1 for line in lines if line.startswith("## "))
        if h2_count > 3:
            result.issues.append(Issue(
                severity="warning",
                message=f"Large document ({line_count} lines, {h2_count} H2s) missing TOC"
            ))
    
    # Check footer
    if not result.has_footer:
        result.issues.append(Issue(
            severity="info",
            message="Missing standard footer"
        ))
    
    # Check section numbering
    h2_lines = [(i, line) for i, line in enumerate(lines, 1) if line.startswith("## ")]
    if h2_lines and not result.has_numbered_sections:
        # Skip if it's just TOC and Related sections
        non_meta_h2 = [h for h in h2_lines if not any(
            x in h[1] for x in ["Table of Contents", "TOC", "Related", "References"]
        )]
        if len(non_meta_h2) > 2:
            result.issues.append(Issue(
                severity="info",
                message="H2 sections not numbered (e.g., '## 1. Section')"
            ))
    
    return result


def check_directory(path: Path, recursive: bool = True) -> List[CheckResult]:
    """Check all markdown files in a directory."""
    results = []
    pattern = "**/*.md" if recursive else "*.md"
    
    for md_file in path.glob(pattern):
        # Skip certain directories
        if any(skip in str(md_file) for skip in [".git", "__pycache__", "node_modules"]):
            continue
        results.append(check_document(md_file))
    
    return results


def print_results(results: List[CheckResult], verbose: bool = False):
    """Print check results."""
    # Sort by status (FAIL first, then WARN, then PASS)
    status_order = {"FAIL": 0, "WARN": 1, "PASS": 2}
    results.sort(key=lambda r: (status_order.get(r.status, 3), -r.lines))
    
    # Summary counts
    total = len(results)
    passed = sum(1 for r in results if r.status == "PASS")
    warned = sum(1 for r in results if r.status == "WARN")
    failed = sum(1 for r in results if r.status == "FAIL")
    
    print("\n" + "=" * 70)
    print("SAGE Documentation Standards Check")
    print("=" * 70)
    
    # Print issues
    for result in results:
        if result.status == "PASS" and not verbose:
            continue
            
        status_color = {
            "FAIL": "\033[91m",  # Red
            "WARN": "\033[93m",  # Yellow
            "PASS": "\033[92m",  # Green
        }.get(result.status, "")
        reset = "\033[0m"
        
        print(f"\n{status_color}[{result.status}]{reset} {result.path} ({result.lines} lines)")
        
        for issue in result.issues:
            prefix = {
                "error": "  ❌",
                "warning": "  ⚠️",
                "info": "  ℹ️",
            }.get(issue.severity, "  •")
            print(f"{prefix} {issue.message}")
    
    # Summary
    print("\n" + "-" * 70)
    print(f"Summary: {total} files checked")
    print(f"  ✅ Passed: {passed}")
    print(f"  ⚠️  Warnings: {warned}")
    print(f"  ❌ Failed: {failed}")
    
    # Recommendations
    if failed > 0 or warned > 0:
        print("\nRecommendations:")
        
        over_limit = [r for r in results if r.lines > 300]
        if over_limit:
            print(f"  • {len(over_limit)} documents exceed 300 lines - consider splitting")
            for r in sorted(over_limit, key=lambda x: -x.lines)[:5]:
                print(f"    - {r.path.name}: {r.lines} lines")
        
        missing_frontmatter = [r for r in results if not r.has_frontmatter]
        if missing_frontmatter:
            print(f"  • {len(missing_frontmatter)} documents missing frontmatter")
        
        missing_toc = [r for r in results if not r.has_toc and r.lines > 60]
        if missing_toc:
            print(f"  • {len(missing_toc)} large documents missing TOC")
    
    print("=" * 70)
    
    return failed


def main():
    """Main entry point."""
    # Parse arguments
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    
    if not args:
        # Default: check docs/ and .knowledge/
        paths = [Path("docs"), Path(".knowledge")]
    else:
        paths = [Path(a) for a in args]
    
    all_results = []
    
    for path in paths:
        if not path.exists():
            print(f"Warning: Path not found: {path}")
            continue
            
        if path.is_file():
            all_results.append(check_document(path))
        else:
            all_results.extend(check_directory(path))
    
    if not all_results:
        print("No markdown files found.")
        return 0
    
    failed = print_results(all_results, verbose)
    return 1 if failed > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
