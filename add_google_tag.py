#!/usr/bin/env python3
"""
Script to add Google Analytics tag to all HTML files.
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
    
    print(f"Added Google Analytics tag to {count} HTML files.")

def update_html_file(file_path):
    """Add Google Analytics tag to a single HTML file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if the file already has the Google Analytics tag
    if 'G-MLHRR9XW0J' in content:
        return False
    
    # Google Analytics tag to add
    google_tag = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-MLHRR9XW0J"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-MLHRR9XW0J');
</script>'''
    
    # Add the Google Analytics tag before the closing head tag
    head_end_tag = '</head>'
    new_content = content.replace(head_end_tag, google_tag + '\n' + head_end_tag)
    
    # Check if the content was actually updated
    if new_content == content:
        return False
    
    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

if __name__ == '__main__':
    update_html_files('output') 