#!/usr/bin/env python3
"""SAGE Pre-Push Hook.

Generates session summary before push based on tracked commits.
Creates conversation/handoff records automatically when needed.

Usage:
    Called automatically by git pre-push hook, or manually:
    python -m tools.hooks.pre_push
"""

import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

# Session tracking
SESSION_FILE = Path(".history/current/session.json")
CONVERSATIONS_DIR = Path(".history/conversations")
HANDOFFS_DIR = Path(".history/handoffs")


def load_session() -> dict | None:
    """Load current session data."""
    if not SESSION_FILE.exists():
        return None

    try:
        return json.loads(SESSION_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def extract_topic(commits: list[dict]) -> str:
    """Extract main topic from commit messages."""
    # Try to find conventional commit scope: feat(scope), fix(scope), etc.
    scopes = []
    for c in commits:
        msg = c.get("message", "")
        match = re.match(r"^\w+\(([^)]+)\)", msg)
        if match:
            scopes.append(match.group(1))

    if scopes:
        # Return most common scope
        return Counter(scopes).most_common(1)[0][0]

    # Try to extract from first significant commit
    for c in commits:
        msg = c.get("message", "")
        # Remove conventional commit prefix
        clean_msg = re.sub(r"^\w+(\([^)]+\))?:\s*", "", msg)
        # Take first few words
        words = clean_msg.split()[:3]
        if words:
            return "-".join(words).lower()

    return "session"


def generate_summary(commits: list[dict]) -> str:
    """Generate summary from commit messages."""
    # Group by type
    by_type = {
        "feat": [],
        "fix": [],
        "docs": [],
        "refactor": [],
        "test": [],
        "chore": [],
        "other": [],
    }

    for c in commits:
        msg = c.get("message", "")
        categorized = False
        for commit_type in by_type:
            if commit_type != "other" and msg.lower().startswith(commit_type):
                by_type[commit_type].append(msg)
                categorized = True
                break
        if not categorized:
            by_type["other"].append(msg)

    # Generate summary lines
    lines = []
    type_labels = {
        "feat": "New features",
        "fix": "Bug fixes",
        "docs": "Documentation",
        "refactor": "Refactoring",
        "test": "Tests",
        "chore": "Maintenance",
        "other": "Other changes",
    }

    for commit_type, label in type_labels.items():
        if by_type[commit_type]:
            lines.append(f"- {label}: {len(by_type[commit_type])}")

    return "\n".join(lines) if lines else "General development work."


def generate_record_content(session: dict, record_type: str) -> str:
    """Generate content for session record."""
    commits = session.get("commits", [])
    files = session.get("files", [])
    date = session.get("date", datetime.now().strftime("%Y-%m-%d"))
    topic = extract_topic(commits)

    # Title based on type
    if record_type == "INCOMPLETE":
        title = f"{topic.title()} - Handoff"
    else:
        title = f"{topic.replace('-', ' ').title()} - {date}"

    # Build content
    content = f"""# {title}

## Context

Work session on {date} with {len(commits)} commits.

## Changes

### Commits

"""

    for c in commits:
        content += f"- `{c.get('hash', '?')}` {c.get('message', 'No message')}\n"

    content += f"""
### Files Modified ({len(files)} files)

"""

    # Show first 20 files
    for f in files[:20]:
        content += f"- {f}\n"

    if len(files) > 20:
        content += f"- ... and {len(files) - 20} more files\n"

    content += f"""
## Summary

{generate_summary(commits)}

"""

    # Add next steps for handoff
    if record_type == "INCOMPLETE":
        content += """## Next Steps

- [ ] TODO: Continue work on this task
- [ ] TODO: Review and test changes

## Handoff Notes

TODO: Add any important context for the next session.

"""

    content += """---

*Auto-generated from Git activity*
*Part of SAGE Knowledge Base*
"""

    return content


def create_record(session: dict) -> Path | None:
    """Create session record if needed."""
    suggested_type = session.get("suggested_type", "ROUTINE")

    if suggested_type == "ROUTINE":
        return None

    date = session.get("date", datetime.now().strftime("%Y-%m-%d"))
    topic = extract_topic(session.get("commits", []))

    # Normalize topic for filename
    topic_slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")

    # Determine target directory and filename
    if suggested_type == "INCOMPLETE":
        target_dir = HANDOFFS_DIR
        filename = f"{date}-{topic_slug}-handoff.md"
    else:
        target_dir = CONVERSATIONS_DIR
        filename = f"{date}-{topic_slug}.md"

    target_path = target_dir / filename

    # Don't overwrite existing records
    if target_path.exists():
        return None

    # Create directory if needed
    target_dir.mkdir(parents=True, exist_ok=True)

    # Generate and save content
    content = generate_record_content(session, suggested_type)
    target_path.write_text(content, encoding="utf-8")

    return target_path


def cleanup_session() -> None:
    """Clean up session file after processing."""
    if SESSION_FILE.exists():
        SESSION_FILE.unlink()


def main() -> int:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate session summary before push")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without doing it",
    )
    parser.add_argument(
        "--no-cleanup", action="store_true", help="Keep session file after processing"
    )
    args = parser.parse_args()

    # Load session
    session = load_session()

    if not session:
        print("ℹ️  No active session to process")
        return 0

    commits = session.get("commits", [])
    suggested_type = session.get("suggested_type", "ROUTINE")

    print(f"📊 Session: {len(commits)} commits, type: {suggested_type}")

    if suggested_type == "ROUTINE":
        print("ℹ️  Routine session - no record needed")
        if not args.no_cleanup:
            cleanup_session()
        return 0

    if args.dry_run:
        topic = extract_topic(commits)
        date = session.get("date", datetime.now().strftime("%Y-%m-%d"))
        if suggested_type == "INCOMPLETE":
            print(f"Would create: {HANDOFFS_DIR}/{date}-{topic}-handoff.md")
        else:
            print(f"Would create: {CONVERSATIONS_DIR}/{date}-{topic}.md")
        return 0

    # Create record
    record_path = create_record(session)

    if record_path:
        print(f"✅ Created session record: {record_path}")
    else:
        print("ℹ️  Record already exists or not needed")

    # Cleanup
    if not args.no_cleanup:
        cleanup_session()
        print("🧹 Session file cleaned up")

    return 0


if __name__ == "__main__":
    sys.exit(main())
