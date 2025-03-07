import pandas as pd
import os
import re
import json
import requests
import statistics
from urllib.parse import urlparse, unquote
from jinja2 import Environment, FileSystemLoader

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

)

# Create CSS file
with open('output/assets/css/style.css', 'w') as f:
    f.write('''
    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
        color: #333;
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        background-color: #f9f9f9;
    }
    header {
        background-color: #0056b3;
        color: white;
        padding: 30px;
        margin-bottom: 30px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
    }
    header h1 {
        color: white;
        margin-bottom: 10px;
        font-size: 2.2em;
    }
    header p {
        font-size: 1.2em;
        opacity: 0.9;
        margin-bottom: 20px;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    h1, h2, h3 {
        color: #0056b3;
        margin: 20px 0 15px;
    }
    .breadcrumb {
        margin-bottom: 25px;
        background-color: #fff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        font-size: 1.1em;
    }
    .breadcrumb a {
        color: #0056b3;
        text-decoration: none;
        transition: color 0.2s;
    }
    .breadcrumb a:hover {
        text-decoration: underline;
        color: #003d7a;
    }
    .map-container {
        width: 100%;
        height: 400px;
        margin-bottom: 30px;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    #map {
        width: 100%;
        height: 100%;
    }
    .map-info-window {
        padding: 5px;
        max-width: 300px;
    }
    .map-info-window h3 {
        margin: 0 0 10px 0;
        color: #0056b3;
    }
    .map-info-window p {
        margin-bottom: 5px;
    }
    .map-info-window a {
        display: inline-block;
        padding: 5px 10px;
        background-color: #0056b3;
        color: white;
        text-decoration: none;
        border-radius: 4px;
        margin-top: 5px;
    }
    .company-card {
        border: none;
        border-radius: 8px;
        padding: 0;
        margin-bottom: 30px;
        background-color: #fff;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        overflow: hidden;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .company-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    .company-photo-container {
        position: relative;
        width: 100%;
        height: 200px;
        background-color: #e9ecef;
        overflow: hidden;
    }
    .company-photo {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
        transition: transform 0.3s;
    }
    .company-card:hover .company-photo {
        transform: scale(1.05);
    }
    .company-photo-placeholder {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #6c757d;
        font-size: 1.2em;
        background-color: #e9ecef;
    }
    .company-photo-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(to bottom, rgba(0,0,0,0) 50%, rgba(0,0,0,0.7) 100%);
    }
    .company-content {
        padding: 20px;
    }
    .company-name {
        font-size: 1.4em;
        font-weight: bold;
        color: #0056b3;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #f0f0f0;
    }
    .company-details {
        display: flex;
        flex-wrap: wrap;
        gap: 25px;
    }
    .company-info {
        flex: 1;
        min-width: 300px;
    }
    .company-contact {
        flex: 1;
        min-width: 300px;
    }
    .company-info p, .company-contact p {
        margin-bottom: 12px;
        line-height: 1.7;
    }
    .reviews {
        font-weight: bold;
        color: #28a745;
        background-color: #e8f5e9;
        padding: 3px 8px;
        border-radius: 4px;
        display: inline-block;
    }
    .state-list, .city-list {
        list-style: none;
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin: 20px 0;
    }
    .state-list li, .city-list li {
        margin-bottom: 12px;
    }
    .state-list a, .city-list a {
        display: inline-block;
        padding: 8px 15px;
        background-color: #fff;
        border-radius: 6px;
        text-decoration: none;
        color: #0056b3;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        transition: all 0.2s;
    }
    .state-list a:hover, .city-list a:hover {
        background-color: #0056b3;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .website-link {
        display: inline-block;
        padding: 8px 16px;
        background-color: #0056b3;
        color: white;
        text-decoration: none;
        border-radius: 4px;
        margin-top: 5px;
        transition: background-color 0.2s;
    }
    .website-link:hover {
        background-color: #003d7a;
    }
    .info-section {
        background-color: #fff;
        padding: 25px;
        border-radius: 8px;
        margin-bottom: 30px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .info-section h2 {
        color: #0056b3;
        margin-top: 0;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #f0f0f0;
    }
    .info-section ul {
        padding-left: 20px;
        margin-bottom: 20px;
    }
    .info-section li {
        margin-bottom: 8px;
    }
    footer {
        margin-top: 60px;
        padding: 25px 0;
        border-top: 1px solid #e9ecef;
        text-align: center;
        color: #6c757d;
        font-size: 0.9em;
    }
    .image-error {
        display: none;
    }
    @media (max-width: 768px) {
        .company-details {
            flex-direction: column;
        }
        .company-info, .company-contact {
            min-width: 100%;
        }
        .map-container {
            height: 300px;
        }
        .search-form {
            flex-direction: column;
        }
        .search-input {
            border-radius: 4px;
            margin-bottom: 10px;
        }
        .search-button {
            border-radius: 4px;
        }
    }
    ''')

# Set up Jinja2 templates
env = Environment(loader=FileSystemLoader('.'))

# Create homepage template with search functionality
homepage_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scissor Lift Rental Near Me | Find Local Scissor Lift Rentals</title>
    <meta name="description" content="Find scissor lift rentals near you. Browse our directory of scissor lift rental companies across the United States.">
    <link rel="stylesheet" href="assets/css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
</head>
<body>
    <header>
        <h1>Scissor Lift Rental Near Me</h1>
        <p>Find the best scissor lift rental companies in your area</p>
        
        
    </header>
    
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
        <p>&copy; {{ current_year }} Scissor Lift Rental Directory. All rights reserved.</p>
    </footer>
    
    
