import datetime
from flask import Flask, json
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        JWT_SECRET_KEY='super-secret-key',
        JWT_ACCESS_TOKEN_EXPIRES=datetime.timedelta(seconds=3600),
        JWT_REFRESH_TOKEN_EXPIRES=datetime.timedelta(seconds=3600),
        SQLALCHEMY_DATABASE_URI='sqlite:///app.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    CORS(app)

    from flaskr.views import auth, post, tag, user_post, user_profile

    app.register_blueprint(auth.bp)
    app.register_blueprint(post.bp)
    app.register_blueprint(tag.bp)
    app.register_blueprint(user_post.bp)
    app.register_blueprint(user_profile.bp)

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            'code': e.code,
            'message': '[{}] {}.'.format(e.name, e.description),
        })
        response.content_type = 'application/json'
        return response

    @app.cli.command('init-db')
    def init_db_command():
        db.create_all()

    return app
