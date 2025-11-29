#!/usr/bin/env python3
"""
Add YAML front matter metadata to markdown files missing it.
"""

from pathlib import Path
from datetime import date

METADATA_TEMPLATE = '''---
version: "1.0"
last_updated: "{date}"
status: published
tokens: ~500
---

'''

def add_metadata():
    """Add YAML front matter to files missing it."""
    kb_path = Path(__file__).parent.parent / ".knowledge"
    today = date.today().isoformat()
    
    added = 0
    skipped = 0
    
    for md_file in kb_path.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8", errors="ignore")
        
        if content.startswith("---"):
            skipped += 1
            continue
        
        # Add metadata
        new_content = METADATA_TEMPLATE.format(date=today) + content
        md_file.write_text(new_content, encoding="utf-8")
        print(f"[ADDED] {md_file.relative_to(kb_path.parent)}")
        added += 1
    
    print()
    print(f"Summary: Added metadata to {added} files, skipped {skipped} files")

if __name__ == "__main__":
    add_metadata()
