#!/usr/bin/env python3
"""
Script to update all HTML files with the new footer links.
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
    
    print(f"Updated {count} HTML files with new footer links.")

def update_html_file(file_path):
    """Update a single HTML file with the new footer links."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if the file already has the new footer links
    if '<div class="footer-links">' in content:
        return False
    
    # Determine the relative path to the root
    depth = file_path.replace('output/', '').count('/')
    relative_path = '../' * depth if depth > 0 else ''
    
    # Replace the old footer with the new one
    old_footer_pattern = r'<footer>\s*<div class="footer-content">\s*<p>&copy; 2025 Scissor Lift Rental Directory\. All rights reserved\.</p>\s*(?:<p><a href="[^"]*">Sitemap</a></p>)?\s*</div>\s*</footer>'
    
    new_footer = f'''<footer>
    <div class="footer-content">
        <p>&copy; 2025 Scissor Lift Rental Directory. All rights reserved.</p>
        <div class="footer-links">
            <a href="{relative_path}privacy-policy.html">Privacy Policy</a>
            <a href="{relative_path}terms-of-service.html">Terms of Service</a>
            <a href="{relative_path}about-us.html">About Us</a>
            <a href="{relative_path}contact-us.html">Contact Us</a>
            <a href="{relative_path}sitemap.xml">Sitemap</a>
        </div>
    </div>
</footer>'''
    
    new_content = re.sub(old_footer_pattern, new_footer, content)
    
    # Check if the content was actually updated
    if new_content == content:
        return False
    
    # Add the page-styles.css link to the head if it doesn't exist
    if 'page-styles.css' not in new_content:
        head_end_tag = '</head>'
        css_link = f'    <link rel="stylesheet" href="{relative_path}assets/css/page-styles.css">\n    '
        new_content = new_content.replace(head_end_tag, css_link + head_end_tag)
    
    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

if __name__ == '__main__':
    update_html_files('output') 