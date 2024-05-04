// Function to fetch coupons for a specific restaurant
async function getCouponsForRestaurant(restaurantId) {
    const response = await fetch(`http://127.0.0.1:8000/restaurants/${restaurantId}/couponlist/`);
    const coupons = await response.json();
    return coupons;
}
// Function to display coupons in a modal with delete buttons
async function showCouponsModal(restaurantId) {
    const coupons = await getCouponsForRestaurant(restaurantId);
    const modalBody = document.getElementById('couponModalBody');
    modalBody.innerHTML = ''; // Clear previous data

    coupons.forEach(coupon => {
        const couponItem = document.createElement('div');
        couponItem.classList.add('coupon-item');
        couponItem.innerHTML = `
            <span>${coupon.title}</span>
            <p>${coupon.description}</p>
            <button onclick="deleteCoupon('${restaurantId}', '${coupon.title}')">Delete</button>
        `;
        modalBody.appendChild(couponItem);
    });

    // Show the modal
    $('#couponModal').modal('show');
}

// Function to handle click event of "View Coupons" button for a restaurant
async function onViewCoupons(restaurantId) {
    // Set the restaurantId input field
    const restaurantIdInput = document.getElementById('restaurantIdInput');
    restaurantIdInput.value = restaurantId;

    // Display the coupons modal
    showCouponsModal(restaurantId);
}


// Function to add a coupon
async function addCoupon(restaurantId, title, description) {
    const response = await fetch(`http://127.0.0.1:8000/restaurants/${restaurantId}/coupons/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            title: title,
            description: description,
            restaurant_id: restaurantId
        })
    });

    if (response.ok) {
        // Reload coupons after adding
        await showCouponsModal(restaurantId);
    } else {
        const errorData= await response.json()
        console.error('Failed to add coupon', errorData);
    }
}

// Function to delete a coupon by restaurant ID and title
async function deleteCoupon(restaurantId, couponTitle) {
    const response = await fetch(`http://127.0.0.1:8000/restaurants/${restaurantId}/coupons/${encodeURIComponent(couponTitle)}`, {
        method: 'DELETE'
    });

    if (response.ok) {
        console.log('Coupon deleted successfully');
        await showCouponsModal(restaurantId); // Refresh the coupons list
    } else {
        const errorData = await response.json();
        console.error('Failed to delete coupon', errorData);
    }
}

// Add event listener to the document when it's loaded
document.addEventListener('DOMContentLoaded', () => {
    const confirmAddCouponBtn = document.getElementById('confirmAddCouponBtn');

    confirmAddCouponBtn.addEventListener('click', async () => {
        // Prevent default form submission
        event.preventDefault();

        // Get the values from the form inputs
        const title = document.getElementById('titleInput').value;
        const description = document.getElementById('descriptionInput').value;
        const restaurantId = document.getElementById('restaurantIdInput').value.trim(); // Get the Restaurant ID from the input field

        // Call the addCoupon function with the provided values
        await addCoupon(restaurantId, title, description);

        // Clear form inputs after submission (optional)
        document.getElementById('titleInput').value = '';
        document.getElementById('descriptionInput').value = '';

        // Hide the modal
        $('#addCouponModal').modal('hide');
    });

    // Optional: Add an event listener to reset the form after the modal is closed
    $('#addCouponModal').on('hidden.bs.modal', () => {
        document.getElementById('titleInput').value = '';
        document.getElementById('descriptionInput').value = '';
        const restaurantId = document.getElementById('restaurantIdInput').value.trim();
        showCouponsModal(restaurantId);
    });
});


