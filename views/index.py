from flask import render_template, send_from_directory, abort, request
from flask.blueprints import Blueprint

from models.core import Post, Tag, PostTag


bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/post/<id>')
def post(id):
    post = Post.get_or_404(id)
    return render_template('post.html', post=post)
