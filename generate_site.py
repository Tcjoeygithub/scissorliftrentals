import pandas as pd
import os
import re
import json
import requests
import statistics
import random
from urllib.parse import urlparse, unquote
from jinja2 import Environment, FileSystemLoader
import shutil

# Function to generate unique SEO-optimized descriptions for states
def generate_state_description(state):
    # LSI keywords and N-grams related to scissor lift rentals
    lsi_keywords = [
        "aerial work platforms", "elevated work platforms", "construction equipment rental",
        "industrial equipment", "maintenance equipment", "height access solutions",
        "lifting equipment", "mobile elevating work platforms", "MEWP rentals",
        "commercial construction equipment", "industrial machinery"
    ]
    
    # Randomly select 3-4 LSI keywords to include
    selected_keywords = random.sample(lsi_keywords, random.randint(3, 4))
    
    # Create a unique description for each state
    descriptions = [
        f"{state} offers a comprehensive selection of scissor lift rentals and {selected_keywords[0]} for construction, maintenance, and industrial projects. Whether you need equipment for indoor applications or {selected_keywords[1]} for outdoor construction sites, rental companies throughout {state} provide reliable solutions with flexible rental terms.",
        
        f"Finding quality scissor lift rentals in {state} is simple with numerous providers offering {selected_keywords[0]} and {selected_keywords[1]}. Construction professionals and maintenance crews across {state} rely on these versatile machines for safe and efficient elevated work access.",
        
        f"Contractors and facility managers in {state} can access a wide range of scissor lift rentals and {selected_keywords[0]} from reputable providers. These {selected_keywords[1]} are essential for projects requiring safe access to elevated work areas in commercial, industrial, and institutional settings.",
        
        f"{state}'s construction and maintenance industries are well-served by local companies offering scissor lift rentals and other {selected_keywords[0]}. These {selected_keywords[1]} provide safe and stable platforms for workers needing to reach heights efficiently.",
        
        f"The {selected_keywords[0]} market in {state} includes numerous options for scissor lift rentals suited to various applications. From {selected_keywords[1]} to specialized equipment for unique projects, {state}'s rental providers offer comprehensive solutions for height access needs."
    ]
    
    # Select a random description template and add safety information
    description = random.choice(descriptions)
    
    # Add information about popular brands
    brands = ["JLG", "Genie", "Skyjack", "Haulotte", "Snorkel"]
    random.shuffle(brands)
    top_brands = brands[:3]  # Select 3 random brands
    
    description += f" Popular scissor lift brands available in {state} include {', '.join(top_brands)}, offering various platform heights, weight capacities, and power options to suit specific project requirements."
    
    return description

# Function to generate unique SEO-optimized descriptions for cities
def generate_city_description(city, state):
    # LSI keywords and N-grams related to scissor lift rentals in cities
    lsi_keywords = [
        "aerial equipment rental", "construction lift rental", "industrial lift equipment",
        "scissor platform rental", "elevated work access", "commercial lift solutions",
        "height access equipment", "construction machinery rental", "industrial access platforms",
        "building maintenance equipment", "contractor equipment rental"
    ]
    
    # Randomly select 3-4 LSI keywords to include
    selected_keywords = random.sample(lsi_keywords, random.randint(3, 4))
    
    # Create a unique description for each city
    descriptions = [
        f"Contractors and businesses in {city}, {state} have access to premium scissor lift rentals and {selected_keywords[0]} from local providers. These {selected_keywords[1]} are essential for construction, maintenance, and renovation projects requiring safe and efficient access to elevated work areas.",
        
        f"{city}, {state} offers numerous options for scissor lift rentals and {selected_keywords[0]} to support local construction and maintenance industries. Companies in {city} provide {selected_keywords[1]} with various platform heights and weight capacities to accommodate different project requirements.",
        
        f"Finding reliable scissor lift rentals in {city}, {state} is straightforward with several local companies offering {selected_keywords[0]} and {selected_keywords[1]}. These versatile machines help contractors and maintenance teams work safely and efficiently at height.",
        
        f"The {selected_keywords[0]} market in {city}, {state} includes multiple providers offering scissor lift rentals for commercial, industrial, and institutional applications. These {selected_keywords[1]} are crucial for projects requiring stable elevated work platforms.",
        
        f"Businesses and contractors in {city}, {state} rely on local scissor lift rentals and {selected_keywords[0]} for safe access to elevated work areas. The {selected_keywords[1]} available in {city} include various models suited to both indoor and outdoor applications."
    ]
    
    # Select a random description template
    description = random.choice(descriptions)
    
    # Add rental advice specific to the city
    rental_advice = [
        f"When renting scissor lifts in {city}, consider factors such as project duration, required working height, and whether you need an electric model for indoor use or a rough terrain unit for outdoor applications.",
        
        f"For optimal results when renting scissor lifts in {city}, be sure to specify your project requirements including working height, platform capacity, and whether you need indoor or outdoor capabilities.",
        
        f"Rental companies in {city} typically offer daily, weekly, and monthly rates for scissor lifts, with significant discounts available for longer rental periods. Be sure to inquire about delivery and pickup services when requesting quotes.",
        
        f"Before renting a scissor lift in {city}, assess your specific project needs including required height, weight capacity, and whether you'll be working indoors or outdoors. Most local rental companies can help determine the right equipment for your application.",
        
        f"When selecting a scissor lift rental in {city}, consider the working environment, required platform height, weight capacity needs, and rental duration to ensure you get the most cost-effective solution for your project."
    ]
    
    description += " " + random.choice(rental_advice)
    
    return description

# Load the Excel file
print("Loading Excel file...")
df = pd.read_excel('scissor-lift-companies.xlsx')

# Clean and prepare data
print("Cleaning and preparing data...")
df = df.fillna('')  # Replace NaN values with empty strings

# Function to strip UTM parameters from URLs
def clean_url(url):
    if not url:
        return ''
    # Remove UTM parameters and other tracking codes
    url = re.sub(r'\?utm_.*$', '', url)
    url = re.sub(r'&utm_.*$', '', url)
    # Remove any other query parameters if needed
    # url = re.sub(r'\?.*$', '', url)
    return url

