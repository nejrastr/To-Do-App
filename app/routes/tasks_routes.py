from flask import Blueprint, request, jsonify
from app import db
from app.models import Task
from datetime import datetime
from ..schema.task_schema import TaskSchema
from marshmallow import ValidationError

tasks=Blueprint('tasks', __name__)

@tasks.route('/tasks', methods=['GET'])
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


@tasks.route('/tasks/<string:guid>', methods=['GET'])
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

@tasks.route('/task', methods=['POST'])
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
    task_schema=TaskSchema(session=db.session)
  
    try:
      task_data=task_schema.load(request.json)
      db.session.add(task_data)
      db.session.commit()
      return jsonify(task_schema.dump(task_data)), 201
    except ValidationError as err:
      return jsonify(err.messages)

  

@tasks.route('/task/<string:guid>', methods=['PUT'])
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
  task_schema=TaskSchema(session=db.session)
    
  try: 
       task=Task.query.filter_by(id=guid).first()
       if task is None:
         return({'message':'This task does not exist'}), 404
       task_data=task_schema.load(request.json)
       if task_data.name:
        task.name=task_data.name
       if task_data.description:
        task.name=task_data.description
       if task_data.due_date:
        task.due_date = task_data.due_date
       if task_data.completed:
        task.completed=task_data.completed
       if task_data.status:
        task.status=task_data.status
       if task_data.priority:
        task.priority=task_data.priority
       
        db.session.commit()
        return jsonify(task_schema.dump(task_data)), 200
  except ValidationError as err:
     return(err.messages), 400
  

@tasks.route('/tasks/<string:guid>', methods=['DELETE'])
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

