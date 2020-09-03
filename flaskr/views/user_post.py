import markdown
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from flaskr import db
from flaskr.helpers import render_paginator, get_sort, error_bad_request, process_tags, error_validation
from flaskr.models import User, Post
from flaskr.schemas import PostSchema

bp = Blueprint('user_post', __name__)


@bp.route('/user/posts/', methods=['GET'])
@jwt_required
def get_user_posts():
    user = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    query = Post().query.filter_by(user=user).order_by(get_sort(request))
    return jsonify(render_paginator(request, PostSchema, query)), 200  # OK


@bp.route('/user/posts/', methods=['DELETE'])
@jwt_required
def delete_user_posts():
    user = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    Post().query.filter_by(user=user).delete()
    db.session.commit()
    return '', 204  # No Content


@bp.route('/user/post/', methods=['POST'])
@jwt_required
def create_user_post():
    if not request.is_json:
        return error_bad_request()
    json_data = request.get_json()
    user = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    tags = process_tags(json_data)
    try:
        post = PostSchema().load(json_data)
        post.user = user
        if tags:
            post.tags = tags
        db.session.add(post)
        db.session.commit()
    except ValidationError as err:
        return error_validation(err.messages)
    return jsonify({'id': post.id}), 201  # Created


@bp.route('/user/post/<int:id>/', methods=['GET'])
@jwt_required
def get_user_post(id):
    user = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    post = Post.query.filter_by(user=user, id=id).first_or_404()
    return jsonify(PostSchema().dump(post)), 200  # OK


@bp.route('/user/post/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required
def update_user_post(id):
    if not request.is_json:
        return error_bad_request()
    json_data = request.get_json()
    user = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    post = Post.query.filter_by(user=user, id=id).first_or_404()
    tags = process_tags(json_data)
    try:
        PostSchema(instance=post, partial=True).load(json_data)
        if tags:
            post.tags = tags
        db.session.add(post)
        db.session.commit()
    except ValidationError as err:
        return error_validation(err.messages)
    return '', 204  # No Content


@bp.route('/user/post/<int:id>/', methods=['DELETE'])
@jwt_required
def delete_user_post(id):
    user = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    post = Post().query.filter_by(user=user, id=id).first_or_404()
    db.session.delete(post)
    db.session.commit()
    return '', 204  # No Content


@bp.route('/user/post/md2html/', methods=['POST'])
@jwt_required
def md2html():
    if not request.is_json:
        return error_bad_request()
    return jsonify({'html': markdown.markdown(request.json.get('text'))}), 200  # OK