# Function to validate and clean image URLs
def clean_image_url(url):
    if not url:
        return ''
    
    # Check if URL is truncated (common in Excel exports)
    if '...' in url:
        return ''
    
    # Remove @ symbol if it's at the beginning (sometimes added in Excel)
    if url.startswith('@'):
        url = url[1:]
    
    # Make sure URL has a valid scheme
    if not url.startswith(('http://', 'https://')):
        if url.startswith('//'):
            url = 'https:' + url
        else:
            url = 'https://' + url
    
    # Special handling for Google images
    if 'googleusercontent.com' in url or 'googleapis.com' in url:
        # Fix common issues with Google image URLs
        
        # Ensure we're using https
        url = url.replace('http://', 'https://')
        
        # Remove size restrictions that might be in the URL
        url = re.sub(r'=s\d+', '=s800', url)  # Set to a reasonable size
        url = re.sub(r'=w\d+', '=w800', url)
        url = re.sub(r'=h\d+', '=h500', url)
        
        # Fix common issues with Google Street View images
        if 'streetviewpixels' in url:
            # These often need special handling
            url = re.sub(r'\?.*$', '', url)  # Remove all query parameters
            url = url + '?cb=1'  # Add a cache-busting parameter
        
        # Handle Google Maps photos
        if 'AF1QipP' in url:
            # These are Google Maps user-contributed photos
            # Make sure we're using the right format
            url = re.sub(r'=.*$', '=w800-h500', url)
    
    # URL decode to handle any encoded characters
    url = unquote(url)
    
    return url

# Function to format working hours in a user-friendly way
def format_hours(hours_str):
    if not hours_str:
        return ''
    
    try:
        # Try to parse the JSON-like string
        hours_str = hours_str.replace("'", '"')  # Replace single quotes with double quotes for JSON parsing
        hours_dict = json.loads(hours_str)
        
        # Format the hours in a readable way
        formatted_hours = []
        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        for day in days_order:
            if day in hours_dict:
                time = hours_dict[day]
                formatted_hours.append(f"{day}: {time}")
        
        return "<br>".join(formatted_hours)
    except:
        # If parsing fails, return the original string
        return hours_str

# Function to format about section in a user-friendly way
def format_about(about_str):
    if not about_str:
        return ''
    
    try:
        # Try to parse the JSON-like string
        about_str = about_str.replace("'", '"')  # Replace single quotes with double quotes for JSON parsing
        about_dict = json.loads(about_str)
        
        # Format the about information in a readable way
        formatted_about = []
        
        for category, details in about_dict.items():
            formatted_about.append(f"<strong>{category}</strong>")
            
            if isinstance(details, dict):
                for feature, value in details.items():
                    if isinstance(value, bool):
                        value_text = "Yes" if value else "No"
                        formatted_about.append(f"- {feature}: {value_text}")
                    else:
                        formatted_about.append(f"- {feature}: {value}")
            else:
                formatted_about.append(f"- {details}")
        
        return "<br>".join(formatted_about)
    except:
        # If parsing fails, return the original string
        return about_str

# Apply URL cleaning to the site column
df['site'] = df['site'].apply(clean_url)

# Apply image URL cleaning
df['photo'] = df['photo'].apply(clean_image_url)

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

# Convert reviews to numeric for sorting
df['reviews_num'] = pd.to_numeric(df['reviews'], errors='coerce').fillna(0)

# Create output directory
os.makedirs('output', exist_ok=True)
os.makedirs('output/assets', exist_ok=True)
os.makedirs('output/assets/css', exist_ok=True)
os.makedirs('output/assets/images', exist_ok=True)
os.makedirs('output/assets/js', exist_ok=True)
os.makedirs('output/assets/data', exist_ok=True)

# Create a default placeholder image
with open('output/assets/images/placeholder.svg', 'w') as f:
    f.write('''<svg width="800" height="400" xmlns="http://www.w3.org/2000/svg">
    <rect width="800" height="400" fill="#e9ecef"/>
    <text x="400" y="200" font-family="Arial" font-size="30" text-anchor="middle" fill="#6c757d">Scissor Lift Rental</text>
</svg>''')

# Create a JavaScript file for image handling
with open('output/assets/js/image-handler.js', 'w') as f:
    f.write('''
// Function to handle image loading errors
function handleImageError(img) {
    img.onerror = null; // Prevent infinite loops
    img.src = '../../assets/images/placeholder.svg';
}

// Function to handle Google images specifically
function handleGoogleImage(img) {
    // Check if it's a Google image
    if (img.src.includes('googleusercontent.com') || img.src.includes('googleapis.com')) {
        // Create a backup of the original source
        var originalSrc = img.src;
        
        // Try to fix common issues with Google images
        if (img.src.includes('AF1QipP')) {
            // These are Google Maps user-contributed photos
            img.src = originalSrc.replace(/=.*$/, '=w800-h500');
        }
        
        // Add error handling
        img.onerror = function() {
            this.onerror = null;
            this.src = '../../assets/images/placeholder.svg';
        };
    }
}

// Process all images when the page loads
document.addEventListener('DOMContentLoaded', function() {
    var images = document.querySelectorAll('.company-photo');
    images.forEach(function(img) {
        // Add error handling to all images
        img.onerror = function() {
            handleImageError(this);
        };
        
        // Special handling for Google images
        handleGoogleImage(img);
    });
});
''')

# Create a JavaScript file for map handling
with open('output/assets/js/map-handler.js', 'w') as f:
    f.write('''
// Initialize the map when the page loads
function initMap() {
    // Get the map container
    var mapContainer = document.getElementById('map');
    
    // If there's no map container, exit
    if (!mapContainer) return;
    
    // Get the map data from the data attribute
    var mapData = JSON.parse(mapContainer.getAttribute('data-locations'));
    
    // If there are no locations, exit
    if (mapData.locations.length === 0) return;
    
    // Create the map centered on the city center
    var map = new google.maps.Map(mapContainer, {
        center: { lat: mapData.center.lat, lng: mapData.center.lng },
        zoom: mapData.zoom,
        mapTypeControl: true,
        streetViewControl: true,
        fullscreenControl: true
    });
    
    // Create an info window to share between markers
    var infoWindow = new google.maps.InfoWindow();
    
    // Create markers for each location
    mapData.locations.forEach(function(location) {
        // Create a marker
        var marker = new google.maps.Marker({
            position: { lat: location.lat, lng: location.lng },
            map: map,
            title: location.name,
            animation: google.maps.Animation.DROP
        });
        
        // Create the content for the info window
        var content = '<div class="map-info-window">' +
            '<h3>' + location.name + '</h3>' +
            '<p><strong>Address:</strong> ' + location.address + '</p>';
        
        if (location.phone) {
            content += '<p><strong>Phone:</strong> ' + location.phone + '</p>';
        }
        
        if (location.reviews) {
            content += '<p><strong>Reviews:</strong> ' + location.reviews + '</p>';
        }
        
        if (location.website) {
            content += '<p><a href="' + location.website + '" target="_blank" rel="nofollow noopener noreferrer">Visit Website</a></p>';
        }
        
        content += '</div>';
        
        // Add a click event to the marker
        marker.addListener('click', function() {
            infoWindow.setContent(content);
            infoWindow.open(map, marker);
        });
    });
}
''')

