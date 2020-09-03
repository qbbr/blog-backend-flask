from flask import Blueprint, jsonify

from flaskr.models import Tag
from flaskr.schemas import TagSchema

bp = Blueprint('tag', __name__)


@bp.route('/tags/', methods=['GET'])
def get_tags():
    tags = Tag().query.all()
    return jsonify(TagSchema(many=True).dump(tags)), 200  # OK
