from datetime import datetime
from flask_login import UserMixin
from bson import ObjectId

class User(UserMixin):
    def __init__(self, id, name, password, email):
        self.id = id
        self.name = name
        self.password = password
        self.email = email

    @staticmethod
    def from_db_object(db_object):
        if db_object is None:
            return None
        return User(
            id=db_object['_id'],
            name=db_object['name'],
            password=db_object['password'],
            email=db_object['email']
        )

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'password': self.password
        }

class Record:
    def __init__(self, id, creator, name, imgData, duration, created_time=None):
        self.id = id
        self.creator = creator
        self.name = name
        self.imgData = imgData
        self.duration = duration
        self.created_time = created_time or datetime.now()

    @staticmethod
    def from_db_object(db_object):
        if db_object is None:
            return None
        return Record(
            id=db_object['_id'],
            creator=db_object['creator'],
            name=db_object['name'],
            imgData=db_object['imgData'],
            duration=db_object['duration'],
            created_time=db_object['created_time']
        )

    def to_dict(self):
        return {
            'id': str(self.id),
            'creator': str(self.creator),
            'name': self.name,
            'imgData': self.imgData,
            'duration': self.duration,
            'created_time': self.created_time.isoformat()
        } 