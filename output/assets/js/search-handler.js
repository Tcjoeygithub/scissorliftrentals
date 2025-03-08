
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
