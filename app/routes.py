from flask import Blueprint, render_template, request,jsonify
from app import db
from app.models import User, Task, Goal, Event
import re

from datetime import datetime





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
def get_task(guid):
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
        
    if due_date<datetime.utcnow().date():
        return jsonify("Date should not be in the past"), 400

    new_task = Task(
        user_id=user_id,
        name=name,
        description=description,
        due_date=due_date,
        completed=completed,
        status=status,
        priority=priority,
        created_at=datetime.utcnow(),  
        updated_at=datetime.utcnow()   
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
  if 'due_date' in data:
        due_date = data['due_date']
        try:
            parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
            task.due_date = parsed_due_date
        except ValueError:
            return jsonify({'message': 'Invalid date format for due_date. Use YYYY-MM-DD.'}), 400
        
       
        if parsed_due_date < datetime.utcnow().date():
            return jsonify({"message": "Date should not be in the past"}), 400
      
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

@main.route('/events/<string:guid>', methods=['GET'])
def get_event(guid): 
 """
    Get event by ID
    ---
    tags:
      - Events
    parameters:
      - name: guid
        in: path
        required: true
        type: string
        description: Unique identifier (GUID) for the event.
    responses:
      200:
        description: A event in JSON format
        schema:
          type: object
          properties:
            id:
              type: integer
              description: Unique identifier for the task.
              example: 1
            user_id:
              type: integer
              description: ID of the user associated with this event.
              example: 12
            name:
              type: string
              description: Name or title of the event.
              example: "birthday"
            description:
              type: string
              description: Detailed description of the event.
              example: "birthday"
              nullable: true
            date:
              type: string
              format: date
              description: Date of the event.
              example: "2024-12-31"
              nullable: true
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
  
 event=Event.query.get(guid)
 if event is None:
  return({'message':'There is event with this id'}), 404
    
 return jsonify({
        'id':event.id,
        'user_id':event.user_id,
        'name':event.name,
        'description':event.description,
        'date':event.date,
        'created_at':event.created_at,
        'updated_at':event.updated_at
              })

@main.route('/events', methods=['GET'])
def get_events():
    """
    Get all events
    ---
    tags:
      - Events
    responses:
      200:
        description: A list of events
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                description: Unique identifier for the event.
                example: "fa6fab10-3798-4990-a8f3-45cd883f577f"
              user_id:
                type: string
                description: ID of the user associated with this task.
                example: "fa6fab10-3798-4990-a8f3-45cd883f577f"
              name:
                type: string
                description: Name or title of the event.
                example: "Finish the project documentation"
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
        description: No events found
    """
    
    events=Event.query.all()
    if not events:
     return({'There is no created events.'})
    
    result=[{
         'id':event.id,
        'user_id':event.user_id,
        'name':event.name,
        'description':event.description,
        'date':event.date,
        'created_at':event.created_at,
        'updated_at':event.updated_at
    } 
    for event in events]
    
    return(result)

@main.route('/events/<string:guid>', methods=['PUT'])
def update_event(guid):
    """
Update an existing event
---
tags:
  - Events
parameters:
  - name: guid
    in: path
    required: true
    type: string
    description: Unique identifier (GUID) for the event.
  - name: body
    in: body
    required: true
    schema:
      type: object
      properties:
        name:
          type: string
          description: Name or title of the event.
          example: "Finish the project documentation"
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
       
responses:
  200:
    description: Event updated successfully
    schema:
      type: object
      properties:
        message:
          type: string
          example: 'Event is updated successfully'
  404:
    description: Event not found
    schema:
      type: object
      properties:
        message:
          type: string
          example: 'This event does not exist'
  400:
    description: Bad request
    schema:
      type: object
      properties:
        message:
          type: string
          example: 'Request body is missing'
"""

    
    event=Event.query.get(guid)

    if not event:
        return({'message':'There is no event with this id.'})
    
    data=request.get_json()

    if 'username' in data:
       event.name=data['name']
    if 'description' in data:
        event.description=data['description']
    if  'date' in data:
        date=data['date']
        parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
        event.date=parsed_date
    
    db.session.commit()

    return jsonify({
        'id':event.id,
        'user_id':event.user_id,
        'name':event.name,
        'description':event.description,
        'date':event.date,
        'created_at':event.created_at,
        'updated_at':event.updated_at
        
    })

@main.route('/tasks/<string:guid>', methods=['DELETE'])
def delete_task(guid):
    """
    Delete an existing task
    ---
    tags:
      - Task
    parameters:
      - name: guid
        in: path
        required: true
        type: string
        description: Unique identifier (GUID) for the task to be deleted.
    responses:
      200:
        description: Task deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Task is successfully deleted"
      404:
        description: Task not found
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Task not found"
      400:
        description: Bad request
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Invalid GUID format or missing GUID"
    """
    task = Task.query.get(guid)

    if task is None:
        return jsonify({'message': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'Task is successfully deleted'}), 200

@main.route('/events/<string:guid>', methods=['DELETE'])
def delete_event(guid):
    """
    Delete an existing event
    ---
    tags:
      - Events
    parameters:
      - name: guid
        in: path
        required: true
        type: string
        description: Unique identifier (GUID) for the event to be deleted.
    responses:
      200:
        description: Event deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Event is successfully deleted"
      404:
        description: Event not found
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Event not found"
      400:
        description: Bad request
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Invalid GUID format or missing GUID"
"""
    event = Event.query.get(guid)

    if event is None:
        return jsonify({'message': 'Event not found'}), 404

    db.session.delete(event)
    db.session.commit()

    return jsonify({'message': 'Event is successfully deleted'}), 200

   
   
   

@main.route('/goals', methods=['POST'])
def create_goal():
    """
    Create a new goal
    ---
    tags:
      - Goal
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            user_id:
              type: string
              description: ID of the user creating the goal.
              example: "1f865910-5cd1-41ae-9803-edc2af810ea6"
            name:
              type: string
              description: Name or title of the goal.
              example: "Finish the project documentation"
            description:
              type: string
              description: Detailed description of the goal.
              example: "Compile all the project documents and submit by the due date."
              nullable: true
            start_date:
              type: string
              format: date
              description: Due date for completing the goal.
              example: "2024-12-31"
              nullable: true
            end_date:
              type: string
              format: date
              description: Due date for completing the goal.
              example: "2024-12-31"
              nullable: true
           
            status:
              type: string
              enum:
                - DONE
                - IN_PROGRESS
                - TBD
              nullable: true.
              example: "IN_PROGRESS"
            frequency:
              type: string
              enum:
                - DAILY
                - WEEKLY
                - MONTHLY
                - YEARLY
              nullable: true.
              example: "WEEKLY"
            priority:
              type: string
              enum:
                - LOW
                - MEDIUM
                - HIGH
              description: Priority level of the goal.
              example: "HIGH"
          required:
            - user_id
            - name
    responses:
      201:
        description: Goal created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              description: Unique identifier for the created goal.
              example: 1
            message:
              type: string
              example: 'Goal created successfully'
      400:
        description: Bad request
        schema:
          type: object
          properties:
            message:
              type: string
              example: 'Missing name for the goal'
    """
    data = request.get_json()

    user_id = data.get('user_id')
    if user_id is None:
        return jsonify({'message': 'Missing user ID'}), 400
    
    name = data.get('name')
    if not name:
        return jsonify({'message': 'Missing name for goal'}), 400
    
    description = data.get('description')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    priority = data.get('priority')
    frequency=data.get('frequency')
    status = data.get('status')
    
    try:
        parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return jsonify({'message': 'Invalid date format, use YYYY-MM-DD'}), 400
    
    if parsed_start_date>parsed_end_date:
        return jsonify({"message":"Start date is after the end date"}), 400

    new_goal = Goal(
        user_id=user_id,
        name=name,
        description=description,
        start_date=parsed_start_date,
        end_date=parsed_end_date,
        priority=priority,
        status=status,
        frequency=frequency,
        created_at=datetime.utcnow(),  
        updated_at=datetime.utcnow()
    )

    db.session.add(new_goal)
    db.session.commit()
    return jsonify({
        'id': new_goal.id,
        'user_id': new_goal.user_id,
        'name': new_goal.name,
        'description': new_goal.description,
        'start_date': str(new_goal.start_date),
        'end_date': str(new_goal.end_date),
        'priority': new_goal.priority.value,
        'status': new_goal.status.value,
        'created_at': new_goal.created_at.isoformat(),
        'updated_at': new_goal.updated_at.isoformat()
    }), 201


@main.route('/goals', methods=['GET'])
def get_goals():
    """
    Get a list of goals
    ---
    tags:
      - Goal
    responses:
      200:
        description: A list of goals
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: Unique identifier for the goal.
                example: "da21f47d-f8c9-4d12-abac-3cfb05cb3ca4"
              user_id:
                type: integer
                description: ID of the user associated with this goal.
                example: "da21f47d-f8c9-4d12-abac-3cfb05cb3ca4"
              name:
                type: string
                description: Name or title of the goal.
                example: "Finish the project documentation"
              description:
                type: string
                description: Detailed description of the goal.
                example: "Compile all the project documents and submit by the due date."
                nullable: true
              start_date:
                type: string
                format: date
                description: when user started working on goal.
                example: "2024-12-31"
                nullable: true
              end_date:
                type: string
                format: date
                description: date when goal is accomplished.
                example: "2024-12-31"
                nullable: true

              status:
                type: string
                enum:
                  - DONE
                  - IN_PROGRESS
                  - TBD
                description: Current status of the goal.
                example: "IN_PROGRESS"
              frequency:
                type: string
                enum:
                  - WEEKLY
                  - DAILY
                  - MONTHLY
                  - YEARLY
                description: Current status of the goal.
                example: "WEEKLY"
              priority:
                type: string
                enum:
                  - LOW
                  - MEDIUM
                  - HIGH
                description: Priority level of the goal.
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
        description: No goals found
    """
    goals=Goal.query.all()

    if goals is None:
      return({'message':'There is no cretaed goals'})
    
    list_of_goals=[{'id': new_goal.id,
        'user_id': new_goal.user_id,
        'name': new_goal.name,
        'description': new_goal.description,
        'start_date': str(new_goal.start_date),
        'end_date': str(new_goal.end_date),
        'priority': new_goal.priority.value,
        'frequency':new_goal.frequency.value,
        'status': new_goal.status.value,
        'created_at': new_goal.created_at.isoformat(),
        'updated_at': new_goal.updated_at.isoformat()
        
    } for new_goal in goals]

    return jsonify(list_of_goals)
    
@main.route('/goals/<string:guid>', methods=['GET'])
def get_goal(guid):
    """
    Get goal by ID
    ---
    tags:
      - Goal
    parameters:
      - name: guid
        in: path
        required: true
        type: string
        description: Unique identifier (GUID) for the task.
    responses:
      200:
        description: A goal in JSON format
        schema:
          type: object
          properties:
            id:
              type: integer
              description: Unique identifier for the task.
              example: "1f865910-5cd1-41ae-9803-edc2af810ea6"
            user_id:
              type: integer
              description: ID of the user associated with this task.
              example: "1f865910-5cd1-41ae-9803-edc2af810ea6"
            name:
              type: string
              description: Name or title of the goal.
              example: "Finish the project documentation"
            description:
              type: string
              description: Detailed description of the goal.
              example: "Compile all the project documents and submit by the due date."
              nullable: true
            start_date:
              type: string
              format: date
              description: started working on goal.
              example: "2024-12-31"
              nullable: true
            end_date:
              type: string
              format: date
              description: completed goal at.
              example: "2024-12-31"
              nullable: true
           
            status:
              type: string
              enum:
                - DONE
                - IN_PROGRESS
                - TBD
              description: Current status of the gaol.
              example: "IN_PROGRESS"
            frequency:
                type: string
                enum:
                  - WEEKLY
                  - DAILY
                  - MONTHLY
                  - YEARLY
                description: Current status of the goal.
                example: "WEEKLY"
            priority:
              type: string
              enum:
                - LOW
                - MEDIUM
                - HIGH
              description: Priority level of the goal.
              example: "HIGH"
            created_at:
              type: string
              format: date-time
              description: Timestamp when the goal was created.
              example: "2024-10-31T13:22:46Z"
            updated_at:
              type: string
              format: date-time
              description: Timestamp when the goal was last updated.
              example: "2024-11-01T10:15:30Z"
      404:
        description: Goal with this ID does not exist
    """
    
    goal=Goal.query.filter_by(id=guid).first()
    if goal is None:
        return({'message':'Goal with this ID does not exist.'}), 400
    return jsonify({
        'id': goal.id,
        'user_id': goal.user_id,
        'name': goal.name,
        'description': goal.description,
        'start_date': str(goal.start_date),
        'end_date': str(goal.end_date),
        'frequency':goal.frequency.value,
        'priority': goal.priority.value,
        'status': goal.status.value,
        'created_at': goal.created_at.isoformat(),
        'updated_at': goal.updated_at.isoformat()
    }), 200
 
@main.route('/goals/<string:guid>', methods=['DELETE'])
def delete_goal(guid):
    """
    Delete an existing goal
    ---
    tags:
      - Goal
    parameters:
      - name: guid
        in: path
        required: true
        type: string
        description: Unique identifier (GUID) for the goal to be deleted.
    responses:
      200:
        description: Goal deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Goal is successfully deleted"
      404:
        description: Goal not found
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Goal not found"
      400:
        description: Bad request
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Invalid GUID format or missing GUID"
    """
    goal=Goal.query.filter_by(id=guid).first()

    if goal is None:
        return({'message':'Goal with this ID does not exist.'}), 404
    db.session.delete(goal)
    db.session.commit()

    return jsonify({'message':'Goal is successfully deleted.'}), 200

@main.route('/goals/<string:guid>', methods=['PUT'])
def update_goal(guid):
    """
Update an existing goal
---
tags:
  - Goal
parameters:
  - name: guid
    in: path
    required: true
    type: string
    description: Unique identifier (GUID) for the goal.
  - name: body
    in: body
    required: true
    schema:
      type: object
      properties:
        name:
          type: string
          description: Name or title of the goal.
          example: "Finish the project documentation"
        description:
          type: string
          description: Detailed description of the goal.
          example: "Compile all the project documents and submit by the due date."
          nullable: true
        start_date:
          type: string
          format: date
          description: Due date for completing the task.
          example: "2024-12-31"
          nullable: true
        end_date:
          type: string
          format: date
          description: Due date for completing the goal.
          example: "2024-12-31"
          nullable: true
        frequency:
                type: string
                enum:
                  - WEEKLY
                  - DAILY
                  - MONTHLY
                  - YEARLY
                description: Current status of the goal.
                example: "WEEKLY"
       
        status:
          type: string
          enum:
            - DONE
            - IN_PROGRESS
            - TBD
          description: Current status of the goal.
          example: "IN_PROGRESS"
        priority:
          type: string
          enum:
            - LOW
            - MEDIUM
            - HIGH
          description: Priority level of the goal.
          example: "HIGH"
responses:
  200:
    description: Goal updated successfully
    schema:
      type: object
      properties:
        message:
          type: string
          example: 'Goal is updated successfully'
  404:
    description: Goal not found
    schema:
      type: object
      properties:
        message:
          type: string
          example: 'This gaol does not exist'
  400:
    description: Bad request
    schema:
      type: object
      properties:
        message:
          type: string
          example: 'Request body is missing'
"""
    
    goal=Goal.query.filter_by(id=guid).first()
    data=request.get_json()

    if goal is None:
        return({'message':'There is no goal with this ID.'}), 404
    if data is None:
        return({'message':'Missing request body'}), 400
    
    name=data.get('name')
    description=data.get('description')
    priority=data.get('priority')
    status=data.get('status')
    frequency=data.get('frequency')
    start_date=data.get('start_date')
    end_date=data.get('end_date')

    if start_date or end_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({'message': 'Invalid date format for due_date. Use YYYY-MM-DD.'}), 400
        
    if start_date>end_date:
        return jsonify({"message":"Start date is after the end date"}), 400
    if name is not None:
        goal.name=name
    if description is not None:
        goal.description=description
    if start_date is not None:
        goal.start_date=start_date
    if end_date is not None:
        goal.end_date=end_date
    if priority is not None:
        goal.priority=priority
    if status is not None:
        goal.status=status
    if frequency is not None:
        goal.frequency=frequency
    
    db.session.commit()

    return jsonify({'id': goal.id,
        'user_id': goal.user_id,
        'name': goal.name,
        'description': goal.description,
        'start_date': str(goal.start_date),
        'end_date': str(goal.end_date),
        'priority': goal.priority.value,
        'frequency':goal.frequency.value,
        'status': goal.status.value,
        'created_at': goal.created_at.isoformat(),
        'updated_at': goal.updated_at.isoformat()
        
    },{'message':'Goal is successfully updated'}), 203 


