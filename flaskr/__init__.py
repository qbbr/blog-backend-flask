import datetime
from flask import Flask, json
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',
    JWT_SECRET_KEY='super-secret-key',
    JWT_ACCESS_TOKEN_EXPIRES=datetime.timedelta(seconds=3600),
    JWT_REFRESH_TOKEN_EXPIRES=datetime.timedelta(seconds=3600),
    SQLALCHEMY_DATABASE_URI='sqlite:///app.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    # CORS_HEADERS='Content-Type',
)
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
CORS(app)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "message": "[{}] {}.".format(e.name, e.description),
    })
    response.content_type = "application/json"
    return response


@app.cli.command('init-db')
def init_db_command():
    db.create_all()


from . import models
from . import views
