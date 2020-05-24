from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from project import settings

app = Flask(__name__)
app.config.from_object(settings)
db = SQLAlchemy(app)

from project import routes
app.register_blueprint(routes.main_blueprint)

db.create_all()
