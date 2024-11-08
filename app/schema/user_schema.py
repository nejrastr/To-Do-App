from marshmallow import fields, ValidationError, validates, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import User
import re
from app import db
from werkzeug.security import generate_password_hash

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model=User
        load_instance=True
        sql_session=db.session
    username=fields.String(required=True, validate=lambda x: len(x)>4 and len(x)<20)
    password=fields.String(required=True, validate=lambda x: len(x)>8)

    @validates("password")
    def validate_password_strength(self,value):
        if not any(char.isupper() for char in value):
            raise ValidationError("Password must contain at least one upper letter.")
        if not any(char.islower() for char in value):
            raise ValidationError("Password must contain at least one lower letter.")
        if not any(char.isdigit() for char in value):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*()_+{}\[\]:;\"\'<>,.?/~`\\|-]", value):
            raise ValidationError("Password must contain at least one specia character.")
    
    @post_load
    def hash_password(self, data, **kwargs):
        if 'password' in data:
            data['password']=generate_password_hash(data['password'])

        return data



