from app import db
from datetime import datetime
from enum import Enum

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

   
    
    def calculate_task_progress(self):
        number_of_tasks=len(self.tasks)
        
        if number_of_tasks == 0:
            return 0
        number_of_completed_tasks=sum(1 for task in self.tasks if task.status==Status.DONE)
        return int((number_of_completed_tasks/number_of_tasks)*100)
    
    def calculate_goal_progress(self):
        number_of_daily_goals = sum(1 for goal in self.goals if goal.frequency == Frequency.DAILY)
        number_of_weekly_goals = sum(1 for goal in self.goals if goal.frequency == Frequency.WEEKLY)
        number_of_monthly_goals = sum(1 for goal in self.goals if goal.frequency == Frequency.MONTHLY)
        number_of_yearly_goals = sum(1 for goal in self.goals if goal.frequency == Frequency.YEARLY)
        
   
       
        number_of_completed_goals_daily = sum(1 for goal in self.goals if goal.status == Status.DONE and goal.frequency == Frequency.DAILY)
        number_of_completed_goals_weekly = sum(1 for goal in self.goals if goal.status == Status.DONE and goal.frequency == Frequency.WEEKLY)
        number_of_completed_goals_monthly = sum(1 for goal in self.goals if goal.status == Status.DONE and goal.frequency == Frequency.MONTHLY)
        number_of_completed_goals_yearly = sum(1 for goal in self.goals if goal.status == Status.DONE and goal.frequency == Frequency.YEARLY)
        
        daily_progress = 0
        weekly_progress = 0
        monthly_progress = 0
        yearly_progress = 0
       
        if(number_of_daily_goals>0):
         daily_progress = int((number_of_completed_goals_daily / number_of_daily_goals) * 100)
        if(number_of_weekly_goals>0):
         weekly_progress = int((number_of_completed_goals_weekly / number_of_weekly_goals) * 100)
        if(number_of_monthly_goals>0):
         monthly_progress = int((number_of_completed_goals_monthly / number_of_monthly_goals) * 100)
        if(number_of_yearly_goals>0):
         yearly_progress = int((number_of_completed_goals_yearly / number_of_yearly_goals) * 100)

        return daily_progress, weekly_progress, monthly_progress, yearly_progress
    
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
    frequency=db.Column(db.Enum(Frequency))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

   

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.String(36), primary_key=True, default= lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)  
    description = db.Column(db.String(100), nullable=True)  
    date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


