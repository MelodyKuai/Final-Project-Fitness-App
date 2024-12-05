from flask import Flask, request, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_cors import CORS
from models import User
from database import db
from config import Config
from bson import ObjectId
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app, supports_credentials=True)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_user_by_id(ObjectId(user_id))

# Authentication routes
@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    user = db.create_user(
        name=data['name'],
        password=data['password'],
        email=data['email']
    )
    if user:
        return jsonify({'message': 'User registered successfully'}), 201
    return jsonify({'error': 'Email already exists'}), 400

@app.route('/api/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    user = db.verify_password(data['email'], data['password'])
    if user:
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    """Logout user"""
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

# Record routes
@app.route('/api/records', methods=['POST'])
@login_required
def create_record():
    """Create a new record"""
    data = request.get_json()
    created_time = None
    if 'created_time' in data:
        try:
            created_time = datetime.fromisoformat(data['created_time'])
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid created_time format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
            
    record = db.create_record(
        creator_id=current_user.id,
        name=data['name'],
        imgData=data['imgData'],
        duration=data['duration'],
        created_time=created_time
    )
    return jsonify({
        'message': 'Record created successfully',
        'record': record.to_dict()
    }), 201

@app.route('/api/records', methods=['GET'])
@login_required
def get_records():
    """Get all records for current user"""
    records = db.get_user_records(current_user.id)
    return jsonify({
        'records': [record.to_dict() for record in records]
    }), 200

@app.route('/api/records/<record_id>', methods=['GET'])
@login_required
def get_record(record_id):
    """Get a specific record"""
    record = db.get_record(ObjectId(record_id), current_user.id)
    if record:
        return jsonify(record.to_dict()), 200
    return jsonify({'error': 'Record not found'}), 404

@app.route('/api/records/<record_id>', methods=['PUT'])
@login_required
def update_record(record_id):
    """Update a record"""
    data = request.get_json()
    updates = {k: v for k, v in data.items() if k in ['name', 'imgData', 'duration']}
    
    if db.update_record(ObjectId(record_id), current_user.id, **updates):
        return jsonify({'message': 'Record updated successfully'}), 200
    return jsonify({'error': 'Record not found or unauthorized'}), 404

@app.route('/api/records/<record_id>', methods=['DELETE'])
@login_required
def delete_record(record_id):
    """Delete a record"""
    if db.delete_record(ObjectId(record_id), current_user.id):
        return jsonify({'message': 'Record deleted successfully'}), 200
    return jsonify({'error': 'Record not found or unauthorized'}), 404

if __name__ == '__main__':
    app.run(debug=True) 