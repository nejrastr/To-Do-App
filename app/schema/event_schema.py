from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import Event
from app import db


class EventSchema(SQLAlchemyAutoSchema):
    class Meta:
        model=Event
        load_instance=True
        sql_session=db.session
    user_id=fields.String(required=False)
    name=fields.String(required=True, validate=lambda x: len(x)>5)
    description=fields.String(required=True)
    date=fields.Date(required=True)

