
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
