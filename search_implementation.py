"""
SEARCH FUNCTIONALITY IMPLEMENTATION GUIDE

Follow these steps to add search functionality to your scissor lift rental directory website:

1. CREATE SEARCH DATA FILE
------------------------
Create a JSON file at 'output/assets/data/search-data.json' with the following structure:

```json
{
  "cities": [
    {
      "name": "City Name",
      "state": "State Name",
      "url": "state-slug/city-slug/"
    }
  ],
  "zips": [
    {
      "code": "12345",
      "city": "City Name",
      "state": "State Name",
      "url": "state-slug/city-slug/"
    }
  ]
}
```

2. ADD SEARCH JAVASCRIPT
----------------------
Create a file at 'output/assets/js/search-handler.js' with the following code:

```javascript
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
```

3. ADD SEARCH CSS
--------------
Add the following CSS to your style.css file:

```css
.search-container {
    max-width: 600px;
    margin: 0 auto 20px;
    position: relative;
}
.search-form {
    display: flex;
    flex-wrap: wrap;
}
.search-input {
    flex: 1;
    min-width: 200px;
    padding: 12px 15px;
    border: none;
    border-radius: 4px 0 0 4px;
    font-size: 1rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
.search-button {
    padding: 12px 20px;
    background-color: #28a745;
    color: white;
    border: none;
    border-radius: 0 4px 4px 0;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.2s;
}
.search-button:hover {
    background-color: #218838;
}
.search-results {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    margin-top: 5px;
    z-index: 10;
    display: none;
}
.search-results-list {
    list-style: none;
}
.search-results-list li {
    padding: 10px 15px;
    border-bottom: 1px solid #f0f0f0;
}
.search-results-list li:last-child {
    border-bottom: none;
}
.search-results-list a {
    color: #0056b3;
    text-decoration: none;
    display: block;
}
.search-results-list a:hover {
    text-decoration: underline;
}
.search-error {
    padding: 15px;
    color: #721c24;
    background-color: #f8d7da;
    border-radius: 4px;
}
.search-loading {
    text-align: center;
    padding: 15px;
    display: none;
}
.search-loading::after {
    content: '';
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid #f3f3f3;
    border-top: 3px solid #0056b3;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
```

4. UPDATE HOMEPAGE HTML
--------------------
Add the search form to your homepage HTML:

```html
<header>
    <h1>Scissor Lift Rental Near Me</h1>
    <p>Find the best scissor lift rental companies in your area</p>
    
    <div class="search-container">
        <form id="search-form" class="search-form">
            <input type="text" id="search-input" class="search-input" placeholder="Enter city, state, or zip code" aria-label="Search">
            <button type="submit" class="search-button">
                <i class="fas fa-search"></i> Find Rentals
            </button>
        </form>
        <div id="search-results" class="search-results"></div>
        <div id="search-loading" class="search-loading"></div>
    </div>
</header>
```

5. INCLUDE THE JAVASCRIPT
----------------------
Add this line before the closing </body> tag:

```html
<script src="assets/js/search-handler.js"></script>
```

6. GENERATE SEARCH DATA
--------------------
Add code to your generate_site.py script to create the search data JSON file:

```python
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
os.makedirs('output/assets/data', exist_ok=True)
with open('output/assets/data/search-data.json', 'w') as f:
    json.dump(search_data, f)
```

This implementation will allow users to search for cities, states, or zip codes and be directed to the appropriate page.
""" 