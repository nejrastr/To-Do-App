from flask import Blueprint, render_template, request,jsonify
from app import db
from app.models import User, Task, Goal, Event, GoalFrequency
import uuid
from datetime import datetime, date

import json



main=Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/signup', methods=['POST'])
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
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    
    if User.query.filter_by(username=username).first():
       return jsonify({'message': 'Username already exists!'}), 400

    new_user = User(username=username)
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

@main.route('/user/<string:guid>', methods=['GET'])
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

@main.route('/user/<string:guid>', methods=['PUT'])
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

    if not data:
        return ({'message': 'Request body is empty!'}), 400
    if 'username' in data:
        user.username=data['username']
    if 'password' in data:
        user.set_password(data['password'])
    
    db.session.commit()

    return jsonify({'message':'User is updated successfully'}), 200
    
@main.route('/tasks', methods=['GET'])
def get_tasks():
  """
    Get all tasks
    ---
    tags:
      - Task
    responses:
      200:
        description: A list of tasks
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: Unique identifier for the task.
                example: 1
              user_id:
                type: integer
                description: ID of the user associated with this task.
                example: 12
              name:
                type: string
                description: Name or title of the task.
                example: "Finish the project documentation"
              description:
                type: string
                description: Detailed description of the task.
                example: "Compile all the project documents and submit by the due date."
                nullable: true
              due_date:
                type: string
                format: date
                description: Due date for completing the task.
                example: "2024-12-31"
                nullable: true
              completed:
                type: boolean
                description: Status indicating whether the task is completed.
                example: false
              status:
                type: string
                enum:
                  - DONE
                  - IN_PROGRESS
                  - TBD
                description: Current status of the task.
                example: "IN_PROGRESS"
              priority:
                type: string
                enum:
                  - LOW
                  - MEDIUM
                  - HIGH
                description: Priority level of the task.
                example: "HIGH"
              created_at:
                type: string
                format: date-time
                description: Timestamp when the task was created.
                example: "2024-10-31T13:22:46Z"
              updated_at:
                type: string
                format: date-time
                description: Timestamp when the task was last updated.
                example: "2024-11-01T10:15:30Z"
      404:
        description: No tasks found
    """
  
  
  tasks=Task.query.all()
  if not tasks:
        return({'message':'There is no tasks created.'})
    
  result=[{
      'id':task.id,
      'user_id':task.user_id,
      'name':task.name,
      'description':task.description,
      'due_date':task.due_date,
      'completed':task.completed,
      'status':task.status.value,
      'priority':task.priority.value,
      'created_at':task.created_at,
      'updated_at':task.updated_at
      }
    for task in tasks
  ]
    
  return jsonify(result)


@main.route('/tasks/<string:guid>', methods=['GET'])
def get_tesk(guid):
    """
    Get task by ID
    ---
    tags:
      - Task
    parameters:
      - name: guid
        in: path
        required: true
        type: string
        description: Unique identifier (GUID) for the task.
    responses:
      200:
        description: A task in JSON format
        schema:
          type: object
          properties:
            id:
              type: integer
              description: Unique identifier for the task.
              example: 1
            user_id:
              type: integer
              description: ID of the user associated with this task.
              example: 12
            name:
              type: string
              description: Name or title of the task.
              example: "Finish the project documentation"
            description:
              type: string
              description: Detailed description of the task.
              example: "Compile all the project documents and submit by the due date."
              nullable: true
            due_date:
              type: string
              format: date
              description: Due date for completing the task.
              example: "2024-12-31"
              nullable: true
            completed:
              type: boolean
              description: Status indicating whether the task is completed.
              example: false
            status:
              type: string
              enum:
                - DONE
                - IN_PROGRESS
                - TBD
              description: Current status of the task.
              example: "IN_PROGRESS"
            priority:
              type: string
              enum:
                - LOW
                - MEDIUM
                - HIGH
              description: Priority level of the task.
              example: "HIGH"
            created_at:
              type: string
              format: date-time
              description: Timestamp when the task was created.
              example: "2024-10-31T13:22:46Z"
            updated_at:
              type: string
              format: date-time
              description: Timestamp when the task was last updated.
              example: "2024-11-01T10:15:30Z"
      404:
        description: Task not found
    """
    task=Task.query.get(guid)

    if task is None:
        return({'There is no task with this id.'}), 404
    
    return jsonify({
      'id':task.id,
      'user_id':task.user_id,
      'name':task.name,
      'description':task.description,
      'due_date':task.due_date,
      'completed':task.completed,
      'status':task.status.value,
      'priority':task.priority.value,
      'created_at':task.created_at,
      'updated_at':task.updated_at
    })

