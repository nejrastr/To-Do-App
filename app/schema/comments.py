from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import Comment
from app import db


class CommentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        load_instance = True
        sql_session = db.session

    task_id = fields.String(required=False)
    comment_text = fields.String(required=True)
