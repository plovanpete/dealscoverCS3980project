from fastapi import APIRouter, HTTPException, Path, status, Depends
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Annotated
from ..models.CouponModel import Coupon, CouponRequest
from databases.db import get_mongo_client


coupons_router = APIRouter()
# coupons_db: list[Coupon] = []

# Function to get the coupons collection from MongoDB
async def get_coupons_collection(client: AsyncIOMotorClient) -> AsyncIOMotorCollection:
    return client["dealscover"]["coupons"]

# Function to create a Coupon.
@coupons_router.post("/coupons", status_code=status.HTTP_201_CREATED)
async def create_coupon(coupon: CouponRequest, client: AsyncIOMotorClient = Depends(get_mongo_client)) -> dict:
    coupons_collection = await get_coupons_collection(client)
    coupon_data = jsonable_encoder(coupon)
    result = await coupons_collection.insert_one(coupon_data)
    inserted_coupon = await coupons_collection.find_one({"_id": result.inserted_id})

    # Extract the desired fields from the inserted_coupon document
    formatted_coupon = {
        "_id": str(inserted_coupon["_id"]),  # Convert ObjectId to string
        "title": inserted_coupon["title"],
        "description": inserted_coupon["description"],
        "couponid": inserted_coupon.get("couponid", ""),  # Assuming "couponid" is a field in CouponRequest
        "businessName": inserted_coupon["businessName"]
    }

    return formatted_coupon


# Function to get all coupons
@coupons_router.get("/coupons/")
async def get_coupons(client: AsyncIOMotorClient = Depends(get_mongo_client)):
    coupons_collection = await get_coupons_collection(client)
    coupons = await coupons_collection.find().to_list(1000)  # Adjust the limit as needed
    return coupons



# Function to get a coupon by either the ID or Name.
@coupons_router.get("/coupons/{coupon_id}")
async def get_coupon(
    coupon_id: str, client: AsyncIOMotorClient = Depends(get_mongo_client)
) -> dict:
    coupons_collection = await get_coupons_collection(client)
    coupon = await coupons_collection.find_one({"_id": ObjectId(coupon_id)})
    if coupon:
        return JSONResponse(coupon)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The coupon with ID={coupon_id} is not found")



# Function to update the coupon.
@coupons_router.put("/coupons/{coupon_id}")
async def update_coupon(
    coupon_id: str, updated_coupon: CouponRequest, client: AsyncIOMotorClient = Depends(get_mongo_client)
) -> dict:
    coupons_collection = await get_coupons_collection(client)
    updated_coupon_data = jsonable_encoder(updated_coupon)
    result = await coupons_collection.update_one({"_id": ObjectId(coupon_id)}, {"$set": updated_coupon_data})
    if result.modified_count == 1:
        return {"msg": "Updated Coupon successfully!"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The coupon with ID={coupon_id} is not found")




# Function to delete the coupon.
@coupons_router.delete("/coupons/{id}")
async def delete_coupon(coupon_id: str, client: AsyncIOMotorClient = Depends(get_mongo_client)):
    coupons_collection = await get_coupons_collection(client)
    result = await coupons_collection.delete_one({"_id": ObjectId(coupon_id)})
    if result.deleted_count == 1:
        return {"msg": f"Coupon with ID: {coupon_id} was successfully deleted!"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The coupon with ID={coupon_id} is not found")
