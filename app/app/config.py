import os

from pymongo import MongoClient

mongo = MongoClient(
    os.getenv("MONGO_URL")
)

mongo_collection = mongo.data.data

config = {"teams": [{"name": "admin", "password": "12345"}]}
