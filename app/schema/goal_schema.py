from marshmallow import fields,validates,ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import Goal
from app import db
from marshmallow_enum import EnumField
from app.models import Status,PriorityEnum, Frequency
from datetime import datetime

class GoalSchema(SQLAlchemyAutoSchema):
    class Meta:
        model=Goal
        load_instance=True
        sql_session=db.session
    user_id=fields.String(required=False)
    name=fields.String(required=True, validate=lambda x: len(x)>5)
    description=fields.String(required=False)
    start_date=fields.Date(required=True)
    end_date=fields.Date(required=False)
    status=EnumField(Status)
    priority=EnumField(PriorityEnum)
    frequency=EnumField(Frequency)
    
@validates('start_date')
def start_date_validation(self,value):
    if value<datetime().now().date():
        raise ValidationError('Start date is in the past.')
@validates('end_date')
def end_date_validation(self,value):
    if value<datetime().now().date():
        raise ValidationError('End date is in the past.')



    