# Create a JavaScript file for search functionality
with open('output/assets/js/search-handler.js', 'w') as f:
    f.write('''
// Function to handle the search form submission
function handleSearch(event) {
    event.preventDefault();
    
    // Get the search query
    var searchQuery = document.getElementById('search-input').value.trim();
    
    // If the search query is empty, show an error message
    if (!searchQuery) {
        showSearchError('Please enter a city, state, or zip code');
        return;
    }
    
    // Show loading indicator
    showSearchLoading();
    
    // Fetch the search data
    fetch('assets/data/search-data.json')
        .then(response => response.json())
        .then(data => {
            processSearchResults(searchQuery, data);
        })
        .catch(error => {
            console.error('Error fetching search data:', error);
            showSearchError('An error occurred while searching. Please try again.');
        });
}

// Function to process search results
function processSearchResults(query, data) {
    query = query.toLowerCase();
    
    // First, try to find an exact match for city or zip
    var exactMatches = [];
    
    // Check for exact city matches
    data.cities.forEach(city => {
        if (city.name.toLowerCase() === query || 
            city.name.toLowerCase() + ', ' + city.state.toLowerCase() === query) {
            exactMatches.push({
                type: 'city',
                url: city.url,
                name: city.name,
                state: city.state,
                distance: 0
            });
        }
    });
    
    // Check for exact zip matches
    data.zips.forEach(zip => {
        if (zip.code === query) {
            exactMatches.push({
                type: 'zip',
                url: zip.url,
                name: zip.city,
                state: zip.state,
                distance: 0
            });
        }
    });
    
    // If we have exact matches, redirect to the first one
    if (exactMatches.length > 0) {
        window.location.href = exactMatches[0].url;
        return;
    }
    
    // If no exact matches, try partial matches for cities
    var partialMatches = [];
    
    data.cities.forEach(city => {
        if (city.name.toLowerCase().includes(query) || 
            query.includes(city.name.toLowerCase()) ||
            city.state.toLowerCase().includes(query) ||
            query.includes(city.state.toLowerCase())) {
            
            // Calculate a simple relevance score based on string similarity
            var relevance = 0;
            if (city.name.toLowerCase().startsWith(query)) relevance += 3;
            else if (city.name.toLowerCase().includes(query)) relevance += 2;
            else if (query.includes(city.name.toLowerCase())) relevance += 1;
            
            partialMatches.push({
                type: 'city',
                url: city.url,
                name: city.name,
                state: city.state,
                relevance: relevance
            });
        }
    });
    
    // Sort partial matches by relevance
    partialMatches.sort((a, b) => b.relevance - a.relevance);
    
    // If we have partial matches, show the top 5
    if (partialMatches.length > 0) {
        showSearchResults(partialMatches.slice(0, 5));
        return;
    }
    
    // If no matches at all, show a message
    showSearchError('No matches found. Please try a different search term.');
}

// Function to show search results
function showSearchResults(results) {
    var resultsContainer = document.getElementById('search-results');
    resultsContainer.innerHTML = '';
    resultsContainer.style.display = 'block';
    
    var resultsList = document.createElement('ul');
    resultsList.className = 'search-results-list';
    
    results.forEach(result => {
        var listItem = document.createElement('li');
        var link = document.createElement('a');
        link.href = result.url;
        link.textContent = result.name + ', ' + result.state;
        listItem.appendChild(link);
        resultsList.appendChild(listItem);
    });
    
    resultsContainer.appendChild(resultsList);
    
    // Hide loading indicator
    document.getElementById('search-loading').style.display = 'none';
}

// Function to show search error
function showSearchError(message) {
    var resultsContainer = document.getElementById('search-results');
    resultsContainer.innerHTML = '<p class="search-error">' + message + '</p>';
    resultsContainer.style.display = 'block';
    
    // Hide loading indicator
    document.getElementById('search-loading').style.display = 'none';
}

// Function to show search loading
function showSearchLoading() {
    var resultsContainer = document.getElementById('search-results');
    resultsContainer.innerHTML = '';
    resultsContainer.style.display = 'block';
    
    // Show loading indicator
    document.getElementById('search-loading').style.display = 'block';
}

// Add event listener to the search form
document.addEventListener('DOMContentLoaded', function() {
    var searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', handleSearch);
    }
});
''')

# Create CSS file
with open('output/assets/css/style.css', 'w') as f:
    f.write('''
/* Global styles */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    margin: 0;
    padding: 0;
    background-color: #f8f9fa;
}

header {
    background-color: #0056b3;
    color: white;
    text-align: center;
    padding: 2rem 1rem;
}

header h1 {
    margin: 0;
    font-size: 2.5rem;
}

header p {
    margin: 0.5rem 0 0;
    font-size: 1.2rem;
    opacity: 0.9;
}

main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
}

footer {
    text-align: center;
    padding: 1.5rem;
    background-color: #343a40;
    color: white;
}

a {
    color: #0056b3;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

/* State list */
.state-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
    list-style: none;
    padding: 0;
    margin: 2rem 0;
}

.state-list li {
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s;
}

.state-list li:hover {
    transform: translateY(-3px);
}

.state-list a {
    display: block;
    padding: 1rem;
    text-align: center;
    font-weight: 500;
}

/* City list */
.city-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 1rem;
    list-style: none;
    padding: 0;
    margin: 2rem 0;
}

.city-list li {
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s;
}

.city-list li:hover {
    transform: translateY(-3px);
}

.city-list a {
    display: block;
    padding: 1rem;
    text-align: center;
    font-weight: 500;
}

/* Company cards */
.company-card {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
    margin-bottom: 2rem;
    overflow: hidden;
    transition: transform 0.3s, box-shadow 0.3s;
}

.company-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
}

.company-content {
    padding: 1.5rem;
}

.company-name {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: #0056b3;
}

.company-details {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1.5rem;
}

@media (min-width: 768px) {
    .company-details {
        grid-template-columns: 1.5fr 1fr;
    }
}

.company-info p, .company-contact p {
    margin: 0.7rem 0;
}

.reviews {
    font-weight: 500;
}

.website-link {
    display: inline-block;
    background-color: #0056b3;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    margin-top: 0.5rem;
    transition: background-color 0.2s;
}

.website-link:hover {
    background-color: #003d7a;
    text-decoration: none;
}

/* Breadcrumb */
.breadcrumb {
    background-color: #e9ecef;
    padding: 0.8rem 1rem;
    border-radius: 4px;
    margin: 1rem auto;
    max-width: 1200px;
    font-size: 0.9rem;
}

/* Info section */
.info-section {
    background-color: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-top: 3rem;
}

.info-section h2 {
    color: #0056b3;
    margin-top: 2rem;
}

.info-section h2:first-child {
    margin-top: 0;
}

.info-section ul {
    padding-left: 1.5rem;
}

/* Map */
.map-container {
    height: 400px;
    margin: 2rem 0;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

#map {
    height: 100%;
    width: 100%;
}

/* Footer */
.footer-content {
    text-align: center;
    padding: 1.5rem;
}

.footer-content p {
    margin: 0.5rem 0;
}

.footer-content a {
    color: #ccc;
    text-decoration: underline;
    transition: color 0.2s;
}

.footer-content a:hover {
    color: white;
}

/* Responsive adjustments */
@media (max-width: 576px) {
    header h1 {
        font-size: 2rem;
    }
    
    header p {
        font-size: 1rem;
    }
    
    .company-name {
        font-size: 1.3rem;
    }
    
    .state-list, .city-list {
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    }
}
    ''')

