// Function to get and render all restaurants in the table of the HTML.
async function getAllRestaurants() {
    const response = await fetch('http://127.0.0.1:8000/allrestaurants/');
    const restaurants = await response.json();

    const tableBody = document.getElementById('restaurantTableBody');
    tableBody.innerHTML = ''; // Clear previous data

    restaurants.forEach(restaurant => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${restaurant.name}</td>
            <td>${restaurant.address}</td>
            <td>${restaurant.zipcode}</td>
            <td>
                <button type="button" class="btn btn-danger btn-sm" onclick="deleteRestaurant('${restaurant.name}', '${restaurant.address}')">Delete</button>
                <button type="button" class="btn btn-warning btn-sm" onclick="openupdateRestaurant('${restaurant.name}', '${restaurant.address}', '${restaurant.zipcode}')">Update</button>
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
async function createRestaurant(name, address, zipcode) {
    const response = await fetch('http://127.0.0.1:8000/restaurants/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id: id,
            name: name,
            address: address,
            zipcode: zipcode,
        }),
    });
    const insertedRestaurant = await response.json();
    console.log(insertedRestaurant);
    getAllRestaurants();
    // Handle the formatted restaurant data as needed
}



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
}


// Function to delete a restaurant by name and address
async function deleteRestaurant(name, address) {
    const response = await fetch(`http://127.0.0.1:8000/restaurants/${name}/${address}`, {
        method: 'DELETE',
    });
    const result = await response.json();
    console.log(result);
    getAllRestaurants();
    // Handle the result data as needed
}




document.addEventListener('DOMContentLoaded', getAllRestaurants);
