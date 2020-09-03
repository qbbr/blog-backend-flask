from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from flaskr import db
from flaskr.helpers import error_bad_request, error_validation
from flaskr.models import User
from flaskr.schemas import UserProfileSchema

bp = Blueprint('user_profile', __name__)


@bp.route('/user/profile/', methods=['GET'])
@jwt_required
def get_user_profile():
    user = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    return jsonify(UserProfileSchema().dump(user)), 200  # OK


@bp.route('/user/profile/', methods=['PUT', 'PATCH'])
@jwt_required
def update_user_profile():
    if not request.is_json:
        return error_bad_request()
    json_data = request.get_json()
    try:
        user = User.query.filter_by(username=get_jwt_identity()).first_or_404()
        UserProfileSchema().load(json_data, instance=user, partial=True)
        db.session.add(user)
        db.session.commit()
    except ValidationError as err:
        return error_validation(err.messages)
    return '', 204  # No Content


@bp.route('/user/profile/', methods=['DELETE'])
@jwt_required
def delete_user_profile():
    user = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return '', 204  # No Content
