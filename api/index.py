from http.server import BaseHTTPRequestHandler
import os
import sys
import importlib.util

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the generate_site_vercel module
spec = importlib.util.spec_from_file_location("generate_site_vercel", "../generate_site_vercel.py")
generate_site_vercel = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate_site_vercel)

# Run the site generation on startup
generate_site_vercel.main()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Site generation complete! The static site should be available.'.encode()) 