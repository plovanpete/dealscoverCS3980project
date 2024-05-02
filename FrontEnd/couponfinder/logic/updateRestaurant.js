// Function to open the update modal with pre-filled data
function openUpdateModal(name, address, zipcode) {
    // Populate the modal fields with existing data
    document.getElementById('updateNameInput').value = name;
    document.getElementById('updateAddressInput').value = address;
    document.getElementById('updateZipcodeInput').value = zipcode;

    console.log("Name:", name);
    console.log("Address:", address);
    console.log("Zipcode:", zipcode);
    // Open the modal
    $('#updateRestaurantModal').modal('show');
}

// Function to update a restaurant
async function openupdateRestaurant(name, address, zipcode) {
    // Open the update modal with pre-filled data
    openUpdateModal(name, address, zipcode);
}
