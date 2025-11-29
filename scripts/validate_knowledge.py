#!/usr/bin/env python3
"""
SAGE Knowledge Base Validation Script

Validates .knowledge directory for:
- Broken internal links
- Missing YAML front matter metadata
- File length warnings (>300 lines)
"""

import os
import re
from pathlib import Path

def validate_knowledge_base():
    """Run validation checks on .knowledge directory."""
    kb_path = Path(__file__).parent.parent / ".knowledge"
    
    if not kb_path.exists():
        print(f"[ERROR] Knowledge base not found: {kb_path}")
        return 1
    
    print("=" * 60)
    print("SAGE Knowledge Base Validation")
    print("=" * 60)
    
    errors = []
    warnings = []
    md_files = list(kb_path.rglob("*.md"))
    
    print(f"[INFO] Found {len(md_files)} markdown files")
    
    for md_file in md_files:
        rel_path = md_file.relative_to(kb_path.parent)
        content = md_file.read_text(encoding="utf-8", errors="ignore")
        lines = content.split("\n")
        
        # Check 1: YAML front matter
        if not content.startswith("---"):
            warnings.append(f"[WARN] Missing YAML front matter: {rel_path}")
        
        # Check 2: File length
        if len(lines) > 300:
            warnings.append(f"[WARN] File exceeds 300 lines ({len(lines)}): {rel_path}")
        
        # Check 3: Internal links
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+\.md)\)')
        for match in link_pattern.finditer(content):
            link_path = match.group(2)
            
            # Skip external links
            if link_path.startswith("http"):
                continue
            
            # Resolve link path
            if link_path.startswith(".knowledge/") or link_path.startswith(".context/") or link_path.startswith(".junie/"):
                target = kb_path.parent / link_path
            elif link_path.startswith("./"):
                target = md_file.parent / link_path[2:]
            elif link_path.startswith("../"):
                target = md_file.parent / link_path
            else:
                target = md_file.parent / link_path
            
            target = target.resolve()
            if not target.exists():
                errors.append(f"[ERROR] Broken link in {rel_path}: {link_path}")
    
    # Print results
    print()
    for err in errors:
        print(err)
    for warn in warnings:
        print(warn)
    
    print()
    print("=" * 60)
    print(f"Summary: {len(errors)} errors, {len(warnings)} warnings")
    print("=" * 60)
    
    return 1 if errors else 0

if __name__ == "__main__":
    exit(validate_knowledge_base())
