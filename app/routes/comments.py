from ..schema.comments import CommentSchema
from flask import Blueprint, request, jsonify
from app import db
from marshmallow import ValidationError
from app.models import Comment, Task
from sqlalchemy import text

comments = Blueprint("comments", __name__)


@comments.route("/comments", methods=["POST"])
def create_comment():
    """
    Create a new comment
    ---
    tags:
      - Comments
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            task_id:
              type: string
              description: ID of the task on which we are adding comment.
              example: "1f865910-5cd1-41ae-9803-edc2af810ea6"
            comment_text:
              type: string
              description: comment text.
              example: "My birthday"

          required:
            - task_id
            - comment_text
    responses:
      201:
        description: Comment created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              description: Unique identifier for the created comment.
              example: 1
            message:
              type: string
              example: 'comment created successfully'
      400:
        description: Bad request
        schema:
          type: object
          properties:
            message:
              type: string
              example: 'misiing values'
    """
    comment_schema = CommentSchema(session=db.session)

    try:
        comments_data = comment_schema.load(request.json)
        db.session.add(comments_data)
        db.session.commit()
        return jsonify(
            "Comment succesfully added to the task.", comment_schema.dump(comments_data)
        )

    except ValidationError as err:
        return jsonify(err.messages)


@comments.route("/comments/<string:guid>", methods=["GET"])
def get_comments(guid):
    """
    Get all comments for a certain task
    ---
    tags:
      - Comments
    parameters:
      - name: guid
        in: path
        required: true
        type: string
        description: Unique identifier (GUID) for the task.
    responses:
      200:
        description: A list of comments for the task
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                description: Unique identifier for the comment.
                example: "fa6fab10-3798-4990-a8f3-45cd883f577f"
              task_id:
                type: string
                description: ID of the task associated with this comment.
                example: "fa6fab10-3798-4990-a8f3-45cd883f577f"
              comment_text:
                type: string
                description: Comment text.
                example: "Finish the project documentation"
              created_at:
                type: string
                format: date-time
                description: Timestamp when the comment was created.
                example: "2024-10-31T13:22:46Z"
              updated_at:
                type: string
                format: date-time
                description: Timestamp when the comment was last updated.
                example: "2024-11-01T10:15:30Z"
      404:
        description: No comments found for this task
    """
    task = Task.query.filter(Task.id == guid).first()
    if not task:
        return ({"message": "This task does not exist."}), 404
    comments = Comment.query.filter(Comment.task_id == guid).all()
    if not comments:
        return jsonify({"message": "No comments found."}), 404

    comments_list = [
        {
            "id": comment.id,
            "task_id": comment.task_id,
            "comment_text": comment.comment_text,
            "created_at": comment.created_at.isoformat(),
            "updated_at": comment.updated_at.isoformat(),
        }
        for comment in comments
    ]

    return jsonify(comments_list), 200


@comments.route("/<string:guid1>/<string:guid2>", methods=["DELETE"])
def delete_comment(guid1, guid2):
    """
    Delete a comment
    ---
    tags:
      - Comments
    parameters:
      - name: guid1
        in: path
        required: true
        type: string
        description: Unique identifier (GUID) for the task that is associated with a comment.
      - name: guid2
        in: path
        required: true
        type: string
        description: Unique identifier (GUID) for the comment.
    responses:
      200:
        description: Comment deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Comment is successfully deleted"
      404:
        description: Comment not found
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Comment not found"
      400:
        description: Bad request
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Invalid GUID format or missing GUID"
    """

    comment = Comment.query.filter(
        Comment.task_id == guid1, Comment.id == guid2
    ).first()
    if not comment:
        return {"message": "Colud not find comment."}
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "Comment deleted successfully."}), 204


@comments.route("/<string:guid1>/<string:guid2>", methods=["PUT"])
def update_task(guid1, guid2):
    """
    Update a comment
    ---
    tags:
      - Comments
    parameters:
      - name: guid1
        in: path
        required: true
        type: string
        description: Unique identifier (GUID) for the task.
      - name: guid2
        in: path
        required: true
        type: string
        description: Unique identifier (GUID) for the comment.
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            comment_text:
              type: string
              description: comment.
              example: "Finish the project documentation"



    responses:
      200:
        description: Comment updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: 'Comment is updated successfully'
      404:
        description: Comment not found
        schema:
          type: object
          properties:
            message:
              type: string
              example: 'This comment does not exist'
      400:
        description: Bad request
        schema:
          type: object
          properties:
            message:
              type: string
              example: 'Request body is missing'
    """

    comment_schema = CommentSchema(session=db.session)
    try:
        comment = Comment.query.filter(
            Comment.task_id == guid1, Comment.id == guid2
        ).first()
        comment_data = comment_schema.load(request.json)

        comment.comment_text = comment_data.comment_text
        db.session.commit()
        return jsonify(comment_schema.dump(comment_data)), 200

    except ValidationError as err:
        return jsonify(err.messages)
