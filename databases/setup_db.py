from pymongo import MongoClient
import bcrypt
from databases.db import get_db
from pymongo.errors import PyMongoError


db = get_db()
client = MongoClient('mongodb+srv://admin:dealscover1@dealscovercluster.bxpq8ph.mongodb.net/')
db = client.userDB # `user_database` is the name of the database



def add_user(username, password, email, admin):
    try:
        users_collection = db.users
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_document = {
            "username": username,
            "password": hashed_password,
            "email": email,
            "admin": 'Y' if admin else 'N'
        }
        result = users_collection.insert_one(user_document)
        print(f'Added user {username} with _id: {result.inserted_id}')
    except PyMongoError as e:
        print(f"An error occurred: {e}")

    # Inserting the user document into the collection
    result = users_collection.insert_one(user_document)
    print(f'Added user {username} with _id: {result.inserted_id}')