from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
migrate = Migrate()
marshmallow = Marshmallow()

def register_blueprints(app):
    from project.blueprints.change_blueprint import change_blueprint
    from project.blueprints.incident_blueprint import incident_blueprint
    from project.blueprints.problem_blueprint import problem_blueprint
    from project.blueprints.health_blueprint import health_blueprint
    app.register_blueprint(change_blueprint)
    app.register_blueprint(incident_blueprint)
    app.register_blueprint(problem_blueprint)
    app.register_blueprint(health_blueprint)

def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)  
    app.config.from_pyfile(config_filename)
    initialize_extensions(app)
    register_blueprints(app)
    return app

def initialize_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    marshmallow.init_app(app)
