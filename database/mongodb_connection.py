import os
from pymongo import MongoClient


def get_mongodb_collection(logger):
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

    client = MongoClient(mongo_uri)

    db = client["lorawan_db"]

    collection = db["uplinks"]

    logger.info("Connected to MongoDB successfully")

    return collection