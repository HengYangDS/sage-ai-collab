#!/usr/bin/env python3
"""SAGE Document Format Validator.

Validates that Markdown documents follow SAGE formatting standards:
- Standard header: # Title + > purpose + ---
- Standard footer: *Part of SAGE Knowledge Base*
- TOC required for documents > 60 lines
"""

import re
import sys
from pathlib import Path

# Patterns for validation
HEADER_PATTERN = re.compile(r"^# .+\n\n> .+\n\n---", re.MULTILINE)
FOOTER_PATTERN = re.compile(r"\*Part of SAGE Knowledge Base\*\s*$")
TOC_PATTERN = re.compile(r"\[.*\]\(#.*\)")

# Directories to validate
CONTENT_DIRS = ["content", "docs", ".context"]

# Files/patterns to skip
SKIP_PATTERNS = [
    r"^_",  # Files starting with underscore (templates/examples)
    r"index\.md$",  # Index files (auto-generated)
    r"CHANGELOG\.md$",
    r"README\.md$",
    r"CONTRIBUTING\.md$",
]


def should_skip(file_path: Path) -> bool:
    """Check if file should be skipped."""
    name = file_path.name
    for pattern in SKIP_PATTERNS:
        if re.search(pattern, name):
            return True
    return False


def validate_file(file_path: Path) -> list[str]:
    """Validate a single file and return list of errors."""
    errors = []

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return [f"{file_path}: Cannot read file - {e}"]

    # Check header
    if not HEADER_PATTERN.match(content):
        errors.append(
            f"{file_path}: Missing standard header (# Title + > purpose + ---)"
        )

    # Check footer
    if not FOOTER_PATTERN.search(content):
        errors.append(
            f"{file_path}: Missing standard footer (*Part of SAGE Knowledge Base*)"
        )

    # Check TOC for long documents
    line_count = content.count("\n")
    h2_count = len(re.findall(r"^## ", content, re.MULTILINE))

    if (line_count > 60 or h2_count > 3) and not TOC_PATTERN.search(content):
        errors.append(
            f"{file_path}: Document with {line_count} lines and {h2_count} sections needs TOC"
        )

    return errors


def get_files_to_validate() -> list[Path]:
    """Get list of Markdown files to validate."""
    files = []

    for dir_name in CONTENT_DIRS:
        dir_path = Path(dir_name)
        if dir_path.exists():
            for md_file in dir_path.rglob("*.md"):
                if not should_skip(md_file):
                    files.append(md_file)

    return files


def main() -> int:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Validate SAGE document format")
    parser.add_argument("files", nargs="*", help="Specific files to validate")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    # Get files to validate
    if args.files:
        files = [Path(f) for f in args.files if f.endswith(".md")]
    else:
        files = get_files_to_validate()

    if args.verbose:
        print(f"Validating {len(files)} files...")

    # Validate all files
    all_errors = []
    for file_path in files:
        if not should_skip(file_path):
            errors = validate_file(file_path)
            all_errors.extend(errors)

    # Report results
    if all_errors:
        print("❌ Document format validation failed:")
        for error in all_errors:
            print(f"  {error}")
        return 1
    else:
        if args.verbose:
            print(f"✅ All {len(files)} documents passed format validation")
        return 0


if __name__ == "__main__":
    sys.exit(main())
