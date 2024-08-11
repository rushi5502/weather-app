import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_mongo_client():
    # Get MongoDB connection string from environment variable
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    return client

def get_database():
    client = get_mongo_client()
    # Replace 'weatherdata' with your actual database name
    db = client['weatherdata']
    return db

def get_collection(collection_name):
    db = get_database()
    collection = db[collection_name]
    return collection
