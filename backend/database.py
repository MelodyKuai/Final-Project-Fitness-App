from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB
from models import User, Record
import bcrypt
from datetime import datetime

class Database:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB]
        self.users = self.db.users
        self.records = self.db.records

    # User operations
    def create_user(self, name, password, email):
        """Create a new user with hashed password"""
        if self.users.find_one({'email': email}):
            return None
        
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_data = {
            'name': name,
            'password': hashed,
            'email': email
        }
        result = self.users.insert_one(user_data)
        return User.from_db_object({'_id': result.inserted_id, **user_data})

    def get_user_by_email(self, email):
        """Get user by email"""
        user_data = self.users.find_one({'email': email})
        return User.from_db_object(user_data)

    def get_user_by_id(self, user_id):
        """Get user by ID"""
        user_data = self.users.find_one({'_id': user_id})
        return User.from_db_object(user_data)

    def verify_password(self, email, password):
        """Verify user password"""
        user = self.get_user_by_email(email)
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
            return user
        return None

    # Record operations
    def create_record(self, creator_id, name, imgData, duration, created_time=None):
        """Create a new record"""
        record_data = {
            'creator': creator_id,
            'name': name,
            'imgData': imgData,
            'duration': duration,
            'created_time': created_time if created_time else datetime.now()
        }
        result = self.records.insert_one(record_data)
        return Record.from_db_object({'_id': result.inserted_id, **record_data})

    def get_user_records(self, user_id):
        """Get all records for a specific user"""
        cursor = self.records.find({'creator': user_id})
        return [Record.from_db_object(record) for record in cursor]

    def get_record(self, record_id, user_id):
        """Get a specific record if user is the creator"""
        record_data = self.records.find_one({'_id': record_id, 'creator': user_id})
        return Record.from_db_object(record_data)

    def update_record(self, record_id, user_id, **updates):
        """Update a record if user is the creator"""
        result = self.records.update_one(
            {'_id': record_id, 'creator': user_id},
            {'$set': updates}
        )
        return result.modified_count > 0

    def delete_record(self, record_id, user_id):
        """Delete a record if user is the creator"""
        result = self.records.delete_one({'_id': record_id, 'creator': user_id})
        return result.deleted_count > 0

# Create global database instance
db = Database() 