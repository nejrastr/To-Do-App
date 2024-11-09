from flask import Blueprint, request, jsonify
from app import db
from app.models import Event
from datetime import datetime
from ..schema.event_schema import EventSchema
from marshmallow import ValidationError

events = Blueprint("events", __name__)


@events.route("/events", methods=["POST"])
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
    event_schema = EventSchema(session=db.session)
    try:
        event_data = event_schema.load(request.json)
        db.session.add(event_data)
        db.session.commit()
        return jsonify("Event successfully created", event_schema.dump(event_data)), 201
    except ValidationError as err:
        return jsonify(err.messages)


@events.route("/events/<string:guid>", methods=["GET"])
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

    event = Event.query.get(guid)
    if event is None:
        return ({"message": "There is event with this id"}), 404

    return jsonify(
        {
            "id": event.id,
            "user_id": event.user_id,
            "name": event.name,
            "description": event.description,
            "date": event.date,
            "created_at": event.created_at,
            "updated_at": event.updated_at,
        }
    )


@events.route("/events", methods=["GET"])
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

    events = Event.query.all()
    if not events:
        return {"There is no created events."}

    result = [
        {
            "id": event.id,
            "user_id": event.user_id,
            "name": event.name,
            "description": event.description,
            "date": event.date,
            "created_at": event.created_at,
            "updated_at": event.updated_at,
        }
        for event in events
    ]

    return result


@events.route("/events/<string:guid>", methods=["PUT"])
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

    event_schema = EventSchema(session=db.session)
    try:

        event = Event.query.get(guid)
        if not event:
            return {"message": "There is no event with this id."}

        event_data = event_schema.load(request.json)
        event.name = event_data.name
        event.description = event_data.description
        event.date = event_data.date

        db.session.commit()

        return jsonify(event_schema.dump(event_data)), 200
    except ValidationError as err:
        return jsonify(err.messages)


@events.route("/events/<string:guid>", methods=["DELETE"])
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
        return jsonify({"message": "Event not found"}), 404

    db.session.delete(event)
    db.session.commit()

    return jsonify({"message": "Event is successfully deleted"}), 200
