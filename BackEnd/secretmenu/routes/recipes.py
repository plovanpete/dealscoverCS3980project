from fastapi import APIRouter, HTTPException, status, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from ..model.RecipeModel import RecipeRequest
from databases.db import get_mongo_client
from BackEnd.gcs_imageuploading.gcs_utils import upload_image_to_gcs
import logging
import shutil



recipes_router = APIRouter()

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Connect to MongoDB
async def get_recipes_collection(client: AsyncIOMotorClient) -> AsyncIOMotorCollection:
    return client["dealscover"]["recipes"]

# Uploads an Image up to the browser.
@recipes_router.post("/upload/")
async def upload_file_handler(file: UploadFile = File(...)):
    # Save the file to local filesystem
    with open(file.filename, "rb") as f:
        f.write(await file.read())

    # Upload the file to Google Cloud Storage
    upload_image_to_gcs("dealscover", file.filename, file.filename)

    return {"filename": file.filename, "message": "File uploaded successfully"}
    
# Function to create a recipe
@recipes_router.post("/recipes/", status_code=status.HTTP_201_CREATED)
async def create_recipe(recipe: RecipeRequest, client: AsyncIOMotorClient = Depends(get_mongo_client)) -> dict:
    recipes_collection = await get_recipes_collection(client)
    result = await recipes_collection.insert_one(recipe.dict())
    inserted_recipe = await recipes_collection.find_one({"_id": result.inserted_id})

    formatted_recipe = {
        "_id": str(inserted_recipe["_id"]),
        "title": inserted_recipe["title"],
        "description": inserted_recipe["description"],
        "image_url": inserted_recipe.get("image_url", "")  # Added image_url field
    }

    logging.info(f'Recipe created: {formatted_recipe["title"]} - {formatted_recipe["description"]}')
    return formatted_recipe

# Function to get all recipes
@recipes_router.get("/allrecipes/")
async def get_all_recipes(client: AsyncIOMotorClient = Depends(get_mongo_client)):
    recipes_collection = await get_recipes_collection(client)
    recipes = await recipes_collection.find().to_list(1000)
    return [remove_id_from_document(recipe) for recipe in recipes]

# Function to get a recipe by title
@recipes_router.get("/recipes/{title}")
async def get_recipe_by_title(title: str, client: AsyncIOMotorClient = Depends(get_mongo_client)) -> dict:
    recipes_collection = await get_recipes_collection(client)
    recipe = await recipes_collection.find_one({"title": title})
    if recipe:
        return remove_id_from_document(recipe)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The recipe with title '{title}' is not found",
        )

# Function to update a recipe
@recipes_router.put("/recipes/{title}")
async def update_recipe(
    title: str, updated_recipe: RecipeRequest, client: AsyncIOMotorClient = Depends(get_mongo_client)
) -> dict:
    updated_recipe_dict = updated_recipe.dict()

    recipes_collection = await get_recipes_collection(client)
    result = await recipes_collection.update_many(
        {"title": title},
        {"$set": updated_recipe_dict}
    )

    if result.modified_count > 0:
        return {"message": f"Updated {result.modified_count} recipe(s) successfully!"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No recipes found with title '{title}'"
        )

# Function to delete a recipe by title
@recipes_router.delete("/recipes/{title}")
async def delete_recipe(title: str, client: AsyncIOMotorClient = Depends(get_mongo_client)):
    recipes_collection = await get_recipes_collection(client)
    result = await recipes_collection.delete_one({"title": title})
    if result.deleted_count == 1:
        logging.info(f'Recipe "{title}" was successfully deleted!')
        return {"message": f'Recipe "{title}" was successfully deleted!'}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The recipe with title '{title}' is not found",
        )

# Helper function to remove "_id" entry from the document
def remove_id_from_document(document: dict) -> dict:
    document.pop('_id', None)
    return document
