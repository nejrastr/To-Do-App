from marshmallow import fields,validates,ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import Task
from app import db
from marshmallow_enum import EnumField
from app.models import Status,PriorityEnum
from datetime import datetime

class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model=Task
        load_instance=True
        sql_session=db.session
    user_id=fields.String(required=False)
    name=fields.String(required=True, validate=lambda x: len(x)>5)
    description=fields.String(required=False)
    due_date=fields.Date(required=True)
    completed=fields.Boolean()
    status=EnumField(Status)
    priority=EnumField(PriorityEnum)
    
@validates('due_date')
def due_date_validation(self,value):
    if value<datetime().now().date():
        raise ValidationError('Due date is in the past.')



    