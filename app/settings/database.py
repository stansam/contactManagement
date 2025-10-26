from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from app.settings.config import Config
import certifi
from flask import current_app

class Database:
    client = None
    db = None

    @staticmethod
    def initialize():
        if Database.client is None:
            Database.client = MongoClient(Config.MONGO_URI, server_api=ServerApi('1'), tlsCAFile=certifi.where())
            Database.db = Database.client["flask_mongodb_assignment"]
            print(f"✅ Connected to MongoDB Atlas database 'flask_mongodb_assignment'")
        else:
            print("⚠️ MongoDB already initialized.")

    @staticmethod
    def create_indexes():
        # User collection indexes
        users = Database.db['users']
        users.create_index("username", unique=True)
        users.create_index("email", unique=True)
        
        # Contact collection indexes
        contacts = Database.db['contacts']
        contacts.create_index("registration_number", unique=True)
        contacts.create_index("user_id")
        
        print("✅ Database indexes created")        

    @staticmethod
    def get_collection(collection_name):
        return Database.db[collection_name]

# Database.client = MongoClient(Config.MONGO_URI)
#         Database.db = Database.client["flask_mongodb_assignment"]