
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
