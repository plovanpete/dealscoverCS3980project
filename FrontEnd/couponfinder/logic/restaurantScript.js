
// Function to get and render all restaurants in the table of the HTML.
async function getAllRestaurants() {
    const response = await fetch('http://127.0.0.1:8000/allrestaurants/');
    const restaurants = await response.json();

    const tableBody = document.getElementById('restaurantTableBody');
    tableBody.innerHTML = ''; // Clear previous data

    restaurants.forEach(restaurant => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${restaurant._id}</td>
            <td>${restaurant.name}</td>
            <td>${restaurant.address}</td>
            <td>${restaurant.zipcode}</td>
            <td>
                <button type="button" class="btn btn-danger btn-sm" onclick="deleteRestaurant('${restaurant.name}', '${restaurant.address}')">Delete</button>
                <button type="button" class="btn btn-warning btn-sm" onclick="openupdateRestaurant('${restaurant.name}', '${restaurant.address}', '${restaurant.zipcode}')">Update</button>
                <button type="button" class="btn btn-primary" onclick="onViewCoupons('${restaurant._id}')">View Coupons</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}



// Function gets the JSON data of a singular restaurant by name and address
async function getRestaurantByNameAndAddress(name, address) {
    const response = await fetch(`http://127.0.0.1:8000/restaurants/${name}/${address}`);
    const restaurant = await response.json();
    console.log(restaurant);
    // Handle the restaurant data as needed
}


// Function creates a new restaurant
async function createRestaurant() {
    // Get the values from the form inputs
    const name = document.getElementById('nameInput').value;
    const address = document.getElementById('addressInput').value;
    const zipcode = document.getElementById('zipcodeInput').value;

    // Check if any of the required fields is empty
    if (!name || !address || !zipcode) {
        alert("Please fill in all the required fields!");
        return;
    }

    const response = await fetch('http://127.0.0.1:8000/restaurants', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: name,
            address: address,
            zipcode: zipcode,
        }),
    });

    if (!response.ok) {
        const message = `An error has occurred: ${response.status}`;
        throw new Error(message);
    }

    const insertedRestaurant = await response.json();
    console.log(insertedRestaurant);
    window.location.reload();
    // Update the list of restaurants here, if necessary
}

// Add an event listener to the form to handle the submit event
document.getElementById('addRestaurantForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission
    createRestaurant();
});

document.getElementById('updateRestaurantForm').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent the default form submission
    await updateRestaurant();
});

// Function updates the JSON data of the restaurant.
async function updateRestaurant() {
    const name = document.getElementById('updateNameInput').value;
    const address = document.getElementById('updateAddressInput').value;
    const zipcode = document.getElementById('updateZipcodeInput').value;
    const newName = document.getElementById('newName').value;
    const newAddress = document.getElementById('newAddress').value;
    const newZipcode = document.getElementById('newZipcode').value;

    // Check if any of the required fields is empty
    if (!name || !address || !zipcode || (!newName && !newAddress && !newZipcode)) {
        alert("Please fill in the required fields!");
        return;
    }

    const response = await fetch(`http://127.0.0.1:8000/restaurants/${name}/${address}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: newName,
            address: newAddress,
            zipcode: newZipcode,
        }),
    });

    const result = await response.json();
    
    // Check if restaurant is not found
    if (response.status === 404) {
        alert(`Restaurant with Name '${name}' and Address '${address}' not found!`);
        return;
    }

    console.log(result);
    window.location.reload();
}


// Function to delete a restaurant by name and address
async function deleteRestaurant(name, address) {
    const response = await fetch(`http://127.0.0.1:8000/restaurants/${name}/${address}`, {
        method: 'DELETE',
    });
    const result = await response.json();
    console.log(result);
    window.location.reload();
    // Handle the result data as needed
}

// Coupon Section --------------------------------------------------------------------

// Function to fetch coupons for a specific restaurant
async function getCouponsForRestaurant(restaurantId) {
    const response = await fetch(`http://127.0.0.1:8000/restaurants/${restaurantId}/couponlist/`);
    const coupons = await response.json();
    return coupons;
}

// Function to display coupons in a modal
async function showCouponsModal(restaurantId) {
    const coupons = await getCouponsForRestaurant(restaurantId);

    const modalBody = document.getElementById('couponModalBody');

    coupons.forEach(coupon => {
        const couponItem = document.createElement('div');
        couponItem.classList.add('coupon-item');
        couponItem.innerHTML = `
            <span>${coupon.title}</span>
            <p>${coupon.description}</p>
        `;
        modalBody.appendChild(couponItem);
    });

    // Show the modal
    $('#couponModal').modal('show');
}

// Function to handle click event of "View Coupons" button for a restaurant
async function onViewCoupons(restaurantId) {
    showCouponsModal(restaurantId);
}




document.addEventListener('DOMContentLoaded', getAllRestaurants);
