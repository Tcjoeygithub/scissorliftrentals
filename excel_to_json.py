#!/usr/bin/env python3
"""
Convert the scissor lift companies Excel file to JSON format.
This makes the data more accessible for web applications and easier to version control.
"""

import pandas as pd
import json
import os

def excel_to_json():
    """Convert the Excel file to JSON format."""
    print("Converting Excel file to JSON...")
    
    # Load the Excel file
    df = pd.read_excel('scissor-lift-companies.xlsx')
    
    # Clean the data
    df = df.fillna('')
    
    # Convert to dictionary format
    companies = []
    for _, row in df.iterrows():
        company = {
            'name': row['name'] if 'name' in row else '',
            'site': row['site'] if 'site' in row else '',
            'scissor_lifts': row['Scissor Lifts'] if 'Scissor Lifts' in row else '',
            'scissor_lift_brands': row['Scissor Lift Brands'] if 'Scissor Lift Brands' in row else '',
            'sizes_available': row['Sizes Available'] if 'Sizes Available' in row else '',
            'phone': row['phone'] if 'phone' in row else '',
            'full_address': row['full_address'] if 'full_address' in row else '',
            'city': row['city'] if 'city' in row else '',
            'us_state': row['us_state'] if 'us_state' in row else '',
            'postal_code': str(row['postal_code']) if 'postal_code' in row and pd.notna(row['postal_code']) else '',
            'reviews': row['reviews'] if 'reviews' in row and pd.notna(row['reviews']) else 0,
            'reviews_num': row['reviews_num'] if 'reviews_num' in row and pd.notna(row['reviews_num']) else 0,
            'working_hours': row['working_hours'] if 'working_hours' in row else '',
            'about': row['about'] if 'about' in row else '',
            'latitude': float(row['latitude']) if 'latitude' in row and pd.notna(row['latitude']) else None,
            'longitude': float(row['longitude']) if 'longitude' in row and pd.notna(row['longitude']) else None,
            'state_slug': row['state_slug'] if 'state_slug' in row else '',
            'city_slug': row['city_slug'] if 'city_slug' in row else ''
        }
        companies.append(company)
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Write to JSON file
    with open('data/scissor-lift-companies.json', 'w') as f:
        json.dump(companies, f, indent=2)
    
    print(f"Conversion complete! JSON file created with {len(companies)} companies.")
    print("File saved to: data/scissor-lift-companies.json")

if __name__ == "__main__":
    excel_to_json() 