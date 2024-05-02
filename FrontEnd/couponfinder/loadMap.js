let map; // Declare map as a global variable
let markers = [];

// Initialize the map
async function initMap() {
  // Create a new map centered at a default location
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 41.66, lng: -91.53 }, // Default center coordinates
    zoom: 8, // Default zoom level
  });

  // Create a search bar and link it to the input field
  const input = document.getElementById("searchInput");
  const searchBox = new google.maps.places.SearchBox(input, {
    types: ["restaurant"] // Limit search results to restaurants
  });

  // Bias the searchBox results towards the map's viewport
  map.addListener("bounds_changed", () => {
    searchBox.setBounds(map.getBounds());
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

      // Add click event listener to the marker
      marker.addListener("click", () => {
        document.getElementById("output").innerText = place.name;
      });

      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }
    });
    map.fitBounds(bounds);
  });

  // Listen for changes in the input field
  input.addEventListener("input", () => {
    document.getElementById("output").innerText = input.value;
  });
}

// Asynchronously load the Google Maps JavaScript API
async function loadMapScript() {
  const script = document.createElement("script");
  script.src = `https://maps.googleapis.com/maps/api/js?key=AIzaSyBRrTFJpK4ZqpjHwMF45OUdwwhRH0D_e5Y &libraries=places&callback=initMap&loading=async`;
  script.defer = true;
  document.body.appendChild(script);
}

// Fetch and display restaurant details based on selected location
async function fetchRestaurantDetails(latitude, longitude) {
  try {
      // Make an HTTP GET request to the /restaurant endpoint with latitude and longitude parameters
      const response = await fetch(`/restaurant?latitude=${latitude}&longitude=${longitude}`);
      const restaurant = await response.json();

      // Update restaurant details in HTML
      document.getElementById('restaurantName').innerText = restaurant.name;
      document.getElementById('restaurantAddress').innerText = restaurant.address;
  } catch (error) {
      console.error('Error fetching restaurant details:', error);
  }
}


// Call the function to load the map script asynchronously
loadMapScript();
