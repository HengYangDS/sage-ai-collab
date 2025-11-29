#!/usr/bin/env python3
"""SAGE Index Generator.

Automatically generates and updates index.md files for knowledge directories.
Extracts titles and purposes from documents to create navigation indexes.
"""

import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# Directories that should have index files
INDEX_DIRS = [
    "content",
    "docs",
    ".context",
    ".history",
]

# Files to skip when building index
SKIP_PATTERNS = [
    r"^_",  # Files starting with underscore
    r"^index\.md$",  # Index files themselves
    r"^\.",  # Hidden files
]


def should_skip(filename: str) -> bool:
    """Check if file should be skipped."""
    for pattern in SKIP_PATTERNS:
        if re.match(pattern, filename):
            return True
    return False


def extract_title(file_path: Path) -> str:
    """Extract title from markdown file (first H1)."""
    try:
        content = file_path.read_text(encoding="utf-8")
        match = re.match(r"^# (.+)$", content, re.MULTILINE)
        if match:
            return match.group(1).strip()
    except Exception:
        pass

    # Fallback to filename
    return file_path.stem.replace("_", " ").replace("-", " ").title()


def extract_purpose(file_path: Path) -> str:
    """Extract purpose from markdown file (first blockquote after title)."""
    try:
        content = file_path.read_text(encoding="utf-8")
        match = re.search(r"^> (.+)$", content, re.MULTILINE)
        if match:
            purpose = match.group(1).strip()
            # Truncate if too long
            if len(purpose) > 60:
                return purpose[:57] + "..."
            return purpose
    except Exception:
        pass

    return "-"


def collect_files(directory: Path) -> dict[str, list[Path]]:
    """Collect markdown files grouped by subdirectory."""
    files_by_subdir = defaultdict(list)

    for md_file in directory.rglob("*.md"):
        if should_skip(md_file.name):
            continue

        # Get relative path from directory
        rel_path = md_file.relative_to(directory)

        # Determine subdirectory (first level)
        if len(rel_path.parts) > 1:
            subdir = rel_path.parts[0]
        else:
            subdir = "_root"

        files_by_subdir[subdir].append(md_file)

    return dict(files_by_subdir)


def generate_index_content(directory: Path) -> str:
    """Generate index.md content for a directory."""
    files_by_subdir = collect_files(directory)

    # Count total files
    total_files = sum(len(files) for files in files_by_subdir.values())

    # Generate content
    dir_name = directory.name
    if dir_name.startswith("."):
        dir_name = dir_name[1:]  # Remove leading dot for display

    content = f"""# {dir_name.title()} Index

> Navigation index for {directory.name} directory

---

## Overview

| Metric | Value |
|--------|-------|
| Total Files | {total_files} |
| Subdirectories | {len(files_by_subdir) - (1 if '_root' in files_by_subdir else 0)} |
| Last Updated | {datetime.now().strftime('%Y-%m-%d')} |

---

## Contents

"""

    # Sort subdirectories, put _root first
    subdirs = sorted(files_by_subdir.keys(), key=lambda x: (x != "_root", x))

    for subdir in subdirs:
        file_list = files_by_subdir[subdir]

        # Section header
        if subdir == "_root":
            content += "### Root Files\n\n"
        else:
            subdir_display = subdir.replace("_", " ").replace("-", " ").title()
            content += f"### {subdir_display}\n\n"

        # File table
        content += "| Document | Purpose |\n"
        content += "|----------|----------|\n"

        for file_path in sorted(file_list, key=lambda x: x.name):
            title = extract_title(file_path)
            purpose = extract_purpose(file_path)
            rel_path = file_path.relative_to(directory)

            # Use forward slashes for markdown links
            link_path = str(rel_path).replace("\\", "/")
            content += f"| [{title}]({link_path}) | {purpose} |\n"

        content += "\n"

    content += "---\n\n*Part of SAGE Knowledge Base*\n"

    return content


def update_index(directory: Path, write: bool = False) -> tuple[bool, str]:
    """Update index.md for a directory.

    Returns:
        Tuple of (needs_update, message)
    """
    index_path = directory / "index.md"
    new_content = generate_index_content(directory)

    # Check if update needed
    if index_path.exists():
        old_content = index_path.read_text(encoding="utf-8")
        # Compare ignoring the "Last Updated" line
        old_normalized = re.sub(
            r"Last Updated \| \d{4}-\d{2}-\d{2}", "Last Updated | DATE", old_content
        )
        new_normalized = re.sub(
            r"Last Updated \| \d{4}-\d{2}-\d{2}", "Last Updated | DATE", new_content
        )

        if old_normalized == new_normalized:
            return False, f"{index_path}: Up to date"

    if write:
        index_path.write_text(new_content, encoding="utf-8")
        return True, f"{index_path}: Updated"
    else:
        return True, f"{index_path}: Needs update (use --write to update)"


def main() -> int:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate SAGE index files")
    parser.add_argument(
        "--all", action="store_true", help="Update all index directories"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if indexes are up to date (exit 1 if not)",
    )
    parser.add_argument("--write", action="store_true", help="Write changes to files")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("dirs", nargs="*", help="Specific directories to update")
    args = parser.parse_args()

    # Determine directories to process
    if args.dirs:
        directories = [Path(d) for d in args.dirs]
    elif args.all:
        directories = [Path(d) for d in INDEX_DIRS if Path(d).exists()]
    else:
        # Default: check all
        directories = [Path(d) for d in INDEX_DIRS if Path(d).exists()]

    if args.verbose:
        print(f"Processing {len(directories)} directories...")

    # Process each directory
    needs_update = []
    for directory in directories:
        if not directory.exists():
            if args.verbose:
                print(f"  Skipping {directory}: does not exist")
            continue

        updated, message = update_index(directory, write=args.write)

        if args.verbose or updated:
            print(f"  {message}")

        if updated:
            needs_update.append(directory)

    # Report results
    if args.check and needs_update:
        print(f"\n❌ {len(needs_update)} index files need updating")
        return 1
    elif needs_update and not args.write:
        print(
            f"\n⚠️  {len(needs_update)} index files need updating (use --write to update)"
        )
        return 0
    elif args.write and needs_update:
        print(f"\n✅ Updated {len(needs_update)} index files")
        return 0
    else:
        if args.verbose:
            print("\n✅ All index files are up to date")
        return 0


if __name__ == "__main__":
    sys.exit(main())
