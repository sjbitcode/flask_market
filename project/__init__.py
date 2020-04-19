from flask import Flask

from project.db import db
from project.routes import main_blueprint
from project import settings


def create_app():
    """Construct the core application."""
    app = Flask(__name__)
    app.config.from_object(settings)

    # register our blueprints
    app.register_blueprint(main_blueprint)

    db.init_app(app)

    with app.app_context():
        from project import models
        db.create_all()  # Create database tables for our data models

    return app
