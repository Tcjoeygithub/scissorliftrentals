#!/bin/bash
# Script to regenerate the site and serve it locally on port 3000

echo "Regenerating site..."
python3 generate_site.py

echo "Starting local server on port 3000..."
python3 serve.py 