# Set up Jinja2 templates
env = Environment(loader=FileSystemLoader('.'))

# Function to generate SEO-optimized meta titles
def generate_meta_title(page_type, city=None, state=None):
    if page_type == 'homepage':
        return "Scissor Lift Rental Near Me | Find Local Scissor Lift Rentals & Prices"
    elif page_type == 'state':
        return f"Scissor Lift Rental in {state} | Top Equipment Rental Companies"
    elif page_type == 'city':
        return f"Scissor Lift Rental in {city}, {state} | Best Prices & Local Providers"
    return ""

# Function to generate SEO-optimized meta descriptions
def generate_meta_description(page_type, city=None, state=None):
    if page_type == 'homepage':
        return "Find scissor lift rentals near you. Compare prices, brands, and availability from top-rated scissor lift rental companies across the United States."
    elif page_type == 'state':
        return f"Looking for scissor lift rentals in {state}? Browse our directory of {state} scissor lift rental companies. Compare prices, equipment types, and availability for your project needs."
    elif page_type == 'city':
        return f"Find the best scissor lift rentals in {city}, {state}. Compare local providers, prices, and equipment options. Get quotes from top-rated scissor lift rental companies in {city}."
    return ""

# Add navigation header to all templates
nav_header = '''
<nav class="main-nav">
    <div class="nav-container">
        <div class="logo">
            <a href="../">Scissor Lifts for Rent</a>
        </div>
        <ul class="nav-links">
            <li><a href="../">Home</a></li>
            <li><a href="../states/">Browse By State</a></li>
        </ul>
    </div>
</nav>
'''

# Create homepage-specific navigation header
homepage_nav_header = '''
<nav class="main-nav">
    <div class="nav-container">
        <div class="logo">
            <a href="./">Scissor Lifts for Rent</a>
        </div>
        <ul class="nav-links">
            <li><a href="./">Home</a></li>
            <li><a href="./states/">Browse By State</a></li>
        </ul>
    </div>
</nav>
'''

# Create city-specific navigation header
city_nav_header = '''
<nav class="main-nav">
    <div class="nav-container">
        <div class="logo">
            <a href="../../">Scissor Lifts for Rent</a>
        </div>
        <ul class="nav-links">
            <li><a href="../../">Home</a></li>
            <li><a href="../../states/">Browse By State</a></li>
        </ul>
    </div>
</nav>
'''

# Create homepage template with search functionality
homepage_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ meta_title }}</title>
    <meta name="description" content="{{ meta_description }}">
    <link rel="stylesheet" href="assets/css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <link rel="icon" href="assets/images/scissor-lift-favicon.png" type="image/png">
    <link rel="shortcut icon" href="assets/images/scissor-lift-favicon.png" type="image/png">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "Scissor Lift Rental Directory",
      "url": "https://scissorliftrentals.com/",
      "potentialAction": {
        "@type": "SearchAction",
        "target": "https://scissorliftrentals.com/?search={search_term_string}",
        "query-input": "required name=search_term_string"
      },
      "description": "{{ meta_description }}"
    }
    </script>
</head>
<body>
    ''' + homepage_nav_header + '''
    <div class="hero-container">
        <div class="hero-content">
            <h1>Scissor Lift Rental Near Me</h1>
            <p class="hero-description">Access affordable scissor lift rentals nationwide from trusted providers. Compare prices, specifications, and availability for electric, rough terrain, and diesel models to find the perfect equipment for your construction, maintenance, or industrial project.</p>
        </div>
    </div>
    
    <main>
        <section>
            <h2>Browse Scissor Lift Rentals by State</h2>
            <ul class="state-list">
                {% for state, state_slug in states %}
                <li><a href="{{ state_slug }}/">{{ state }}</a></li>
                {% endfor %}
            </ul>
        </section>
        
        <section class="info-section">
            <h2>Why Rent a Scissor Lift?</h2>
            <p>Scissor lifts are essential equipment for construction, maintenance, and industrial applications. They provide a stable platform for workers to reach elevated areas safely. Renting a scissor lift is often more economical than purchasing, especially for short-term projects.</p>
            
            <h2>Types of Scissor Lifts Available for Rent</h2>
            <p>Our directory includes companies that rent various types of scissor lifts:</p>
            <ul>
                <li><strong>Electric Scissor Lifts:</strong> Ideal for indoor use with zero emissions</li>
                <li><strong>Rough Terrain Scissor Lifts:</strong> Perfect for outdoor construction sites</li>
                <li><strong>Diesel Scissor Lifts:</strong> For heavy-duty applications requiring more power</li>
            </ul>
            
            <h2>How to Choose the Right Scissor Lift Rental</h2>
            <p>Consider these factors when selecting a scissor lift rental:</p>
            <ul>
                <li>Height requirements for your project</li>
                <li>Weight capacity needed</li>
                <li>Indoor vs. outdoor use</li>
                <li>Platform size requirements</li>
                <li>Rental duration and budget</li>
            </ul>
        </section>
    </main>
    
    <footer>
        <div class="footer-content">
            <p>&copy; {{ current_year }} Scissor Lift Rental Directory. All rights reserved.</p>
            <p><a href="sitemap.xml">Sitemap</a></p>
        </div>
    </footer>
