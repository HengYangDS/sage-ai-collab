#!/usr/bin/env python3
"""SAGE Post-Commit Hook.

Tracks session activity after each commit.
Updates session.json with commit information for later summary generation.

Usage:
    Called automatically by git post-commit hook, or manually:
    python -m tools.hooks.post_commit
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Session tracking file
SESSION_DIR = Path(".history/current")
SESSION_FILE = SESSION_DIR / "session.json"


def get_commit_info() -> dict:
    """Get information about the last commit."""
    try:
        commit_hash = (
            subprocess.check_output(
                ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()[:8]
        )

        commit_msg = (
            subprocess.check_output(
                ["git", "log", "-1", "--pretty=%s"], stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()
        )

        changed_files = (
            subprocess.check_output(
                ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"],
                stderr=subprocess.DEVNULL,
            )
            .decode()
            .strip()
            .split("\n")
        )

        # Filter empty strings
        changed_files = [f for f in changed_files if f]

        return {
            "hash": commit_hash,
            "message": commit_msg,
            "files": changed_files,
            "timestamp": datetime.now().isoformat(),
        }
    except subprocess.CalledProcessError:
        return None
    except FileNotFoundError:
        # Git not available
        return None


def load_session() -> dict:
    """Load existing session or create new one."""
    if SESSION_FILE.exists():
        try:
            return json.loads(SESSION_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            pass

    # Create new session
    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "started": datetime.now().isoformat(),
        "commits": [],
        "files": [],
    }


def save_session(session: dict) -> None:
    """Save session to file."""
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    SESSION_FILE.write_text(
        json.dumps(session, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def detect_session_type(session: dict) -> str:
    """Detect session type based on activity.

    Returns:
        SIGNIFICANT - Major work, needs conversation record
        INCOMPLETE - Work in progress, needs handoff
        ROUTINE - Minor changes, no record needed
        EXPLORATION - Research/exploration, needs session state
    """
    commits = session.get("commits", [])

    if not commits:
        return "ROUTINE"

    # Check for WIP indicators
    has_wip = any(
        "wip" in c.get("message", "").lower()
        or "work in progress" in c.get("message", "").lower()
        for c in commits
    )

    if has_wip:
        return "INCOMPLETE"

    # Check commit count
    if len(commits) >= 5:
        return "SIGNIFICANT"

    # Check for significant commit types
    significant_types = ["feat", "fix", "refactor", "perf"]
    has_significant = any(
        any(c.get("message", "").lower().startswith(t) for t in significant_types)
        for c in commits
    )

    if has_significant and len(commits) >= 3:
        return "SIGNIFICANT"

    if len(commits) <= 2:
        return "ROUTINE"

    return "EXPLORATION"


def update_session() -> None:
    """Update session with latest commit."""
    commit_info = get_commit_info()

    if not commit_info:
        return

    # Load or create session
    session = load_session()

    # Check if this is a new day
    today = datetime.now().strftime("%Y-%m-%d")
    if session.get("date") != today:
        # Start fresh session for new day
        session = {
            "date": today,
            "started": datetime.now().isoformat(),
            "commits": [],
            "files": [],
        }

    # Add commit
    session["commits"].append(
        {
            "hash": commit_info["hash"],
            "message": commit_info["message"],
            "timestamp": commit_info["timestamp"],
        }
    )

    # Update files list (unique)
    existing_files = set(session.get("files", []))
    existing_files.update(commit_info["files"])
    session["files"] = sorted(existing_files)

    # Update metadata
    session["last_update"] = datetime.now().isoformat()
    session["suggested_type"] = detect_session_type(session)

    # Save
    save_session(session)

    print(
        f"📝 Session updated: {len(session['commits'])} commits, type: {session['suggested_type']}"
    )


def main() -> int:
    """Main entry point."""
    try:
        update_session()
        return 0
    except Exception as e:
        print(f"⚠️ Session tracking error: {e}", file=sys.stderr)
        return 0  # Don't fail the commit


if __name__ == "__main__":
    sys.exit(main())
