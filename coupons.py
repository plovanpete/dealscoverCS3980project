from fastapi import APIRouter, HTTPException, Path, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Annotated
from CouponModel import Coupon, CouponRequest

coupons_router = APIRouter()
coupons_db: list[Coupon] = []

# Function to create a Coupon.
@coupons_router.post("/coupons", status_code=status.HTTP_201_CREATED)
async def create_coupon(coupon: CouponRequest) -> Coupon:
    if len(coupons_db) == 0:
        id = 1
    else:
        id = max(coupons_db, key = lambda x: x.id).id + 1
    
    new_coupon = Coupon(id = id, title = coupon.title, description = coupon.description)
    coupons_db.append(new_coupon)
    json_coupon = new_coupon.model_dump()

    # Adds a message that the coupon was created.
    response_data = {
        "msg": f"Coupon '{coupon.title}' created successfully!",
        "coupon": json_coupon,
    }


    return JSONResponse(json_coupon, status_code = status.HTTP_201_CREATED)

# Function to get all coupons
@coupons_router.get("/coupons/")
async def get_coupons():
    json_coupons_db = jsonable_encoder(coupons_db)
    return json_coupons_db

# Function to get a coupon by either the ID or Name.
@coupons_router.get("/coupons/{id_or_name}")
async def get_coupon_by_id_or_name(
    id_or_name: Annotated[str, Path(title="The ID or Name to get")]
) -> dict:
    # Loops through the coupon list and finds JSON data of the coupon.
    for coupon in coupons_db:
        if str(coupon.id) == id_or_name or coupon.title == id_or_name:
            json_coupon = coupon.model_dump()
            return JSONResponse(json_coupon)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"The coupon with ID or Name={id_or_name} is not found",
    )

# Function to update the coupon.
@coupons_router.put("/coupons/{id_or_name}")
async def update_coupon(
    id_or_name: str, updated_coupon: CouponRequest
) -> dict:
    updated_coupon_dict = updated_coupon.dict()

    matching_indexes = []  # List to store indexes of matching coupons (duplicate coupons)

    # Check if id_or_name is a numeric value (ID) or a string (Name)
    try:
        id_or_name_val = int(id_or_name)
        # Updating by ID
        for i, coupon in enumerate(coupons_db):
            if coupon.id == id_or_name_val:
                matching_indexes.append(i)
    except ValueError:
        # Updating by Name
        for i, coupon in enumerate(coupons_db):
            if coupon.title == id_or_name:
                matching_indexes.append(i)

    if matching_indexes:
        # Updates the last matching (duplicate) coupon
        latest_index = max(matching_indexes)
        coupon_to_update = coupons_db[matching_indexes[0]]
        coupon_to_update.title = updated_coupon_dict.get("title", coupon_to_update.title)
        coupon_to_update.description = updated_coupon_dict.get("description", coupon_to_update.description)

        return {"msg": "Updated Coupon successfully!"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"The coupon with ID or Name={id_or_name} is not found",
    )



# Function to delete the coupon.
@coupons_router.delete("/coupons/{id_or_name}")
async def delete_coupon(id_or_name: Annotated[str, Path(title="The ID or Name to delete")]):
    for i, coupon in enumerate(coupons_db):
        if str(coupon.id) == id_or_name or coupon.title == id_or_name:
            coupons_db.pop(i)
            for j in range(i, len(coupons_db)):
                coupons_db[j].id -= 1
            return {"msg": f"Coupon with ID or Name: {id_or_name} was successfully deleted!"}

    return {"msg": f"Coupon with the id or name: {id_or_name} was not found."}