</body>
</html>'''

# Create state page template
state_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ meta_title }}</title>
    <meta name="description" content="{{ meta_description }}">
    <link rel="stylesheet" href="../assets/css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <link rel="icon" href="../assets/images/scissor-lift-favicon.png" type="image/png">
    <link rel="shortcut icon" href="../assets/images/scissor-lift-favicon.png" type="image/png">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "name": "Scissor Lift Rental in {{ state }}",
      "description": "{{ meta_description }}",
      "url": "https://scissorliftrentals.com/{{ state_slug }}/",
      "mainEntity": {
        "@type": "ItemList",
        "itemListElement": [
          {% for city, city_slug in cities %}
          {
            "@type": "ListItem",
            "position": {{ loop.index }},
            "url": "https://scissorliftrentals.com/{{ state_slug }}/{{ city_slug }}/"
          }{% if not loop.last %},{% endif %}
          {% endfor %}
        ]
      }
    }
    </script>
</head>
<body>
    ''' + nav_header + '''
    <div class="hero-container">
        <div class="hero-content">
            <h1>Scissor Lift Rental in {{ state }}</h1>
            <p class="hero-description">Find the best scissor lift rental companies in {{ state }}. Compare prices, equipment options, and availability from top-rated providers.</p>
        </div>
    </div>
    
    <div class="breadcrumb">
        <a href="../"><i class="fas fa-home"></i> Home</a> &gt; <a href="../states/">States</a> &gt; {{ state }}
    </div>
    
    <main>
        <section>
            <h2>Browse Scissor Lift Rentals in {{ state }} by City</h2>
            <ul class="city-list">
                {% for city, city_slug in cities %}
                <li><a href="{{ city_slug }}/">{{ city }}</a></li>
                {% endfor %}
            </ul>
        </section>
        
        <section class="info-section">
            <h2>About Scissor Lift Rentals in {{ state }}</h2>
            <p>{{ state_description }}</p>
            
            <h2>Safety Tips for Using Scissor Lifts</h2>
            <p>When operating scissor lifts in {{ state }}, always follow these essential safety guidelines:</p>
            <ul>
                <li><strong>Pre-Operation Inspection:</strong> Always inspect the scissor lift before use, checking for hydraulic leaks, damaged controls, or structural issues</li>
                <li><strong>Weight Limitations:</strong> Never exceed the manufacturer's specified weight capacity, including all personnel, tools, and materials</li>
                <li><strong>Platform Maintenance:</strong> Keep the platform clean and free of debris, oil, or other slip hazards</li>
                <li><strong>Overhead Awareness:</strong> Be aware of overhead obstructions including power lines, ceiling fixtures, and building structures</li>
                <li><strong>Level Operation:</strong> Only operate on level surfaces unless using a rough terrain model specifically designed for uneven ground</li>
                <li><strong>Proper Training:</strong> Ensure all operators have received proper training and certification for scissor lift operation</li>
                <li><strong>Weather Considerations:</strong> Avoid outdoor operation during high winds, storms, or extreme weather conditions</li>
                <li><strong>Manufacturer Guidelines:</strong> Follow all manufacturer guidelines and safety protocols specific to your equipment model</li>
            </ul>
        </section>
    </main>
    
    <footer>
        <div class="footer-content">
            <p>&copy; {{ current_year }} Scissor Lift Rental Directory. All rights reserved.</p>
            <p><a href="../sitemap.xml">Sitemap</a></p>
        </div>
    </footer>
</body>
</html>'''

# Create city page template
city_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ meta_title }}</title>
    <meta name="description" content="{{ meta_description }}">
    <link rel="stylesheet" href="../../assets/css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <link rel="icon" href="../../assets/images/scissor-lift-favicon.png" type="image/png">
    <link rel="shortcut icon" href="../../assets/images/scissor-lift-favicon.png" type="image/png">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "LocalBusiness",
      "name": "Scissor Lift Rental in {{ city }}, {{ state }}",
      "description": "{{ meta_description }}",
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "{{ city }}",
        "addressRegion": "{{ state }}"
      },
      "geo": {
        "@type": "GeoCoordinates"
        {% if map_data %}
        ,"latitude": {{ map_data.split(',')[0] }},
        "longitude": {{ map_data.split(',')[1] }}
        {% endif %}
      },
      "url": "https://scissorliftrentals.com/{{ state_slug }}/{{ city_slug }}/",
      "telephone": "",
      "openingHoursSpecification": {
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": [
          "Monday",
          "Tuesday",
          "Wednesday",
          "Thursday",
          "Friday"
        ],
        "opens": "08:00",
        "closes": "17:00"
      }
    }
    </script>
