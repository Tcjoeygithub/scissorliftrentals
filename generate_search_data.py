#!/usr/bin/env python3
"""
Script to generate search data for the scissor lift rental directory website.
This script reads the Excel file and creates a JSON file with city and zip code data
that can be used by the search functionality.
"""

import pandas as pd
import json
import os

def main():
    # Load the Excel file
    print("Loading Excel file...")
    df = pd.read_excel('scissor-lift-companies.xlsx')
    
    # Clean and prepare data
    print("Cleaning and preparing data...")
    df = df.fillna('')  # Replace NaN values with empty strings
    
    # Convert state names to lowercase abbreviations for URLs
    state_abbr = {
        'Alabama': 'al', 'Alaska': 'ak', 'Arizona': 'az', 'Arkansas': 'ar', 'California': 'ca',
        'Colorado': 'co', 'Connecticut': 'ct', 'Delaware': 'de', 'Florida': 'fl', 'Georgia': 'ga',
        'Hawaii': 'hi', 'Idaho': 'id', 'Illinois': 'il', 'Indiana': 'in', 'Iowa': 'ia',
        'Kansas': 'ks', 'Kentucky': 'ky', 'Louisiana': 'la', 'Maine': 'me', 'Maryland': 'md',
        'Massachusetts': 'ma', 'Michigan': 'mi', 'Minnesota': 'mn', 'Mississippi': 'ms', 'Missouri': 'mo',
        'Montana': 'mt', 'Nebraska': 'ne', 'Nevada': 'nv', 'New Hampshire': 'nh', 'New Jersey': 'nj',
        'New Mexico': 'nm', 'New York': 'ny', 'North Carolina': 'nc', 'North Dakota': 'nd', 'Ohio': 'oh',
        'Oklahoma': 'ok', 'Oregon': 'or', 'Pennsylvania': 'pa', 'Rhode Island': 'ri', 'South Carolina': 'sc',
        'South Dakota': 'sd', 'Tennessee': 'tn', 'Texas': 'tx', 'Utah': 'ut', 'Vermont': 'vt',
        'Virginia': 'va', 'Washington': 'wa', 'West Virginia': 'wv', 'Wisconsin': 'wi', 'Wyoming': 'wy',
        'District of Columbia': 'dc'
    }
    
    # Function to convert to URL-friendly slug
    def to_slug(text):
        if not text:
            return ''
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s-]', '', text)
        text = re.sub(r'\s+', '-', text)
        return text
    
    # Add slug columns for state and city
    df['state_slug'] = df['us_state'].apply(lambda x: state_abbr.get(x, to_slug(x)))
    df['city_slug'] = df['city'].apply(to_slug)
    
    # Create search data
    print("Generating search data...")
    search_data = {
        "cities": [],
        "zips": []
    }
    
    # Get states with companies
    states_with_companies = df[df['state_slug'] != ''][['us_state', 'state_slug']].drop_duplicates().sort_values('us_state')
    states_list = [(state, slug) for state, slug in zip(states_with_companies['us_state'], states_with_companies['state_slug'])]
    
    # Process all cities
    for state, state_slug in states_list:
        # Get cities in this state
        state_df = df[df['state_slug'] == state_slug]
        cities_with_companies = state_df[state_df['city_slug'] != ''][['city', 'city_slug']].drop_duplicates().sort_values('city')
        
        for city, city_slug in zip(cities_with_companies['city'], cities_with_companies['city_slug']):
            # Add city to search data
            search_data["cities"].append({
                "name": city,
                "state": state,
                "url": f"{state_slug}/{city_slug}/"
            })
            
            # Get zip codes for this city
            city_df = state_df[state_df['city_slug'] == city_slug]
            zip_codes = city_df['postal_code'].dropna().unique()
            
            for zip_code in zip_codes:
                if zip_code and str(zip_code).strip():
                    # Add zip code to search data
                    search_data["zips"].append({
                        "code": str(zip_code).strip(),
                        "city": city,
                        "state": state,
                        "url": f"{state_slug}/{city_slug}/"
                    })
    
    # Create output directory
    os.makedirs('output/assets/data', exist_ok=True)
    
    # Save search data to a JSON file
    with open('output/assets/data/search-data.json', 'w') as f:
        json.dump(search_data, f)
    
    print(f"Search data generated with {len(search_data['cities'])} cities and {len(search_data['zips'])} zip codes.")

if __name__ == "__main__":
    import re  # Import re here to avoid issues
    main() 