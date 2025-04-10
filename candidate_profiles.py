import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

if __name__ == '__main__':
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)
    db = client["app-dev"]
    collection = db["profiles"]

    profiles = list(collection.find({}, {"_id": 0, "profileImage": 0, "seoImage": 0}))
    print(f'total profiles fetch: {len(profiles)}')
