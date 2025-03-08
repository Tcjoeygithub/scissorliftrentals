#!/usr/bin/env python3
"""
Script to update all HTML files to use Leaflet instead of Google Maps.
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
    
    print(f"Updated {count} HTML files to use Leaflet instead of Google Maps.")

def update_html_file(file_path):
    """Update a single HTML file to use Leaflet instead of Google Maps."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if the file contains Google Maps API
    if 'maps.googleapis.com' not in content:
        return False
    
    # Replace Google Maps API with Leaflet
    new_content = re.sub(
        r'<!-- Google Maps API -->\s*<script src="https://maps.googleapis.com/maps/api/js\?key=[^"]+&callback=initMap" async defer></script>\s*<script src="../../assets/js/map-handler.js"></script>',
        '<!-- Leaflet Map -->\n'
        '    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>\n'
        '    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>\n'
        '    <script src="../../assets/js/leaflet-map-handler.js"></script>',
        content
    )
    
    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

if __name__ == '__main__':
    update_html_files('output') 