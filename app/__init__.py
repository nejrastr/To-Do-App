from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from app.extensions import swagger

db = SQLAlchemy()  # Initialize the database instance

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    swagger.init_app(app)

    db.init_app(app)  # Initialize SQLAlchemy with the app

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        from .models import Task
        from .models import User
        from .models import Goal
        from .models import GoalFrequency
        from .models import Event

        db.create_all()  

    return app
