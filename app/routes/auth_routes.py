from flask import Blueprint, request, jsonify
import re
from app.models import User
from app import db
from ..schema.user_schema import UserSchema
from marshmallow import ValidationError


auth=Blueprint('auth', __name__)

@auth.route('/signup', methods=['POST'])
def create_user():
    """
    User Registration
    ---
    tags:
      - User
    parameters:
      - name: user
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              example: john_doe
            password:
              type: string
              example: strongpassword
    responses:
      201:
        description: User created successfully
      400:
        description: Username and password are required
      400:
        description: Username already exists
    """
    user_schema=UserSchema(session=db.session)

    try:
        user_data=user_schema.load(request.json)

        if User.query.filter_by(username=user_data.username).first():
            return ({"error":"Username alredy exists."}), 409

        db.session.add(user_data)
        db.session.commit()
        user_response=user_schema.dump(user_data)
        user_response.pop('password')
        return jsonify(user_response), 201
    except ValidationError as err:
        return jsonify({"errors":err.messages}), 400

@auth.route('/user/<string:guid>', methods=['GET'])
def get_user(guid):
    """
    Get user by ID
    ---
    tags:
      - User
    parameters:
      - name: guid
        in: path
        type: string
        required: true
        description: The ID of the user to retrieve
    responses:
      200:
        description: User found
        schema:
          type: object
          properties:
            id:
              type: string
              example: '1a2b3c4d5e6f7g8h9i0j'
            username:
              type: string
              example: Nejra
      404:
        description: User not found
    """
 
    user = User.query.get(guid)  # Corrected parameter name

    if user is None:
        return {'message': 'User is not found.'}, 404

    return jsonify({
        'id': user.id,
        'username': user.username,
        'created_at': user.created_at,
        'updated_at': user.updated_at
    }), 200

@auth.route('/user/<string:guid>', methods=['PUT'])
def update_user(guid):
    """
    Update user by ID
    ---
    tags:
      - User
    parameters:
      - name: guid
        in: path
        type: string
        required: true
        description: The GUID of the user to update
      - name: user
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              example: NejraUpdated
            password:
              type: string
              example: new_password
    responses:
      200:
        description: User updated successfully
      404:
        description: User not found
    """
    
    user=User.query.filter_by(id=guid).first()
    
    if user is None:
        return ({'message':'User is not found.'}), 404
    
    data=request.get_json()
    username=data['username']
    password=data['password']
    if not data:
        return ({'message': 'Request body is empty!'}), 400
    
    if len(username) < 4 or len(username) > 20:
        return jsonify({"error": "Username must be between 4 and 20 characters"}), 400
    if username.isalnum() is False:
        return jsonify({"error":"User must contain only alphanumeric characters."}), 400
    if len(password) < 8:
        return jsonify({"error": "Password must be more than 8 characters"}), 400
    if not re.search(r"[A-Z]", password):
        return jsonify("Password must contain at least one uppercase letter"), 400
    if not re.search(r"[0-9]", password):
        return jsonify("Password must contain at least one digit."), 400
    if not re.search(r"[!@#$%^&*()_+{}\[\]:;\"\'<>,.?/~`\\|-]", password):
        return jsonify("Password must contain at least one specia character."), 400
    
    if 'username' in data:
        user.username=data['username']
    if 'password' in data:
        user.set_password(data['password'])
    
    db.session.commit()

    return jsonify({'message':'User is updated successfully'}), 200
    