</body>
</html>'''

# Create state page template
state_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scissor Lift Rental in {{ state }} | Find Local Scissor Lift Rentals</title>
    <meta name="description" content="Find scissor lift rentals in {{ state }}. Browse our directory of scissor lift rental companies in {{ state }}.">
    <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>
    <header>
        <h1>Scissor Lift Rental in {{ state }}</h1>
        <p>Find the best scissor lift rental companies in {{ state }}</p>
    </header>
    
    <div class="breadcrumb">
        <a href="../">Home</a> &gt; {{ state }}
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
        
        <section>
            <h2>About Scissor Lift Rentals in {{ state }}</h2>
            <p>{{ state }} offers a wide range of scissor lift rental options for construction, maintenance, and industrial projects. Whether you need a scissor lift for indoor use or rough terrain applications, you'll find reliable rental companies throughout the state.</p>
            
            <h2>Popular Scissor Lift Brands in {{ state }}</h2>
            <p>Rental companies in {{ state }} typically offer scissor lifts from top manufacturers including:</p>
            <ul>
                <li>JLG</li>
                <li>Genie</li>
                <li>Skyjack</li>
                <li>Haulotte</li>
                <li>Snorkel</li>
            </ul>
        </section>
    </main>
    
    <footer>
        <p>&copy; {{ current_year }} Scissor Lift Rental Directory. All rights reserved.</p>
    </footer>
</body>
</html>'''

# Create city page template
city_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scissor Lift Rental in {{ city }}, {{ state }} | Find Local Scissor Lift Rentals</title>
    <meta name="description" content="Find scissor lift rentals in {{ city }}, {{ state }}. Compare top-rated scissor lift rental companies in {{ city }}.">
    <link rel="stylesheet" href="../../assets/css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <script src="../../assets/js/image-handler.js"></script>
</head>
<body>
    <header>
        <h1>Scissor Lift Rental in {{ city }}, {{ state }}</h1>
        <p>Find the best scissor lift rental companies in {{ city }}, {{ state }}</p>
    </header>
    
    <div class="breadcrumb">
        <a href="../../"><i class="fas fa-home"></i> Home</a> &gt; <a href="../">{{ state }}</a> &gt; {{ city }}
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
                <div class="company-card">
                    <div class="company-photo-container">
                        {% if company.photo %}
                        <img src="{{ company.photo }}" alt="{{ company.name }}" class="company-photo" onerror="handleImageError(this)">
                        <div class="company-photo-overlay"></div>
                        {% else %}
                        <div class="company-photo-placeholder">
                            <i class="fas fa-tools"></i> No Image Available
                        </div>
                        {% endif %}
                    </div>
                    <div class="company-content">
                        <div class="company-name">{{ company.name }}</div>
                        <div class="company-details">
                            <div class="company-info">
                                <p><strong><i class="fas fa-star"></i> Reviews:</strong> <span class="reviews">{{ company.reviews }}</span></p>
                                {% if company.Scissor_Lifts %}
                                <p><strong><i class="fas fa-truck"></i> Scissor Lifts:</strong> {{ company.Scissor_Lifts }}</p>
                                {% endif %}
                                {% if company.Scissor_Lift_Brands %}
                                <p><strong><i class="fas fa-tag"></i> Brands:</strong> {{ company.Scissor_Lift_Brands }}</p>
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
            <p>When renting a scissor lift in {{ city }}, consider your specific project requirements including height, weight capacity, and whether you need an electric or rough terrain model. Most rental companies offer daily, weekly, and monthly rates.</p>
            
            <h2>Safety Tips for Using Scissor Lifts</h2>
            <ul>
                <li>Always inspect the scissor lift before use</li>
                <li>Never exceed the weight capacity</li>
                <li>Keep the platform clean and free of debris</li>
                <li>Be aware of overhead obstructions</li>
                <li>Only operate on level surfaces unless using a rough terrain model</li>
                <li>Follow all manufacturer guidelines and safety protocols</li>
            </ul>
        </section>
    </main>
    
    <footer>
        <p>&copy; {{ current_year }} Scissor Lift Rental Directory. All rights reserved.</p>
    </footer>
    
    {% if map_data %}
    <!-- Google Maps API -->
    <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBNLrJhOMz6idD05pzfn5lhA-TAw-mAZCU&callback=initMap" async defer></script>
    <script src="../../assets/js/map-handler.js"></script>
    {% endif %}
</body>
</html>'''

# Generate the site
from datetime import datetime
current_year = datetime.now().year

print("Generating site structure...")

# Create homepage
states_with_companies = df[df['state_slug'] != ''][['us_state', 'state_slug']].drop_duplicates().sort_values('us_state')
states_list = [(state, slug) for state, slug in zip(states_with_companies['us_state'], states_with_companies['state_slug'])]

homepage_html = Environment().from_string(homepage_template).render(
    states=states_list,
    current_year=current_year
)

with open('output/index.html', 'w') as f:
    f.write(homepage_html)



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
        current_year=current_year
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
                'Scissor_Lifts': row['Scissor Lifts'],
                'Scissor_Lift_Brands': row['Scissor Lift Brands'],
                'Sizes_Available': row['Sizes Available'],
                'full_address': row['full_address'],
                'phone': row['phone'],
                'site': row['site'],
                'about': format_about(row['about']),
                'working_hours': format_hours(row['working_hours']),
                'photo': row['photo']
            })
        
        # Generate city page
        city_html = Environment().from_string(city_template).render(
            state=state,
            city=city,
            companies=companies,
            map_data=map_data,
            current_year=current_year
        )
        
        with open(f'output/{state_slug}/{city_slug}/index.html', 'w') as f:
            f.write(city_html)

print("Site generation complete! Output is in the 'output' directory.") 