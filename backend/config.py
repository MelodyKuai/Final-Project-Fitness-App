from datetime import timedelta
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# MongoDB Configuration
MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = os.getenv('MONGO_PORT', '27017')
MONGO_DB = os.getenv('MONGO_DB', 'fitness_tracker')
MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"

# Flask Configuration
class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)