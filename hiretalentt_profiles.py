import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


class ProfileManager:
    def __init__(self):
        self.mongo_uri = os.getenv("MONGO_URI")
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client["app-dev"]
        self.collection = self.db["profiles"]

    def get_profiles(self):
        profiles = list(self.collection.find({}, {"_id": 0, "profileImage": 0, "seoImage": 0}))
        return profiles
        # print(f'total profiles fetch: {len(profiles)}')


# for testing...
if __name__ == '__main__':
    profile_manager = ProfileManager()
    all_profiles = profile_manager.get_profiles()
    print(all_profiles)
