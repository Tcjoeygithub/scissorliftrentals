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
    var map = L.map('map').setView([mapData.center.lat, mapData.center.lng], mapData.zoom);
    
    // Add the OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    // Create markers for each location
    mapData.locations.forEach(function(location) {
        // Create a marker
        var marker = L.marker([location.lat, location.lng]).addTo(map);
        
        // Create the content for the popup
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
        
        // Add a popup to the marker
        marker.bindPopup(content);
    });
}

// Initialize the map when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Check if the Leaflet library is loaded
    if (typeof L !== 'undefined') {
        initMap();
    } else {
        console.error('Leaflet library not loaded');
    }
}); 