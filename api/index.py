from http.server import BaseHTTPRequestHandler
import os
import sys

# Import the simple site generator
from simple_site import main as generate_site

# Run the site generation on startup
try:
    generate_site()
    print("Site generation completed successfully!")
except Exception as e:
    print(f"Error during site generation: {e}")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Site generation complete! The static site should be available.'.encode()) 