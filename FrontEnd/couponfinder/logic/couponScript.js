// Function gets the JSON data of coupons
async function getCoupons() {
    const response = await fetch('http://127.0.0.1:8000/coupons/');
    const coupons = await response.json();
    console.log(coupons);
    // Handle the coupons data as needed
}

// Function gets the JSON data of a singular coupon by ID
async function getCouponById(couponId) {
    const response = await fetch(`http://127.0.0.1:8000/coupons/${couponId}`);
    const coupon = await response.json();
    console.log(coupon);
    // Handle the coupon data as needed
}

// Function creates a new coupon
async function createCoupon(title, description) {
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
    const insertedCoupon = await response.json();
    
    // Extract the desired fields from the insertedCoupon object
    const formattedCoupon = {
        "_id": insertedCoupon._id,
        "title": insertedCoupon.title,
        "description": insertedCoupon.description,
        "couponid": insertedCoupon.couponid || "",
        "businessName": insertedCoupon.businessName
    };

    console.log(formattedCoupon);
    // Handle the formatted coupon data as needed
}


// Function updates an existing coupon
async function updateCoupon(couponId, updatedCouponData) {
    const response = await fetch(`http://127.0.0.1:8000/coupons/${couponId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedCouponData),
    });
    const result = await response.json();
    console.log(result);
    // Handle the result data as needed
}

// Function deletes a coupon by ID
async function deleteCoupon(couponId) {
    const response = await fetch(`http://127.0.0.1:8000/coupons/${couponId}`, {
        method: 'DELETE',
    });
    const result = await response.json();
    console.log(result);
    // Handle the result data as needed
}


// Function to display messages in the output div
function displayMessage(message) {
    const outputDiv = document.getElementById('output');
    outputDiv.innerText = message || "Something went Wrong."; // Display a default message if 'message' is undefined
}


