#!/usr/bin/env python3
"""SAGE Link Checker.

Checks that all internal Markdown links point to existing files.
Skips external links (http/https), anchors (#), and mailto links.
"""

import re
import sys
from pathlib import Path

# Pattern to match Markdown links: [text](target)
LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

# Directories to check
CHECK_DIRS = ["content", "docs", ".context", ".history"]

# Patterns to skip
SKIP_DIRS = [".git", ".outputs", "node_modules", "__pycache__", ".venv"]


def is_external_link(target: str) -> bool:
    """Check if link is external or special."""
    return target.startswith(
        (
            "http://",
            "https://",
            "#",
            "mailto:",
            "tel:",
            "ftp://",
        )
    )


def check_links_in_file(file_path: Path) -> list[str]:
    """Check all links in a single file."""
    errors = []

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return [f"{file_path}: Cannot read file - {e}"]

    for match in LINK_PATTERN.finditer(content):
        text, target = match.groups()

        # Skip external links
        if is_external_link(target):
            continue

        # Handle anchor links within target
        target_path_str = target.split("#")[0]

        # Skip pure anchor links
        if not target_path_str:
            continue

        # Resolve relative path
        try:
            if target_path_str.startswith("/"):
                # Absolute path from project root
                target_path = Path(".") / target_path_str.lstrip("/")
            else:
                # Relative path from file location
                target_path = (file_path.parent / target_path_str).resolve()

            # Check if target exists
            if not target_path.exists():
                errors.append(
                    f"{file_path}: Broken link [{text}]({target}) -> {target_path}"
                )
        except Exception as e:
            errors.append(f"{file_path}: Invalid link [{text}]({target}) - {e}")

    return errors


def get_files_to_check() -> list[Path]:
    """Get list of Markdown files to check."""
    files = []

    for dir_name in CHECK_DIRS:
        dir_path = Path(dir_name)
        if dir_path.exists():
            for md_file in dir_path.rglob("*.md"):
                # Skip files in excluded directories
                if not any(skip in str(md_file) for skip in SKIP_DIRS):
                    files.append(md_file)

    # Also check root level markdown files
    for md_file in Path(".").glob("*.md"):
        files.append(md_file)

    return files


def main() -> int:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Check SAGE document links")
    parser.add_argument("files", nargs="*", help="Specific files to check")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    # Get files to check
    if args.files:
        files = [Path(f) for f in args.files if f.endswith(".md")]
    else:
        files = get_files_to_check()

    if args.verbose:
        print(f"Checking links in {len(files)} files...")

    # Check all files
    all_errors = []
    for file_path in files:
        errors = check_links_in_file(file_path)
        all_errors.extend(errors)

    # Report results
    if all_errors:
        print("❌ Broken links found:")
        for error in all_errors:
            print(f"  {error}")
        return 1
    else:
        if args.verbose:
            print(f"✅ All links valid in {len(files)} files")
        return 0


if __name__ == "__main__":
    sys.exit(main())
