import logging
from fastapi import APIRouter, HTTPException, status, Depends, Path
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from bson import ObjectId
from ..model.RestaurantModel import RestaurantRequest
from databases.db import get_mongo_client

restaurants_router = APIRouter()

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to get the restaurants collection from MongoDB
async def get_restaurants_collection(client: AsyncIOMotorClient) -> AsyncIOMotorCollection:
    return client["dealscover"]["restaurants"]

# Function to create a Restaurant
@restaurants_router.post("/restaurants/", status_code=status.HTTP_201_CREATED)
async def create_restaurant(restaurant: RestaurantRequest, client: AsyncIOMotorClient = Depends(get_mongo_client)) -> dict:
    restaurants_collection = await get_restaurants_collection(client)
    result = await restaurants_collection.insert_one(restaurant.dict())  # Convert RestaurantRequest to dictionary
    inserted_restaurant = await restaurants_collection.find_one({"_id": result.inserted_id})

    # Extract the desired fields from the inserted_restaurant document
    formatted_restaurant = {
        "_id": str(inserted_restaurant["_id"]),  # Convert ObjectId to string
        "name": inserted_restaurant["name"],
        "address": inserted_restaurant["address"],
        "zipcode": inserted_restaurant["zipcode"]
    }

    # Logging
    logging.info(f'Restaurant created: {formatted_restaurant["name"]} at address {formatted_restaurant["address"]}. Zipcode: {formatted_restaurant["zipcode"]}')

    return formatted_restaurant



# Function to get all restaurants
@restaurants_router.get("/allrestaurants/")
async def get_restaurants(client: AsyncIOMotorClient = Depends(get_mongo_client)):
    restaurants_collection = await get_restaurants_collection(client)
    restaurants = await restaurants_collection.find().to_list(1000)  # Adjust the limit as needed
    return [remove_id_from_document(restaurant) for restaurant in restaurants]

# Function to get a restaurant by name and address
@restaurants_router.get("/restaurants/{name}/{address}")
async def get_restaurant_by_name_and_address(
    name: str, address: str, client: AsyncIOMotorClient = Depends(get_mongo_client)
) -> dict:
    restaurants_collection = await get_restaurants_collection(client)
    restaurant = await restaurants_collection.find_one({"name": name, "address": address})
    if restaurant:
        return remove_id_from_document(restaurant)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The restaurant with Name '{name}' and Address '{address}' is not found",
        )

# Function to update a restaurant
@restaurants_router.put("/restaurants/{name}/{address}")
async def update_restaurant(
    name: str, address: str, updated_restaurant: RestaurantRequest, client: AsyncIOMotorClient = Depends(get_mongo_client)
) -> dict:
    updated_restaurant_dict = updated_restaurant.dict()

    restaurants_collection = await get_restaurants_collection(client)
    result = await restaurants_collection.update_many(
        {"name": name, "address": address},
        {"$set": updated_restaurant_dict}
    )

    if result.modified_count > 0:
        return {"msg": f"Updated {result.modified_count} restaurant successfully!"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No restaurants found with name '{name}' and address '{address}'"
        )




# Function to delete a restaurant by name and address
@restaurants_router.delete("/restaurants/{name}/{address}")
async def delete_restaurant(name: str, address: str, client: AsyncIOMotorClient = Depends(get_mongo_client)):
    restaurants_collection = await get_restaurants_collection(client)
    result = await restaurants_collection.delete_one({"name": name, "address": address})
    if result.deleted_count == 1:
        logging.info(f'Restaurant "{name}" at address "{address}" was successfully deleted!')
        return {"msg": f'Restaurant "{name}" at address "{address}" was successfully deleted!'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The restaurant with name='{name}' and address='{address}' is not found")



# Helper function to remove "_id" entry from the document
def remove_id_from_document(document: dict) -> dict:
    if document and '_id' in document:
        document['_id'] = str(document['_id'])  # Convert ObjectId to string
    return document



