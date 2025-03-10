#!/usr/bin/env python3
"""
Script to update HTML files using templates.
This makes it easier to maintain common elements across all pages.
"""

import os
import re

def update_html_files(directory, header_template_path, footer_template_path):
    """Update all HTML files in the given directory and its subdirectories."""
    # Read the templates
    with open(header_template_path, 'r', encoding='utf-8') as f:
        header_template = f.read()
    
    with open(footer_template_path, 'r', encoding='utf-8') as f:
        footer_template = f.read()
    
    count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                updated = update_html_file(file_path, header_template, footer_template)
                if updated:
                    count += 1
    
    print(f"Updated {count} HTML files with templates.")

def update_html_file(file_path, header_template, footer_template):
    """Update a single HTML file with the templates."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Determine the relative path to the root
    depth = file_path.replace('output/', '').count('/')
    relative_path = '../' * depth if depth > 0 else ''
    
    # Replace placeholders in templates
    header = header_template.replace('{relative_path}', relative_path)
    footer = footer_template.replace('{relative_path}', relative_path)
    
    # Replace the head content
    head_pattern = r'<head>.*?</head>'
    title_meta_pattern = r'<title>.*?</title>(?:\s*<meta name="description" content=".*?">\s*)?'
    
    # Extract title and meta description
    title_meta_match = re.search(title_meta_pattern, content, re.DOTALL)
    title_meta = title_meta_match.group(0) if title_meta_match else '<title>Scissor Lifts for Rent</title>'
    
    # Create new head content
    new_head = f'<head>\n    {title_meta}\n    {header}\n</head>'
    
    # Replace the head
    new_content = re.sub(head_pattern, new_head, content, flags=re.DOTALL)
    
    # Replace the footer
    footer_pattern = r'<footer>.*?</footer>'
    new_content = re.sub(footer_pattern, footer, new_content, flags=re.DOTALL)
    
    # Check if the content was actually updated
    if new_content == content:
        return False
    
    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    """Main function."""
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
        print("Created templates directory.")
    
    # Check if template files exist
    header_template_path = 'templates/header.html'
    footer_template_path = 'templates/footer.html'
    
    if not os.path.exists(header_template_path) or not os.path.exists(footer_template_path):
        print("Template files not found. Please create them first.")
        return
    
    # Update HTML files
    update_html_files('output', header_template_path, footer_template_path)

if __name__ == '__main__':
    main() 