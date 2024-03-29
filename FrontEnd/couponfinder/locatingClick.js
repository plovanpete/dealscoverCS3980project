// Initialize the map
function initMap() {
  // Create a new map centered at a default location
  const map = new google.maps.Map(document.getElementById("map"), {
      center: { lat: -34.397, lng: 150.644 }, // Default center coordinates
      zoom: 8, // Default zoom level
  });

  // Create a search bar and link it to the input field
  const input = document.getElementById("searchInput");
  const searchBox = new google.maps.places.SearchBox(input);

  let markers = [];

  // Bias the searchBox results towards the map's viewport
  map.addListener("bounds_changed", () => {
    searchBox.setBounds(map.getBounds());
  });

  // Listen for a click event on the map
  map.addListener("click", (event) => {
    const latLng = event.latLng;
  
    // Reverse geocode the clicked location to get its address
    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({ location: latLng }, (results, status) => {
      if (status === google.maps.GeocoderStatus.OK) {
        if (results[0]) {
          let placeName = "Unnamed place"; // Default value
          // Iterate through address components to find the place name
          for (let i = 0; i < results[0].address_components.length; i++) {
            const component = results[0].address_components[i];
            if (component.types.includes("establishment")) {
              placeName = component.long_name;
              break; // Exit loop once place name is found
            }
          }
          console.log("Place name:", placeName); // Log the name of the place
  
          // Display the name of the place in the output container
          document.getElementById("output").innerText = placeName;
        } else {
          console.error("No results found");
        }
      } else {
        console.error("Geocoder failed due to:", status);
      }
    });
  });

  // Listen for changes in the search box input
  searchBox.addListener("places_changed", () => {
    const places = searchBox.getPlaces();
    if (places.length === 0) {
      return;
    }

    // Clear any existing markers
    markers.forEach((marker) => {
      marker.setMap(null);
    });
    markers = [];

    // For each place, add a marker and center the map on it
    const bounds = new google.maps.LatLngBounds();
    places.forEach((place) => {
      if (!place.geometry || !place.geometry.location) {
        console.log("Returned place contains no geometry");
        return;
      }
      const marker = new google.maps.Marker({
        map,
        title: place.name,
        position: place.geometry.location,
      });
      markers.push(marker);

      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }
    });
    map.fitBounds(bounds);
  });
}


