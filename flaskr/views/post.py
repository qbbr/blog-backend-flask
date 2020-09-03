from flask import request, jsonify, Blueprint
from sqlalchemy import or_

from flaskr.helpers import get_search_filter, render_paginator, get_sort
from flaskr.models import Post
from flaskr.schemas import PostSchema

bp = Blueprint('post', __name__)


@bp.route('/posts/', methods=['GET'])
def get_posts():
    query = Post.query.filter_by(isPrivate=False).order_by(get_sort(request))
    search_query = request.args.get('query', type=str, default='')
    if len(search_query):
        query = query.filter(or_(*get_search_filter(search_query)))
    return jsonify(render_paginator(request, PostSchema, query)), 200  # OK


@bp.route('/post/<slug>/', methods=['GET'])
def get_post_by_slug(slug):
    post = Post.query.filter_by(slug=slug).first()
    return jsonify(PostSchema().dump(post))
