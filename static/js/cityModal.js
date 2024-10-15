// static/js/cityModal.js

document.addEventListener('DOMContentLoaded', function() {
    var cityModal = document.getElementById('city-modal');
    var citySlug = "{{ city_slug|default:'' }}";

    if (!citySlug && cityModal) {
        // The modal will be shown by the template script when needed
        // No need to do anything here
    }

    // Handler for the "Select City" button if it exists
    var selectCityButton = document.getElementById('select-city');
    if (selectCityButton) {
        selectCityButton.addEventListener('click', function(event) {
            event.preventDefault();
            if (cityModal) {
                cityModal.style.display = 'block';
            }
        });
    }

    // Close the modal when clicking outside of it
    window.onclick = function(event) {
        if (event.target == cityModal) {
            cityModal.style.display = "none";
        }
    }
});