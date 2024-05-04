from fastapi import APIRouter, HTTPException, status, Depends
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List
from ..models.CouponModel import Coupon, CouponRequest
from databases.db import get_mongo_client

coupons_router = APIRouter()

# Function to get the coupons collection from MongoDB
async def get_coupons_collection(client: AsyncIOMotorClient) -> AsyncIOMotorCollection:
    return client["dealscover"]["couponordeal"]

# Function to get all coupons
@coupons_router.get("/coupons/", response_model=List[Coupon])
async def get_coupons(client: AsyncIOMotorClient = Depends(get_mongo_client)):
    coupons_collection = await get_coupons_collection(client)
    coupons = await coupons_collection.find().to_list(1000)  # Adjust the limit as needed
    return coupons

# Function to get coupons for a specific restaurant
@coupons_router.get("/restaurants/{restaurant_id}/couponlist/", response_model=List[Coupon])
async def get_coupons_for_restaurant(restaurant_id: str, client: AsyncIOMotorClient = Depends(get_mongo_client)):
    coupons_collection = await get_coupons_collection(client)
    coupons = await coupons_collection.find({"restaurant_id": ObjectId(restaurant_id)}).to_list(1000)  # Adjust the limit as needed
    return coupons

# Function to create a Coupon
@coupons_router.post("/restaurants/{restaurant_id}/coupons/", response_model=Coupon, status_code=status.HTTP_201_CREATED)
async def create_coupon(restaurant_id: str, coupon: CouponRequest, client: AsyncIOMotorClient = Depends(get_mongo_client)) -> Coupon:
    coupons_collection = await get_coupons_collection(client)
    coupon_data = jsonable_encoder(coupon)
    coupon_data["restaurant_id"] = ObjectId(restaurant_id)  # Add restaurant_id to the coupon data
    result = await coupons_collection.insert_one(coupon_data)
    inserted_coupon = await coupons_collection.find_one({"_id": result.inserted_id})

    # Convert the inserted_coupon document to a CouponResponse model
    return Coupon(**inserted_coupon)

# Function to get a coupon by ID
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

# Function to update a coupon
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

# Function to delete a coupon by restaurant ID and coupon title
@coupons_router.delete("/restaurants/{restaurant_id}/coupons/{coupon_title}")
async def delete_coupon_by_title(restaurant_id: str, coupon_title: str, client: AsyncIOMotorClient = Depends(get_mongo_client)):
    coupons_collection = await get_coupons_collection(client)
    result = await coupons_collection.delete_one({"restaurant_id": ObjectId(restaurant_id), "title": coupon_title})
    if result.deleted_count == 1:
        return {"msg": f"Coupon with title: {coupon_title} for restaurant ID: {restaurant_id} was successfully deleted!"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The coupon with title='{coupon_title}' for restaurant ID='{restaurant_id}' is not found")



