async function getCoupons() {
    const response = await fetch('http://127.0.0.1:8000/coupons/');
    const coupons = await response.json();

    console.log(coupons);
    document.getElementById('output').innerText = JSON.stringify(coupons);
}

async function getCouponByIdOrName() {
    const idOrName = document.getElementById('couponIdOrName').value;

    const response = await fetch(`http://127.0.0.1:8000/coupons/${idOrName}`);
    const coupon = await response.json();

    console.log(coupon);
    document.getElementById('output').innerText = JSON.stringify(coupon);
}

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
}

async function updateCoupon() {
    const idOrName = document.getElementById('couponIdOrName').value;
    const newTitle = document.getElementById('updateTitle').value;
    const newDescription = document.getElementById('updateDescription').value;

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
    console.log(result);

    // Update the table after updating the coupon
    getAllCoupons();
}

async function deleteCoupon() {
    const idOrNameToDelete = document.getElementById('couponIdOrName').value;

    const response = await fetch(`http://127.0.0.1:8000/coupons/${idOrNameToDelete}`, {
        method: 'DELETE',
    });

    const result = await response.json();
    console.log(result);

    // Update the table after deleting the coupon
    getAllCoupons();
}


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


