from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from app.extensions import  Swagger

db = SQLAlchemy()  



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    template = {
    "swagger": "2.0",
    "info": {
      "title": "Planning App API",
      "description": "This API was developed using Python Flask",
      "version": "1.0"
    }
  }
    app.config['SWAGGER'] = {
    'title': 'Planer app API',
    'uiversion': 3,
    'template': './resources/flasgger/swagger_ui.html'
  }
    Swagger(app, template=template)

    db.init_app(app)  

  
    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        from .models import Task
        from .models import User
        from .models import Goal
        from .models import Event

        db.create_all()  

    return app