</head>
<body>
    ''' + city_nav_header + '''
    <div class="hero-container">
        <div class="hero-content">
            <h1>Scissor Lift Rental in {{ city }}, {{ state }}</h1>
            <p class="hero-description">Find the best scissor lift rental companies in {{ city }}, {{ state }}. Compare local providers, equipment options, and get quotes for your project.</p>
        </div>
    </div>
    
    <div class="breadcrumb">
        <a href="../../"><i class="fas fa-home"></i> Home</a> &gt; <a href="../../states/">States</a> &gt; <a href="../">{{ state }}</a> &gt; {{ city }}
    </div>
    
    <main>
        {% if map_data %}
        <section>
            <h2>Scissor Lift Rental Locations in {{ city }}, {{ state }}</h2>
            <div class="map-container">
                <div id="map" data-locations='{{ map_data|safe }}'></div>
            </div>
        </section>
        {% endif %}
        
        <section>
            <h2>Top Scissor Lift Rental Companies in {{ city }}, {{ state }}</h2>
            
            {% if companies %}
                {% for company in companies %}
                <div class="company-card" itemscope itemtype="https://schema.org/LocalBusiness">
                    <meta itemprop="name" content="{{ company.name }}">
                    <meta itemprop="address" content="{{ company.full_address }}">
                    {% if company.phone %}
                    <meta itemprop="telephone" content="{{ company.phone }}">
                    {% endif %}
                    {% if company.site %}
                    <meta itemprop="url" content="{{ company.site }}">
                    {% endif %}
                    {% if company.reviews %}
                    <meta itemprop="aggregateRating" content="{{ company.reviews }}">
                    {% endif %}
                    <div class="company-content">
                        <div class="company-name">{{ company.name }}</div>
                        <div class="company-details">
                            <div class="company-info">
                                <p><strong><i class="fas fa-star"></i> Reviews:</strong> <span class="reviews">{{ company.reviews }}</span></p>
                                {% if company.Scissor_Lift_Brands %}
                                <p><strong><i class="fas fa-tag"></i> Scissor Lift Brands Available:</strong> {{ company.Scissor_Lift_Brands }}</p>
                                {% endif %}
                                {% if company.Sizes_Available %}
                                <p><strong><i class="fas fa-ruler-vertical"></i> Sizes Available:</strong> {{ company.Sizes_Available }}</p>
                                {% endif %}
                                {% if company.about %}
                                <p><strong><i class="fas fa-info-circle"></i> About:</strong> {{ company.about|safe }}</p>
                                {% endif %}
                            </div>
                            <div class="company-contact">
                                <p><strong><i class="fas fa-map-marker-alt"></i> Address:</strong> {{ company.full_address }}</p>
                                {% if company.phone %}
                                <p><strong><i class="fas fa-phone"></i> Phone:</strong> {{ company.phone }}</p>
                                {% endif %}
                                {% if company.site %}
                                <p><a href="{{ company.site }}" target="_blank" rel="nofollow noopener noreferrer" class="website-link"><i class="fas fa-external-link-alt"></i> Visit their website</a></p>
                                {% endif %}
                                {% if company.working_hours %}
                                <p><strong><i class="fas fa-clock"></i> Hours:</strong> {{ company.working_hours|safe }}</p>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                </div>
                {% endfor %}
            {% else %}
                <p>No scissor lift rental companies found in this area. Please check nearby cities or contact us for assistance.</p>
            {% endif %}
        </section>
        
        <section class="info-section">
            <h2>Renting Scissor Lifts in {{ city }}, {{ state }}</h2>
            <p>{{ city_description }}</p>
            
            <h2>Types of Scissor Lifts Available in {{ city }}</h2>
            <p>Rental companies in {{ city }} typically offer several types of scissor lifts to meet different project needs:</p>
            <ul>
                <li><strong>Electric Scissor Lifts:</strong> Ideal for indoor use with zero emissions, perfect for warehouse work, maintenance, and indoor construction</li>
                <li><strong>Rough Terrain Scissor Lifts:</strong> Designed with rugged tires and powerful engines for outdoor construction sites and uneven surfaces</li>
                <li><strong>Diesel Scissor Lifts:</strong> Provide exceptional power for heavy-duty applications and extended outdoor use</li>
                <li><strong>Compact Scissor Lifts:</strong> Smaller models that can fit through standard doorways and operate in tight spaces</li>
                <li><strong>High-Capacity Scissor Lifts:</strong> Models designed to support multiple workers and heavier materials</li>
            </ul>
            
            <h2>Safety Considerations for Scissor Lift Operation</h2>
            <p>When operating scissor lifts in {{ city }}, always prioritize safety with these essential guidelines:</p>
            <ul>
                <li><strong>Operator Training:</strong> Ensure all personnel have proper training and certification before operating equipment</li>
                <li><strong>Site Assessment:</strong> Evaluate the work area for potential hazards including uneven surfaces, overhead obstructions, and power lines</li>
                <li><strong>Equipment Inspection:</strong> Thoroughly inspect the scissor lift before each use, checking controls, safety devices, and hydraulic systems</li>
                <li><strong>Weather Awareness:</strong> Consider local {{ city }} weather conditions, avoiding outdoor operation during high winds or storms</li>
                <li><strong>Fall Protection:</strong> Always use appropriate fall protection equipment when required by regulations or manufacturer guidelines</li>
                <li><strong>Load Management:</strong> Never exceed the manufacturer's specified weight capacity for the specific model</li>
            </ul>
        </section>
    </main>
    
    <footer>
        <div class="footer-content">
            <p>&copy; {{ current_year }} Scissor Lift Rental Directory. All rights reserved.</p>
            <p><a href="../../sitemap.xml">Sitemap</a></p>
        </div>
    </footer>
    
    {% if map_data %}
    <!-- Google Maps API -->
    <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBNLrJhOMz6idD05pzfn5lhA-TAw-mAZCU&callback=initMap" async defer></script>
    <script src="../../assets/js/map-handler.js"></script>
    {% endif %}
</body>
</html>'''

# Create state portal template with card-based layout
state_portal_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Find Scissor Lift Rentals By State | Browse All States</title>
    <meta name="description" content="Browse scissor lift rentals by state. Find local scissor lift rental companies across the United States with our comprehensive directory organized by location.">
    <link rel="stylesheet" href="../assets/css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <link rel="icon" href="../assets/images/scissor-lift-favicon.png" type="image/png">
    <link rel="shortcut icon" href="../assets/images/scissor-lift-favicon.png" type="image/png">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "name": "Find Scissor Lift Rentals By State",
      "description": "Browse scissor lift rentals by state. Find local scissor lift rental companies across the United States with our comprehensive directory organized by location.",
      "url": "https://scissorliftrentals.com/states/",
      "mainEntity": {
        "@type": "ItemList",
        "itemListElement": [
          {% for state, state_slug in states %}
          {
            "@type": "ListItem",
            "position": {{ loop.index }},
            "url": "https://scissorliftrentals.com/{{ state_slug }}/"
          }{% if not loop.last %},{% endif %}
          {% endfor %}
        ]
      }
    }
    </script>
</head>
<body>
    ''' + nav_header + '''
    <div class="hero-container state-portal-hero">
        <div class="hero-content">
            <h1>Find Scissor Lift Rentals By State</h1>
            <p class="hero-description">Browse our comprehensive directory of scissor lift rental companies organized by state. Find local providers, compare equipment options, and get the best rental prices for your project needs.</p>
        </div>
    </div>
    
    <main>
        <div class="breadcrumb">
            <a href="../"><i class="fas fa-home"></i> Home</a> &gt; States
        </div>
        
        <section>
            <h2>Browse All States</h2>
            <ul class="state-list state-portal-list">
                {% for state, state_slug in states %}
                <li class="state-card">
                    <a href="../{{ state_slug }}/">
                        <h3>{{ state }}</h3>
                        <p>Find scissor lift rentals in {{ state }}</p>
                        <span class="state-link">View Rentals <i class="fas fa-arrow-right"></i></span>
                    </a>
                </li>
                {% endfor %}
            </ul>
        </section>
        
        <section class="info-section">
            <h2>Why Browse Scissor Lift Rentals by State?</h2>
            <p>Finding the right scissor lift rental company in your area is essential for project success. Our state-by-state directory helps you:</p>
            <ul>
                <li><strong>Find Local Providers:</strong> Connect with rental companies in your specific state</li>
                <li><strong>Compare Options:</strong> View multiple providers to compare prices and equipment availability</li>
                <li><strong>Save Time:</strong> Quickly narrow down options to companies that serve your location</li>
                <li><strong>Access Specialized Equipment:</strong> Find providers with the specific scissor lift models you need</li>
            </ul>
            
            <h2>Types of Scissor Lifts Available Across the United States</h2>
            <p>Scissor lift rental companies throughout the country offer various types of equipment:</p>
            <ul>
                <li><strong>Electric Scissor Lifts:</strong> Ideal for indoor use with zero emissions</li>
                <li><strong>Rough Terrain Scissor Lifts:</strong> Perfect for outdoor construction sites</li>
                <li><strong>Diesel Scissor Lifts:</strong> For heavy-duty applications requiring more power</li>
                <li><strong>Compact Scissor Lifts:</strong> For tight spaces and narrow doorways</li>
                <li><strong>High-Reach Scissor Lifts:</strong> For applications requiring maximum height</li>
            </ul>
            
            <h2>How to Choose the Right Scissor Lift Rental in Your State</h2>
            <p>When selecting a scissor lift rental company in your state, consider these factors:</p>
            <ul>
                <li>Local availability and delivery options</li>
                <li>Rental duration flexibility</li>
                <li>Equipment condition and maintenance history</li>
                <li>Operator training and certification options</li>
                <li>Emergency service and support availability</li>
                <li>Insurance and liability coverage</li>
            </ul>
        </section>
    </main>
    
    <footer>
        <div class="footer-content">
            <p>&copy; {{ current_year }} Scissor Lift Rental Directory. All rights reserved.</p>
            <p><a href="../sitemap.xml">Sitemap</a></p>
        </div>
    </footer>
</body>
</html>'''

