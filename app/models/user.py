import bcrypt
from app.settings.database import Database
from datetime import datetime
from flask_login import UserMixin
from bson import ObjectId

class User(UserMixin):
    COLLECTION = 'users'

    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.email = user_data['email']
        self.password = user_data['password']
        self.created_at = user_data.get('created_at')
    
    def get_id(self):
        return self.id

    @staticmethod
    def create_user(username, email, password):
        users = Database.get_collection(User.COLLECTION)
        # users.create_index("username", unique=True)
        # users.create_index("email", unique=True)

        # Check if user already exists
        if users.find_one({'$or': [{'username': username}, {'email': email}]}):
            return None

        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user = {
            'username': username,
            'email': email,
            'password': hashed_password,
            'created_at': datetime.utcnow()
        }

        result = users.insert_one(user)
        return result.inserted_id

    @staticmethod
    def get_by_id(user_id):
        users = Database.get_collection(User.COLLECTION)
        return users.find_one({'_id': ObjectId(user_id)})
    
    @staticmethod
    def find_by_username(username):
        users = Database.get_collection(User.COLLECTION)
        return users.find_one({'username': username})

    @staticmethod
    def find_by_email(email):
        users = Database.get_collection(User.COLLECTION)
        return users.find_one({'email': email})

    @staticmethod
    def verify_password(username, password):
        user_data = User.find_by_username(username)
        if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data['password']):
            return User(user_data)
        return None

    @staticmethod
    def update_password(email, new_password):
        users = Database.get_collection(User.COLLECTION)
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

        result = users.update_one(
            {'email': email},
            {'$set': {'password': hashed_password}}
        )
        return result.modified_count > 0
