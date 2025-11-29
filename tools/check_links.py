#!/usr/bin/env python
"""
Link Checker Script for Pre-commit Hook.

This script checks all internal links in the knowledge base
and reports any broken links found.

Usage:
    python tools/check_links.py [--verbose]

Exit codes:
    0 - All links valid
    1 - Broken links found
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def main() -> int:
    """
    Check all links in the knowledge base.

    Returns:
        Exit code (0 = success, 1 = broken links found)
    """
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    try:
        from sage.capabilities.checkers.links import LinkChecker

        kb_path = Path(__file__).parent.parent
        checker = LinkChecker(kb_path=kb_path)
        report = checker.check_all()

        # Print summary
        print("📊 Link Check Results")
        print(f"   Files checked: {report.files_checked}")
        print(f"   Total links: {report.total_links}")
        print(f"   Valid: {report.valid_count}")
        print(f"   Broken: {report.broken_count}")
        print(f"   Warnings: {report.warning_count}")
        print(f"   Duration: {report.duration_ms:.0f}ms")

        # Print broken links
        if report.broken_count > 0:
            print(f"\n❌ Broken links ({report.broken_count}):")
            for result in report.results:
                if result.status.value == "broken":
                    print(f"   {result.source_file}:{result.line_number}")
                    print(f"      → {result.link_target}")
                    print(f"      {result.message}")

        # Print warnings if verbose
        if verbose and report.warning_count > 0:
            print(f"\n⚠️  Warnings ({report.warning_count}):")
            for result in report.results:
                if result.status.value == "warning":
                    print(f"   {result.source_file}:{result.line_number}")
                    print(f"      → {result.link_target}")
                    print(f"      {result.message}")

        # Final status
        if report.broken_count == 0:
            print("\n✅ All links valid")
            return 0
        else:
            print(f"\n❌ {report.broken_count} broken link(s) found")
            return 1

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure sage-kb is installed: pip install -e .")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
