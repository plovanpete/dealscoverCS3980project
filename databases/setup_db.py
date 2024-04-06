from pymongo import MongoClient
import bcrypt
from databases.db import get_db

db = get_db()
client = MongoClient('mongodb+srv://admin:dealscover1@dealscovercluster.bxpq8ph.mongodb.net/')
db = client.userDB # `user_database` is the name of the database



def add_user(username, password, email, admin):
    users_collection = db.users  # `users` is the name of the collection

    # Hashing the password before storing it
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Creating a new user document
    user_document = {
        "username": username,
        "password": hashed_password,
        "email": email,
        "admin": 'Y' if admin else 'N'
    }

    # Inserting the user document into the collection
    result = users_collection.insert_one(user_document)
    print(f'Added user {username} with _id: {result.inserted_id}')