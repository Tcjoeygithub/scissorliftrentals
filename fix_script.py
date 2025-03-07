#!/usr/bin/env python3
"""
Script to modify generate_site_fixed.py by removing search functionality
"""

import re

# Read the original file
with open('generate_site_fixed.py', 'r') as f:
    content = f.read()

# Remove search-handler.js creation
content = re.sub(r'# Create a JavaScript file for search functionality.*?function handleSearch\(event\).*?addEventListener\(\'submit\', handleSearch\);.*?\'\'\'', '', content, flags=re.DOTALL)

# Remove search styles from CSS
content = re.sub(r'\.search-container \{.*?\.search-loading::after \{.*?}', '', content, flags=re.DOTALL)

# Replace homepage template with one without search
homepage_template = re.search(r'homepage_template = \'\'\'<!DOCTYPE html>.*?</html>\'\'\'', content, re.DOTALL).group(0)
homepage_template_no_search = re.sub(r'<div class="search-container">.*?<div id="search-loading" class="search-loading"></div>\s*</div>', '', homepage_template, flags=re.DOTALL)
content = content.replace(homepage_template, homepage_template_no_search)

# Remove search-handler.js script tag
content = re.sub(r'<script src="assets/js/search-handler.js"></script>', '', content)

# Remove search data generation code
content = re.sub(r'# Create search data for the search functionality.*?with open\(\'output/assets/data/search-data.json\', \'w\'\) as f:.*?json\.dump\(search_data, f\)', '', content, flags=re.DOTALL)

# Write the modified content to the file
with open('generate_site_fixed.py', 'w') as f:
    f.write(content)

print("Search functionality removed from generate_site_fixed.py") 