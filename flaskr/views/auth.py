from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError

from flaskr import db
from flaskr.helpers import error_bad_request, error_validation, error_bad_login
from flaskr.models import User
from flaskr.schemas import UserRegistrationSchema

bp = Blueprint('auth', __name__)


@bp.route('/register/', methods=['POST'])
def auth_register():
    if not request.is_json:
        return error_bad_request()
    json_data = request.get_json()
    try:
        data = UserRegistrationSchema().load(json_data)
    except ValidationError as err:
        return error_validation(err.messages)
    if User.query.filter_by(username=data['username']).first():
        return error_validation({'username': ['That username is already used']})
    else:
        user = User(username=data['username'])
        user.setpassword(data['password'])
        db.session.add(user)
        db.session.commit()
    access_token = create_access_token(data['username'])
    return jsonify(token=access_token), 201  # Created


@bp.route('/login/', methods=['POST'])
def auth_login():
    if not request.is_json:
        return error_bad_request()
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return error_bad_login()
    user = User().query.filter_by(username=username).first()
    if not user or not user.checkpassword(password):
        return error_bad_login()
    access_token = create_access_token(username)
    return jsonify(token=access_token), 200  # OK
