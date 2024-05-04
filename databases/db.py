from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection URL
url = 'mongodb+srv://admin:dealscover1@dealscovercluster.bxpq8ph.mongodb.net/'
dbName = 'userDB'  # This will create the database if it doesn't already exist

async def get_mongo_client() -> AsyncIOMotorClient:
    try:
        client = AsyncIOMotorClient(url)
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise


async def get_db():
    client = await get_mongo_client()
    db = client[dbName]
    return db

