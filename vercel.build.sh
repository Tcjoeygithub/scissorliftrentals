#!/bin/bash
# Install dependencies
pip install -r requirements.txt

# Run the site generator
python generate_site_vercel.py

# Print success message
echo "Site generation complete!" 