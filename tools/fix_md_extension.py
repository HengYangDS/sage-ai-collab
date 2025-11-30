#!/usr/bin/env python3
"""Fix .MD extensions to .md in all markdown file references."""

import os
import re


def fix_md_extensions():
    """Replace .MD with .md in all markdown files."""
    # Get all .md files
    md_files = []
    for root, dirs, files in os.walk('.'):
        # Skip .git directory
        if '.git' in root:
            continue
        for f in files:
            if f.endswith('.md'):
                md_files.append(os.path.join(root, f))

    print(f'Found {len(md_files)} .md files')

    # Batch replace .MD references with .md
    updated_files = 0
    total_replacements = 0

    # Pattern to match .MD at end of words (file references)
    pattern = r'\.MD(?=[\s\)\]\"\'\`\,\;\:\|\#]|$)'

    for filepath in md_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Count matches before replacement
            matches = re.findall(pattern, content)
            
            if matches:
                # Replace .MD with .md
                new_content = re.sub(pattern, '.md', content)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                total_replacements += len(matches)
                updated_files += 1
                
        except Exception as e:
            print(f'Error: {filepath} -> {e}')

    print(f'Updated {updated_files} files')
    print(f'Total replacements: {total_replacements}')


if __name__ == '__main__':
    fix_md_extensions()
