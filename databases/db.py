from pymongo import MongoClient

# MongoDB connection URL
url = 'mongodb+srv://admin:dealscover1@dealscovercluster.bxpq8ph.mongodb.net/'
#password = dealscover1
dbName = 'userDB' # This will create the database if it doesn't already exist

client = MongoClient(url)

def get_db():
    db = client[dbName]
    return db
