#!/usr/bin/env python3
"""Remove frontmatter metadata from all .knowledge markdown files."""

import re
from pathlib import Path


def remove_frontmatter():
    """Remove YAML frontmatter from markdown files."""
    knowledge_dir = Path('.knowledge')
    updated = 0
    
    for md_file in knowledge_dir.rglob('*.md'):
        try:
            # Read raw bytes
            raw_bytes = md_file.read_bytes()
            
            # Remove BOM if present (can be multiple)
            while raw_bytes.startswith(b'\xef\xbb\xbf'):
                raw_bytes = raw_bytes[3:]
            
            # Decode to string
            content = raw_bytes.decode('utf-8')
            
            # Check if starts with frontmatter
            stripped = content.lstrip()
            if stripped.startswith('---'):
                # Find the closing ---
                lines = stripped.split('\n')
                if lines[0].strip() == '---':
                    # Find second ---
                    end_idx = None
                    for i, line in enumerate(lines[1:], 1):
                        if line.strip() == '---':
                            end_idx = i
                            break
                    
                    if end_idx is not None:
                        # Remove frontmatter
                        new_lines = lines[end_idx + 1:]
                        new_content = '\n'.join(new_lines).lstrip()
                        
                        # Write back without BOM
                        md_file.write_text(new_content, encoding='utf-8')
                        updated += 1
                        if updated <= 25:
                            print(f'  Updated: {md_file}')
                            
        except Exception as e:
            print(f'  Error: {md_file} - {e}')
    
    print(f'\nTotal updated: {updated} files')


if __name__ == '__main__':
    remove_frontmatter()
