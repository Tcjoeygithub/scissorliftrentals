#!/usr/bin/env python3
"""
Script to add Bing verification meta tag to all HTML files.
"""

import os
import re

def update_html_files(directory):
    """Update all HTML files in the given directory and its subdirectories."""
    count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                updated = update_html_file(file_path)
                if updated:
                    count += 1
    
    print(f"Added Bing verification meta tag to {count} HTML files.")

def update_html_file(file_path):
    """Add Bing verification meta tag to a single HTML file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if the file already has the Bing verification meta tag
    if 'msvalidate.01' in content:
        return False
    
    # Add the Bing verification meta tag after the viewport meta tag
    viewport_pattern = r'<meta name="viewport" content="[^"]*">'
    bing_meta = '<meta name="msvalidate.01" content="22BBEF395E3FC6F1DD27ECE4914235FB" />'
    
    new_content = re.sub(
        viewport_pattern,
        lambda m: m.group(0) + '\n    ' + bing_meta,
        content
    )
    
    # Check if the content was actually updated
    if new_content == content:
        return False
    
    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

if __name__ == '__main__':
    update_html_files('output') 