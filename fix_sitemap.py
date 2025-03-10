#!/usr/bin/env python3
"""
Script to fix the sitemap.xml file by updating the domain and removing extra slashes.
"""

import re
import os
from datetime import datetime

def fix_sitemap(sitemap_path):
    """Fix the sitemap.xml file by updating the domain and removing extra slashes."""
    # Read the current sitemap
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the domain and fix the URLs by removing extra slashes
    fixed_content = re.sub(
        r'<loc>https://scissorliftrentals\.com/+', 
        '<loc>https://www.scissorliftsforrent.com/', 
        content
    )
    
    # Update the lastmod date to today
    today = datetime.now().strftime('%Y-%m-%d')
    fixed_content = re.sub(r'<lastmod>.*?</lastmod>', f'<lastmod>{today}</lastmod>', fixed_content)
    
    # Write the fixed sitemap
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"Fixed sitemap at {sitemap_path}")
    
    # Count the number of URLs in the sitemap
    url_count = fixed_content.count('<url>')
    print(f"Sitemap contains {url_count} URLs")

if __name__ == '__main__':
    sitemap_path = 'output/sitemap.xml'
    if os.path.exists(sitemap_path):
        fix_sitemap(sitemap_path)
    else:
        print(f"Sitemap not found at {sitemap_path}") 