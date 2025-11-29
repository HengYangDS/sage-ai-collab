#!/usr/bin/env python3
"""
Batch add YAML front matter metadata to markdown files.
Usage: python scripts/add_metadata.py
"""

import re
from pathlib import Path
from datetime import date

KNOWLEDGE_DIR = Path(__file__).parent.parent / ".knowledge"
TODAY = date.today().strftime("%Y-%m-%d")

def estimate_tokens(content: str) -> int:
    """Estimate token count (~4 chars per token for English)."""
    return len(content) // 4

def get_status(file_path: Path) -> str:
    """Determine status based on path."""
    path_str = str(file_path)
    if "core" in path_str or "index.md" in path_str:
        return "published"
    return "published"

def add_metadata(file_path: Path) -> bool:
    """Add metadata to file if missing. Returns True if modified."""
    try:
        content = file_path.read_text(encoding='utf-8')
        if content.startswith("---"):
            return False  # Already has metadata
        
        tokens = estimate_tokens(content)
        token_str = f"~{(tokens // 50) * 50}" if tokens > 100 else "~100"
        status = get_status(file_path)
        
        metadata = f'''---
version: "1.0"
last_updated: "{TODAY}"
status: {status}
tokens: {token_str}
---

'''
        new_content = metadata + content
        file_path.write_text(new_content, encoding='utf-8')
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    print("=" * 60)
    print("Adding metadata to markdown files")
    print("=" * 60)
    
    md_files = list(KNOWLEDGE_DIR.rglob("*.md"))
    modified = 0
    skipped = 0
    
    for file_path in md_files:
        rel_path = file_path.relative_to(KNOWLEDGE_DIR.parent)
        if add_metadata(file_path):
            print(f"  + {rel_path}")
            modified += 1
        else:
            skipped += 1
    
    print("\n" + "=" * 60)
    print(f"Summary: {modified} modified, {skipped} skipped (already had metadata)")
    print("=" * 60)

if __name__ == "__main__":
    main()