# Generate the site
from datetime import datetime
current_year = datetime.now().year

print("Generating site structure...")

# Create homepage
states_with_companies = df[df['state_slug'] != ''][['us_state', 'state_slug']].drop_duplicates().sort_values('us_state')
states_list = [(state, slug) for state, slug in zip(states_with_companies['us_state'], states_with_companies['state_slug'])]

# Define popular states
popular_states = [
    ('California', 'ca'),
    ('Texas', 'tx'),
    ('Florida', 'fl'),
    ('New York', 'ny'),
    ('Illinois', 'il')
]

# Generate homepage
homepage_html = Environment().from_string(homepage_template.replace(
    '<h2>Browse Scissor Lift Rentals by State</h2>',
    '<h2>Browse Scissor Lift Rentals by State <a href="states/" class="view-all-link">View All States <i class="fas fa-arrow-right"></i></a></h2>'
)).render(
    states=states_list,
    popular_states=popular_states,
    current_year=current_year,
    meta_title=generate_meta_title("homepage"),
    meta_description=generate_meta_description("homepage")
)

with open('output/index.html', 'w') as f:
    f.write(homepage_html)

# Create search data for the search functionality
print("Generating search data...")
search_data = {
    "cities": [],
    "zips": []
}

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

# Save search data to a JSON file
with open('output/assets/data/search-data.json', 'w') as f:
    json.dump(search_data, f)

# Create state pages
for state, state_slug in states_list:
    # Create state directory
    os.makedirs(f'output/{state_slug}', exist_ok=True)
    
    # Get cities in this state
    state_df = df[df['state_slug'] == state_slug]
    cities_with_companies = state_df[state_df['city_slug'] != ''][['city', 'city_slug']].drop_duplicates().sort_values('city')
    cities_list = [(city, slug) for city, slug in zip(cities_with_companies['city'], cities_with_companies['city_slug'])]
    
    # Generate state page
    state_html = Environment().from_string(state_template).render(
        state=state,
        cities=cities_list,
        popular_states=popular_states,
        current_year=current_year,
        state_description=generate_state_description(state),
        meta_title=f"Scissor Lift Rental in {state} | Top Equipment Rental Companies",
        meta_description=f"Looking for scissor lift rentals in {state}? Browse our directory of {state} scissor lift rental companies. Compare prices, equipment types, and availability for your project needs."
    )
    
    with open(f'output/{state_slug}/index.html', 'w') as f:
        f.write(state_html)
    
    # Create city pages
    for city, city_slug in cities_list:
        # Create city directory
        os.makedirs(f'output/{state_slug}/{city_slug}', exist_ok=True)
        
        # Get companies in this city
        city_df = state_df[state_df['city_slug'] == city_slug].sort_values('reviews_num', ascending=False)
        
        # Prepare map data if we have coordinates
        map_data = None
        if not city_df.empty and city_df['latitude'].notna().any() and city_df['longitude'].notna().any():
            # Filter out rows with invalid coordinates
            valid_coords_df = city_df[(city_df['latitude'].notna()) & (city_df['longitude'].notna())]
            
            if not valid_coords_df.empty:
                # Calculate the center of the map
                center_lat = statistics.mean(valid_coords_df['latitude'].astype(float))
                center_lng = statistics.mean(valid_coords_df['longitude'].astype(float))
                
                # Prepare location data for the map
                locations = []
                for _, row in valid_coords_df.iterrows():
                    try:
                        lat = float(row['latitude'])
                        lng = float(row['longitude'])
                        
                        location = {
                            'name': row['name'],
                            'lat': lat,
                            'lng': lng,
                            'address': row['full_address'],
                            'phone': row['phone'],
                            'reviews': row['reviews'],
                            'website': row['site']
                        }
                        locations.append(location)
                    except (ValueError, TypeError):
                        # Skip if we can't convert coordinates to float
                        continue
                
                if locations:
                    map_data = json.dumps({
                        'center': {'lat': center_lat, 'lng': center_lng},
                        'zoom': 12,
                        'locations': locations
                    })
        
        # Prepare company data for template
        companies = []
        for _, row in city_df.iterrows():
            companies.append({
                'name': row['name'],
                'reviews': row['reviews'],
                'Scissor_Lift_Brands': row['Scissor Lift Brands'],
                'Sizes_Available': row['Sizes Available'],
                'full_address': row['full_address'],
                'phone': row['phone'],
                'site': row['site'],
                'about': format_about(row['about']),
                'working_hours': format_hours(row['working_hours'])
            })
        
        # Generate city page
        city_html = Environment().from_string(city_template).render(
            city=city,
            state=state,
            companies=companies,
            map_data=map_data,
            popular_states=popular_states,
            current_year=current_year,
            city_description=generate_city_description(city, state),
            meta_title=f"Scissor Lift Rental in {city}, {state} | Best Prices & Local Providers",
            meta_description=f"Find the best scissor lift rentals in {city}, {state}. Compare local providers, prices, and equipment options. Get quotes from top-rated scissor lift rental companies in {city}."
        )
        
        with open(f'output/{state_slug}/{city_slug}/index.html', 'w') as f:
            f.write(city_html)

