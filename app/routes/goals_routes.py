from flask import Blueprint, request, jsonify
from app.models import Goal
from app import db
from datetime import datetime

goals=Blueprint('goals', __name__)

@goals.route('/goals', methods=['POST'])
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


@goals.route('/goals', methods=['GET'])
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
    
@goals.route('/goals/<string:guid>', methods=['GET'])
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
 
@goals.route('/goals/<string:guid>', methods=['DELETE'])
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

@goals.route('/goals/<string:guid>', methods=['PUT'])
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


