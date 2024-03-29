// Function gets the JSON data of coupons
async function getCoupons() {
    const response = await fetch('http://127.0.0.1:8000/coupons/');
    const coupons = await response.json();

    console.log(coupons);
    document.getElementById('output').innerText = JSON.stringify(coupons);
}

// Function gets the JSON data of a singular coupon, either by the ID or Name.
async function getCouponByIdOrName() {
    const idOrName = document.getElementById('couponIdOrName').value;

    const response = await fetch(`http://127.0.0.1:8000/coupons/${idOrName}`);
    const coupon = await response.json();

    console.log(coupon);
    document.getElementById('output').innerText = JSON.stringify(coupon);
}

// Function creates the JSON data of coupon.
async function createCoupon() {
    const title = document.getElementById('couponTitle').value;
    const description = document.getElementById('couponDescription').value;

    const response = await fetch('http://127.0.0.1:8000/coupons', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            title: title,
            description: description,
        }),
    });

    const result = await response.json();
    console.log(result);

    // Update the table after creating a new coupon
    getAllCoupons();

    // Clear input fields
    document.getElementById('couponTitle').value = '';
    document.getElementById('couponDescription').value = '';
    document.getElementById('couponIdOrName').value = '';
    document.getElementById('updateTitle').value = '';
    document.getElementById('updateDescription').value = '';

     // Message saying that Coupon was created
    document.getElementById('output').innerText = "Coupon created successfully!";
}

// Function updates the JSON data of the coupon.
async function updateCoupon() {
    const idOrName = document.getElementById('couponIdOrName').value;
    const newTitle = document.getElementById('updateTitle').value;
    const newDescription = document.getElementById('updateDescription').value;

    // Check if any of the required fields is empty
    if (!idOrName || (!newTitle && !newDescription)) {
        alert("Please fill in what you want to update!");
        return;
    }


    const response = await fetch(`http://127.0.0.1:8000/coupons/${idOrName}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            title: newTitle,
            description: newDescription,
        }),
    });

    const result = await response.json();
    
     // Check if coupon is not found
     if (response.status === 404) {
        alert(`Coupon with ID or Name '${idOrName}' not found!`);
        return;
    }

    console.log(result);

    // Update the table after updating the coupon
    getAllCoupons();

    // Clear input fields
    document.getElementById('couponTitle').value = '';
    document.getElementById('couponDescription').value = '';
    document.getElementById('couponIdOrName').value = '';
    document.getElementById('updateTitle').value = '';
    document.getElementById('updateDescription').value = '';

    // Displays update message
    displayMessage(result.msg);
}

// Function deletes data of the coupon
async function deleteCoupon() {
    const idOrNameToDelete = document.getElementById('couponIdOrName').value;

    // Check if input field is empty
    if (!idOrNameToDelete) {
        alert("Please fill what you want to delete!");
        return;
    }

    const response = await fetch(`http://127.0.0.1:8000/coupons/${idOrNameToDelete}`, {
        method: 'DELETE',
    });

    const result = await response.json();

    // Check if coupon is not found
    if (response.status === 404) {
        alert(`Coupon with ID or Name '${idOrNameToDelete}' not found!`);
        return;
    }

    console.log(result);

    // Update the table after deleting the coupon
    getAllCoupons();

    // Clear input fields
    document.getElementById('couponTitle').value = '';
    document.getElementById('couponDescription').value = '';
    document.getElementById('couponIdOrName').value = '';
    document.getElementById('updateTitle').value = '';
    document.getElementById('updateDescription').value = '';

    // Display delete message
    displayMessage(result.msg);
}

// Function gets and renders all coupons in the table of the HTML.
async function getAllCoupons() {
    const response = await fetch('http://127.0.0.1:8000/coupons/');
    const coupons = await response.json();

    const tableBody = document.getElementById('couponsTableBody');
    tableBody.innerHTML = ''; // Clear previous data

    coupons.forEach(coupon => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${coupon.id}</td>
            <td>${coupon.title}</td>
            <td>${coupon.description}</td>
        `;
        tableBody.appendChild(row);
    });
}

// Function to display messages in the output div
function displayMessage(message) {
    const outputDiv = document.getElementById('output');
    outputDiv.innerText = message || "Something went Wrong."; // Display a default message if 'message' is undefined
}

// Updates the page each time it's refreshed or re-opened.
document.addEventListener('DOMContentLoaded', getAllCoupons);

