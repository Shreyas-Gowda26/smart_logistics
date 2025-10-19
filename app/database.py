from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017"
client = MongoClient(MONGO_URL)
db = client["smart_logistics"]

users_collection = db["users"]
deliveries_collection = db["deliveries"]
vehicles_collection = db["vehicles"]
tracking_collection = db["tracking"]
notifications_collection = db["notifications"]

