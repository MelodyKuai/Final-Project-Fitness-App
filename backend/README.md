# Fitness Record Tracking System

A Flask-based REST API for tracking fitness records with user authentication and MongoDB integration.

## Features

- User registration and authentication
- CRUD operations for fitness records
- Creator-based access control
- MongoDB integration with environment variable configuration
- RESTful API endpoints

## Prerequisites

- Python 3.8+
- MongoDB
- pip (Python package manager)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
Create a `.env` file in the project root with the following variables:
```
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DB=fitness_tracker
FLASK_SECRET_KEY=your-secret-key-here
```
You can modify these values according to your MongoDB setup.

3. Run the application:
```bash
python app.py
```

## API Endpoints and Usage Examples

### Authentication

#### Register New User
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }'
```

#### Login
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

#### Logout
```bash
curl -X POST http://localhost:5000/api/logout \
  -H "Content-Type: application/json" \
  --cookie "session=your-session-cookie"
```

### Records

#### Create New Record
```bash
curl -X POST http://localhost:5000/api/records \
  -H "Content-Type: application/json" \
  --cookie "session=your-session-cookie" \
  -d '{
    "name": "Morning Run",
    "imgData": "base64_encoded_image_data_here",
    "duration": 30,
    "created_time": "2024-01-01T10:00:00"  # Optional, ISO format
  }'
```

Note: The `created_time` field is optional. If not provided, the current time will be used.
The `imgData` field should contain the base64 encoded image data.

#### Get All Records
```bash
curl -X GET http://localhost:5000/api/records \
  -H "Content-Type: application/json" \
  --cookie "session=your-session-cookie"
```

#### Get Specific Record
```bash
curl -X GET http://localhost:5000/api/records/record_id_here \
  -H "Content-Type: application/json" \
  --cookie "session=your-session-cookie"
```

#### Update Record
```bash
curl -X PUT http://localhost:5000/api/records/record_id_here \
  -H "Content-Type: application/json" \
  --cookie "session=your-session-cookie" \
  -d '{
    "name": "Evening Run",
    "imgData": "base64_encoded_image_data_here",
    "duration": 45
  }'
```

#### Delete Record
```bash
curl -X DELETE http://localhost:5000/api/records/record_id_here \
  -H "Content-Type: application/json" \
  --cookie "session=your-session-cookie"
```

## Important Notes

1. Replace `your-session-cookie` with the actual session cookie received after login
2. Replace `record_id_here` with the actual record ID
3. All record operations require authentication (valid session cookie)
4. The session cookie is automatically set in your browser when using the login endpoint
5. Records can only be accessed/modified by their creators

## Security Notes

- Passwords are hashed using bcrypt before storage
- Authentication is required for all record operations
- Records can only be accessed/modified by their creators