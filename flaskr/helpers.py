from flask import jsonify
from sqlalchemy import desc, asc

from flaskr.models import Post, Tag

PAGE_SIZE = 10


def error(code, message, errors=None):
    data = {'code': code, 'message': message}
    if errors:
        data['errors'] = errors
    return jsonify(data), code


def error_bad_request():
    return error(400, 'Bad Request.')  # Bad Request


def error_bad_login():
    return error(401, 'Invalid credentials.')  # Unauthorized


def error_validation(errors):
    return error(422, 'Validation failed.', errors)  # Unprocessable Entity


def render_paginator(request, schema, query):
    page = request.args.get('page', type=int, default=1)
    results = query.paginate(page, PAGE_SIZE)
    return {
        'results': schema(many=True).dump(results.items),
        'page': results.page,
        'pageSize': results.per_page,
        'total': results.total,
    }


def get_sort(request):
    sort = request.args.get('sort', type=str)
    order = request.args.get('order', type=str, default='desc')
    if sort == 'title':
        sort = Post.title
    else:
        sort = Post.createdAt
    if order == 'desc':
        order_by = desc(sort)
    else:
        order_by = asc(sort)
    return order_by


def get_search_filter(search_query):
    or_statements = set()
    for term in extract_search_terms(search_query):
        or_statements.add(Post.title.like('%{}%'.format(term)))
    return or_statements


def extract_search_terms(search_query):
    terms = set()
    for term in search_query.split():
        terms.add(term.strip())
    return terms


def process_tags(json_data):
    tags = list()
    for tag_data in json_data['tags']:
        tag = Tag().query.filter_by(name=tag_data['name']).first()
        if not tag:
            tag = Tag(name=tag_data['name'])
        tags.append(tag)
    del json_data['tags']
    return tags
