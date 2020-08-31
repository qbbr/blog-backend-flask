from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError
from sqlalchemy import or_

from flaskr import app, db
from flaskr.helpers import error_bad_request, error_validation, error_bad_login, render_paginator, get_sort, \
    get_search_filter, process_tags
from flaskr.models import User, Post, Tag
from flaskr.schemas import UserProfileSchema, UserRegistrationSchema, PostSchema, TagSchema
import markdown


@app.route('/register/', methods=['POST'])
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


@app.route('/login/', methods=['POST'])
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


@app.route('/user/profile/', methods=['GET'])
@jwt_required
def get_user_profile():
    user = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    return jsonify(UserProfileSchema().dump(user)), 200  # OK


@app.route('/user/profile/', methods=['PUT', 'PATCH'])
@jwt_required
def update_user_profile():
    if not request.is_json:
        return error_bad_request()
    json_data = request.get_json()
    try:
        user = User.query.filter_by(username=get_jwt_identity()).first_or_404()
        UserProfileSchema().load(json_data, instance=user)
        db.session.add(user)
        db.session.commit()
    except ValidationError as err:
        return error_validation(err.messages)
    return '', 204  # No Content


@app.route('/user/profile/', methods=['DELETE'])
@jwt_required
def delete_user_profile():
    user = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return '', 204  # No Content


@app.route('/posts/', methods=['GET'])
def get_posts():
    query = Post.query.filter_by(isPrivate=False).order_by(get_sort(request))
    search_query = request.args.get('query', type=str, default='')
    if len(search_query):
        query = query.filter(or_(*get_search_filter(search_query)))
    return jsonify(render_paginator(request, PostSchema, query)), 200  # OK


@app.route('/post/<slug>/', methods=['GET'])
def get_post_by_slug(slug):
    post = Post.query.filter_by(slug=slug).first()
    return jsonify(PostSchema().dump(post))


@app.route('/tags/', methods=['GET'])
def get_tags():
    tags = Tag().query.all()
    return jsonify(TagSchema(many=True).dump(tags)), 200  # OK


@app.route('/user/posts/', methods=['GET'])
@jwt_required
def get_user_posts():
    user = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    query = Post().query.filter_by(user=user).order_by(get_sort(request))
    return jsonify(render_paginator(request, PostSchema, query)), 200  # OK


@app.route('/user/post/', methods=['POST'])
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
        post.tags = tags
        db.session.add(post)
        db.session.commit()
    except ValidationError as err:
        return error_validation(err.messages)
    return jsonify({'id': post.id}), 201  # Created


@app.route('/user/post/<int:id>/', methods=['GET'])
@jwt_required
def get_user_post(id):
    user = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    post = Post.query.filter_by(user=user, id=id).first_or_404()
    return jsonify(PostSchema().dump(post)), 200  # OK


@app.route('/user/post/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required
def update_user_post(id):
    if not request.is_json:
        return error_bad_request()
    json_data = request.get_json()
    user = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    post = Post.query.filter_by(user=user, id=id).first_or_404()
    tags = process_tags(json_data)
    try:
        PostSchema(instance=post).load(json_data)
        post.tags = tags
        db.session.add(post)
        db.session.commit()
    except ValidationError as err:
        return error_validation(err.messages)
    return '', 204  # No Content


@app.route('/user/post/<int:id>/', methods=['DELETE'])
@jwt_required
def delete_user_post(id):
    user = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    post = Post().query.filter_by(user=user, id=id).first_or_404()
    db.session.delete(post)
    db.session.commit()
    return '', 204  # No Content


@app.route('/user/post/md2html/', methods=['POST'])
@jwt_required
def md2html():
    if not request.is_json:
        return error_bad_request()
    return jsonify({'html': markdown.markdown(request.json.get('text'))}), 200  # OK
