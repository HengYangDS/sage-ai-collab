#!/usr/bin/env python3
"""SAGE New File Creator.

Creates new files with correct placement and template.
Eliminates guesswork about where to put files and ensures consistent formatting.

Usage:
    python -m tools.dev_scripts.new_file adr "use-event-bus"
    python -m tools.dev_scripts.new_file convention "naming"
    python -m tools.dev_scripts.new_file practice "caching" --category engineering
    python -m tools.dev_scripts.new_file guide "getting-started"
"""

import re
import sys
from datetime import datetime
from pathlib import Path

# File type configurations
FILE_TYPES = {
    "adr": {
        "directory": ".context/decisions",
        "pattern": "ADR-{number:04d}-{name}.md",
        "template": "adr.md",
        "description": "Architecture Decision Record",
    },
    "convention": {
        "directory": ".context/conventions",
        "pattern": "{name}_convention.md",
        "template": "convention.md",
        "description": "Project convention document",
    },
    "practice": {
        "directory": ".knowledge/practices/{category}",
        "pattern": "{name}.md",
        "template": "practice.md",
        "description": "Generic practice/pattern document",
        "default_category": "engineering",
    },
    "guide": {
        "directory": "docs/guides",
        "pattern": "{name}.md",
        "template": "guide.md",
        "description": "User guide document",
    },
    "scenario": {
        "directory": ".knowledge/scenarios/{name}",
        "pattern": "context.md",
        "template": "scenario.md",
        "description": "Usage scenario documentation",
    },
    "framework": {
        "directory": ".knowledge/frameworks/{category}",
        "pattern": "{name}.md",
        "template": "framework.md",
        "description": "Framework documentation",
        "default_category": "patterns",
    },
}

# Templates directory
TEMPLATES_DIR = Path("templates")


def get_next_adr_number() -> int:
    """Get the next ADR number by scanning existing files."""
    decisions_dir = Path(".context/decisions")

    if not decisions_dir.exists():
        return 1

    max_num = 0
    for f in decisions_dir.glob("ADR-*.md"):
        match = re.match(r"ADR-(\d+)", f.name)
        if match:
            num = int(match.group(1))
            max_num = max(max_num, num)

    return max_num + 1


def normalize_name(name: str) -> str:
    """Normalize name for use in filenames."""
    # Convert to lowercase, replace spaces with hyphens
    normalized = name.lower().strip()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = normalized.strip("-")
    return normalized


def title_from_name(name: str) -> str:
    """Generate title from name."""
    return name.replace("-", " ").replace("_", " ").title()


def load_template(template_name: str) -> str:
    """Load template content or return default."""
    template_path = TEMPLATES_DIR / template_name

    if template_path.exists():
        return template_path.read_text(encoding="utf-8")

    # Default template
    return """# {TITLE}

> {PURPOSE}

---

## Overview

{CONTENT}

---

## Related

- [Related Document](path/to/doc.md)

---

*Part of SAGE Knowledge Base*
"""


def create_file(
    file_type: str,
    name: str,
    category: str | None = None,
    title: str | None = None,
    purpose: str | None = None,
) -> Path:
    """Create a new file with the appropriate template and location."""
    if file_type not in FILE_TYPES:
        raise ValueError(
            f"Unknown file type: {file_type}. Available: {', '.join(FILE_TYPES.keys())}"
        )

    config = FILE_TYPES[file_type]
    normalized_name = normalize_name(name)

    # Handle category
    if "{category}" in config["directory"]:
        if category is None:
            category = config.get("default_category", "general")
        category = normalize_name(category)

    # Build directory path
    directory = config["directory"]
    if "{category}" in directory:
        directory = directory.format(category=category)
    if "{name}" in directory:
        directory = directory.format(name=normalized_name)

    dir_path = Path(directory)

    # Build filename
    filename = config["pattern"]
    if "{number}" in filename:
        number = get_next_adr_number()
        filename = filename.format(number=number, name=normalized_name)
    else:
        filename = filename.format(name=normalized_name)

    file_path = dir_path / filename

    # Check if file exists
    if file_path.exists():
        raise FileExistsError(f"File already exists: {file_path}")

    # Create directory if needed
    dir_path.mkdir(parents=True, exist_ok=True)

    # Load and fill template
    template = load_template(config["template"])

    # Generate default values
    if title is None:
        title = title_from_name(name)
    if purpose is None:
        purpose = f"{config['description']} for {title}"

    # Fill template
    content = template.format(
        TITLE=title,
        PURPOSE=purpose,
        CONTENT="TODO: Add content here",
        DATE=datetime.now().strftime("%Y-%m-%d"),
        NAME=name,
        CATEGORY=category or "",
    )

    # Write file
    file_path.write_text(content, encoding="utf-8")

    return file_path


def main() -> int:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Create new SAGE files with correct placement and template",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
File types:
  adr         Architecture Decision Record (.context/decisions/)
  convention  Project convention (.context/conventions/)
  practice    Generic practice/pattern (.knowledge/practices/)
  guide       User guide (docs/guides/)
  scenario    Usage scenario (.knowledge/scenarios/)
  framework   Framework documentation (.knowledge/frameworks/)

Examples:
  %(prog)s adr "use-event-bus"
  %(prog)s convention "naming"
  %(prog)s practice "caching" --category engineering
  %(prog)s guide "getting-started"
""",
    )

    parser.add_argument(
        "type", choices=FILE_TYPES.keys(), help="Type of file to create"
    )
    parser.add_argument("name", help="Name for the new file")
    parser.add_argument(
        "--category", "-c", help="Category (for practice/framework types)"
    )
    parser.add_argument(
        "--title", "-t", help="Custom title (default: derived from name)"
    )
    parser.add_argument("--purpose", "-p", help="Custom purpose description")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without creating",
    )

    args = parser.parse_args()

    try:
        if args.dry_run:
            config = FILE_TYPES[args.type]
            normalized_name = normalize_name(args.name)
            category = args.category or config.get("default_category", "general")

            directory = config["directory"]
            if "{category}" in directory:
                directory = directory.format(category=normalize_name(category))
            if "{name}" in directory:
                directory = directory.format(name=normalized_name)

            filename = config["pattern"]
            if "{number}" in filename:
                filename = filename.format(
                    number=get_next_adr_number(), name=normalized_name
                )
            else:
                filename = filename.format(name=normalized_name)

            print(f"Would create: {directory}/{filename}")
            print(f"  Type: {config['description']}")
            print(f"  Template: {config['template']}")
            return 0

        file_path = create_file(
            file_type=args.type,
            name=args.name,
            category=args.category,
            title=args.title,
            purpose=args.purpose,
        )

        print(f"✅ Created: {file_path}")
        print(f"   Type: {FILE_TYPES[args.type]['description']}")
        return 0

    except FileExistsError as e:
        print(f"❌ Error: {e}")
        return 1
    except ValueError as e:
        print(f"❌ Error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