# Generate sitemap.xml
print("Generating sitemap.xml...")
with open('output/sitemap.xml', 'w') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    
    # Homepage
    f.write('  <url>\n')
    f.write('    <loc>https://scissorliftrentals.com/</loc>\n')
    f.write('    <changefreq>weekly</changefreq>\n')
    f.write('    <priority>1.0</priority>\n')
    f.write('  </url>\n')
    
    # State pages
    for state, state_slug in states_list:
        f.write('  <url>\n')
        f.write(f'    <loc>https://scissorliftrentals.com/{state_slug}/</loc>\n')
        f.write('    <changefreq>weekly</changefreq>\n')
        f.write('    <priority>0.8</priority>\n')
        f.write('  </url>\n')
        
        # City pages for this state
        state_df = df[df['state_slug'] == state_slug]
        cities = sorted(set(zip(state_df['city'], state_df['city_slug'])))
        
        for city, city_slug in cities:
            f.write('  <url>\n')
            f.write(f'    <loc>https://scissorliftrentals.com/{state_slug}/{city_slug}/</loc>\n')
            f.write('    <changefreq>weekly</changefreq>\n')
            f.write('    <priority>0.6</priority>\n')
            f.write('  </url>\n')
      
    f.write('</urlset>')

print("Site generation complete! Output is in the 'output' directory.")

# Copy the scissor-lift.jpeg to the assets/images directory
print("Copying hero image to assets directory...")
os.makedirs('output/assets/images', exist_ok=True)
import shutil
shutil.copy('scissor-lift.jpeg', 'output/assets/images/scissor-lift.jpeg')

# Copy the favicon to the output directory
print("Copying favicon to output directory...")
os.makedirs('output/assets/images', exist_ok=True)
shutil.copy('scissor-lift-favicon.png', 'output/assets/images/scissor-lift-favicon.png')

# Also copy to assets/images for direct references
os.makedirs('output/assets/images', exist_ok=True)
shutil.copy('scissor-lift-favicon.png', 'output/assets/images/favicon.ico')

# Add hero styles to the CSS file
print("Adding hero styles to CSS...")
with open('output/assets/css/style.css', 'r') as f:
    css_content = f.read()

# Add hero styles if they don't already exist
if '.hero-container' not in css_content:
    hero_styles = '''
/* Hero section styles */
.hero-container {
    position: relative;
    width: 100%;
    height: 500px;
    background-image: url('../images/scissor-lift.jpeg');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    margin-bottom: 2rem;
}

.hero-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
}

.hero-content {
    position: relative;
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    color: white;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
}

.hero-content h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.hero-description {
    font-size: 1.2rem;
    max-width: 800px;
    line-height: 1.6;
    margin: 0 auto;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

@media (max-width: 768px) {
    .hero-container {
        height: 400px;
    }
    
    .hero-content h1 {
        font-size: 2.2rem;
    }
    
    .hero-description {
        font-size: 1rem;
    }
}

@media (max-width: 576px) {
    .hero-container {
        height: 350px;
    }
    
    .hero-content h1 {
        font-size: 1.8rem;
    }
}
'''
    
    with open('output/assets/css/style.css', 'a') as f:
        f.write(hero_styles)

# Generate state portal page
print("Generating state portal page...")
os.makedirs('output/states', exist_ok=True)

state_portal_html = Environment().from_string(state_portal_template).render(
    states=states_list,
    current_year=current_year
)

with open('output/states/index.html', 'w') as f:
    f.write(state_portal_html)

# Update homepage to link to the state portal page
homepage_template = homepage_template.replace(
    '<h2>Browse Scissor Lift Rentals by State</h2>',
    '<h2>Browse Scissor Lift Rentals by State <a href="states/" class="view-all-link">View All States <i class="fas fa-arrow-right"></i></a></h2>'
)

# Add view-all-link style if it doesn't exist
if '.view-all-link' not in css_content:
    view_all_link_style = '''
/* View all link */
.view-all-link {
    float: right;
    font-size: 1rem;
    font-weight: normal;
    color: #0056b3;
}

.view-all-link i {
    margin-left: 5px;
    transition: transform 0.2s;
}

.view-all-link:hover i {
    transform: translateX(3px);
}

@media (max-width: 576px) {
    .view-all-link {
        display: block;
        float: none;
        margin-top: 0.5rem;
        font-size: 0.9rem;
    }
}
'''
    
    with open('output/assets/css/style.css', 'a') as f:
        f.write(view_all_link_style)

# Add navigation styles to CSS
print("Adding navigation styles to CSS...")
with open('output/assets/css/style.css', 'r') as f:
    css_content = f.read()

# Add navigation styles if they don't already exist
if '.main-nav' not in css_content:
    nav_styles = '''
/* Navigation styles */
.main-nav {
    background-color: #0056b3;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
}

.nav-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0.8rem 1rem;
}

.logo a {
    color: white;
    font-size: 1.5rem;
    font-weight: 700;
    text-decoration: none;
}

.nav-links {
    display: flex;
    list-style: none;
    margin: 0;
    padding: 0;
}

.nav-links li {
    margin-left: 1.5rem;
}

.nav-links a {
    color: white;
    text-decoration: none;
    font-weight: 500;
    transition: opacity 0.2s;
}

.nav-links a:hover {
    opacity: 0.8;
    text-decoration: none;
}

@media (max-width: 576px) {
    .nav-container {
        flex-direction: column;
        padding: 0.8rem;
    }
    
    .logo {
        margin-bottom: 0.5rem;
    }
    
    .nav-links li {
        margin: 0 0.75rem;
    }
}

/* Update state portal styles */
.state-portal-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1.5rem;
}

.state-portal-list li {
    margin: 0;
    padding: 0;
}

.state-portal-list .state-card {
    height: 100%;
    display: flex;
}

.state-portal-list .state-card a {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
    padding: 1.5rem;
}

.state-portal-list h3 {
    margin: 0 0 0.5rem 0;
    color: #0056b3;
    font-size: 1.3rem;
}

.state-portal-list p {
    margin: 0 0 1rem 0;
    color: #666;
    font-size: 0.9rem;
    flex-grow: 1;
}

.state-portal-list .state-link {
    align-self: flex-start;
    color: #0056b3;
    font-weight: 500;
    font-size: 0.9rem;
}
'''
    
    with open('output/assets/css/style.css', 'a') as f:
        f.write(nav_styles)

# Update the state portal page generation to use the correct CSS path
state_portal_html = Environment().from_string(state_portal_template).render(
    states=states_list,
    current_year=current_year
)

with open('output/states/index.html', 'w') as f:
    f.write(state_portal_html) 