#!/usr/bin/env python3
"""
Simple HTTP server for testing the generated website locally.
Run this script and then open http://localhost:3000 in your browser.
"""

import http.server
import socketserver
import os
import webbrowser

# Change to the output directory
os.chdir('output')

# Set up the server
PORT = 3000
Handler = http.server.SimpleHTTPRequestHandler

# Open the browser
webbrowser.open(f'http://localhost:{PORT}')

# Start the server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped") 