from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from app.extensions import  Swagger


db = SQLAlchemy()  



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.name="ToBeDo"
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

  
    
    from .auth import auth
    from .goals import goals
    from .events import events
    from .tasks import tasks
    from .main  import main
    from .comments import comments
    app.register_blueprint(auth)
    app.register_blueprint(tasks)
    app.register_blueprint(events)
    app.register_blueprint(goals)
    app.register_blueprint(main)
    app.register_blueprint(comments)

    with app.app_context():

        db.create_all()  

    return app
