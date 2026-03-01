document.addEventListener('DOMContentLoaded', function() {
    // JavaScript for handling map interactions and AJAX requests

    // Example function to handle form submission
    document.getElementById('pollution-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        
        fetch('/api/report_pollution', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Pollution report submitted successfully!');
            } else {
                alert('Error submitting report.');
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // Example function to initialize map
    function initMap() {
        const map = L.map('map').setView([51.505, -0.09], 13); // Example coordinates
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
        }).addTo(map);
    }

    initMap();
});