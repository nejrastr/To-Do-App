from app import db
from datetime import datetime
from enum import Enum
from werkzeug.security import generate_password_hash,check_password_hash
import uuid

class PriorityEnum(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class Status(Enum):
    IN_PROGRESS = "In Progress"
    DONE = "Done"
    TBD = "To Be Done"

class Frequency(Enum):
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    YEARLY = "Yearly"

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default= lambda: str(uuid.uuid4()))
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password=generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    tasks = db.relationship('Task', backref='user', lazy=True)
    goals = db.relationship('Goal', backref='user', lazy=True)
    events = db.relationship('Event', backref='user', lazy=True)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.String(36), primary_key=True,default= lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    status = db.Column(db.Enum(Status))
    priority = db.Column(db.Enum(PriorityEnum))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Goal(db.Model):
    __tablename__ = 'goals'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)  
    description = db.Column(db.String(100), nullable=True)  
    start_date = db.Column(db.DateTime, default=datetime.utcnow)  
    end_date = db.Column(db.DateTime, default=datetime.utcnow)  
    priority = db.Column(db.Enum(PriorityEnum))
    status = db.Column(db.Enum(Status))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    frequency = db.relationship('GoalFrequency', backref='goal', lazy=True)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.String(36), primary_key=True, default= lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)  
    description = db.Column(db.String(100), nullable=True)  
    date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