@main.route('/task', methods=['POST'])
def create_task():
    """
    Create a new task
    ---
    tags:
      - Task
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            user_id:
              type: string
              description: ID of the user creating the task.
              example: "1f865910-5cd1-41ae-9803-edc2af810ea6"
            name:
              type: string
              description: Name or title of the task.
              example: "Finish the project documentation"
            description:
              type: string
              description: Detailed description of the task.
              example: "Compile all the project documents and submit by the due date."
              nullable: true
            due_date:
              type: string
              format: date
              description: Due date for completing the task.
              example: "2024-12-31"
              nullable: true
            completed:
              type: boolean
              description: Status indicating whether the task is completed.
              example: false
            status:
              type: string
              enum:
                - DONE
                - IN_PROGRESS
                - TBD
              description: Current status of the task.
              example: "IN_PROGRESS"
            priority:
              type: string
              enum:
                - LOW
                - MEDIUM
                - HIGH
              description: Priority level of the task.
              example: "HIGH"
          required:
            - user_id
            - name
    responses:
      201:
        description: Task created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              description: Unique identifier for the created task.
              example: 1
            message:
              type: string
              example: 'Task created successfully'
      400:
        description: Bad request
        schema:
          type: object
          properties:
            message:
              type: string
              example: 'Missing name for the task'
    """
   
    data = request.get_json()
    
    user_id = data.get('user_id') 
    name = data.get('name')
    description = data.get('description')
    due_date = data.get('due_date')
    completed = data.get('completed', False)  # Default to False if not provided
    priority = data.get('priority')
    status = data.get('status')
    
    if user_id is None:
        return jsonify({'message': 'There is no user with this id.'}), 400

    if not name:
        return jsonify({'message': 'Missing name for the task'}), 400
    
    
    if due_date:
        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({'message': 'Invalid date format for due_date. Use YYYY-MM-DD.'}), 400

    new_task = Task(
        user_id=user_id,
        name=name,
        description=description,
        due_date=due_date,
        completed=completed,
        status=status,
        priority=priority,
        created_at=datetime.utcnow(),  # Set created_at to current time
        updated_at=datetime.utcnow()   # Set updated_at to current time
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({'id': new_task.id, 'message': 'Task created successfully'}), 201

@main.route('/task/<string:guid>', methods=['PUT'])
def update_task(guid):
  """
Update an existing task
---
tags:
  - Task
parameters:
  - name: guid
    in: path
    required: true
    type: string
    description: Unique identifier (GUID) for the task.
  - name: body
    in: body
    required: true
    schema:
      type: object
      properties:
        name:
          type: string
          description: Name or title of the task.
          example: "Finish the project documentation"
        description:
          type: string
          description: Detailed description of the task.
          example: "Compile all the project documents and submit by the due date."
          nullable: true
        due_date:
          type: string
          format: date
          description: Due date for completing the task.
          example: "2024-12-31"
          nullable: true
        completed:
          type: boolean
          description: Status indicating whether the task is completed.
          example: false
        status:
          type: string
          enum:
            - DONE
            - IN_PROGRESS
            - TBD
          description: Current status of the task.
          example: "IN_PROGRESS"
        priority:
          type: string
          enum:
            - LOW
            - MEDIUM
            - HIGH
          description: Priority level of the task.
          example: "HIGH"
responses:
  200:
    description: Task updated successfully
    schema:
      type: object
      properties:
        message:
          type: string
          example: 'Task is updated successfully'
  404:
    description: Task not found
    schema:
      type: object
      properties:
        message:
          type: string
          example: 'This task does not exist'
  400:
    description: Bad request
    schema:
      type: object
      properties:
        message:
          type: string
          example: 'Request body is missing'
"""

    
  task=Task.query.filter_by(id=guid).first()
  if task is None:
    return({'message':'This task does not exist'}), 404
  data=request.get_json()
 
  
  if not data:
        return({'message':'Request body is missing'})
  if 'username' in data:
       task.name=data['name']
  if 'description' in data:
        task.description=data['description']
  if  'due_date' in data:
        due_date=data['due_date']
        parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        task.due_date=parsed_due_date
      
  if 'completed' in data:
        task.completed=data['completed']
  if 'priority' in data:
        task.priority=data['priority']
  if 'status' in data:
        task.status=data['status']  
    
  db.session.commit()

  return jsonify({'message':'Task is updated successfully'}), 200

@main.route('/events',methods=['POST'])
def create_event():
  """
    Create a new event
    ---
    tags:
      - Events
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            user_id:
              type: string
              description: ID of the user creating the task.
              example: "1f865910-5cd1-41ae-9803-edc2af810ea6"
            name:
              type: string
              description: Name or title of the event.
              example: "My birthday"
            description:
              type: string
              description: Detailed description of the event.
              example: "Compile all the project documents and submit by the due date."
              nullable: true
            date:
              type: string
              format: date
              description: Date of the event.
              example: "2024-12-31"
              nullable: true
          
          required:
            - user_id
            - name
    responses:
      201:
        description: Event created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              description: Unique identifier for the created task.
              example: 1
            message:
              type: string
              example: 'Event created successfully'
      400:
        description: Bad request
        schema:
          type: object
          properties:
            message:
              type: string
              example: 'Missing name for the event'
    """
  data=request.get_json()
    
  user_id=data['user_id']
  name=data['name']
  description=data['description']
  date=data['date']
  parsed_date = datetime.strptime(date, "%Y-%m-%d").date()

  if name is None:
        return({'message':'Missing event name'})
  if date is None:
        return({'message':'Missing date of the event'})
  

    
  new_event=Event(
        user_id=user_id,
        name=name,
        description=description,
        date=parsed_date,
        created_at=datetime.utcnow(),  # Set created_at to current time
        updated_at=datetime.utcnow()   # Set updated_at to current time
        
    )

  db.session.add(new_event)
  db.session.commit()

  return jsonify({'New event is succesfully created': new_event.id}), 201


   
    
