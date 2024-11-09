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

    from app.routes.auth import auth
    from app.routes.goals import goals
    from app.routes.events import events
    from app.routes.tasks import tasks
    from app.routes.main import main
    app.register_blueprint(auth)
    app.register_blueprint(tasks)
    app.register_blueprint(events)
    app.register_blueprint(goals)
    app.register_blueprint(main)

    
    with app.app_context():

        db.create_all()  

    return app
