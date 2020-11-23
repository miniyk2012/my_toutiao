import os

from flask import render_template, send_from_directory, abort, request
from flask.blueprints import Blueprint

from config import UPLOAD_FOLDER
from models.core import Post, Tag, PostTag
from models.search import Item

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/post/<id>')
def post(id):
    post = Post.get_or_404(id)
    return render_template('post.html', post=post)


@bp.route('/static/avatars/<path>')
def avatar(path):
    return send_from_directory(os.path.join(UPLOAD_FOLDER, 'avatars'), path)


@bp.route('/tag/<ident>')
def tag(ident):
    ident = ident.lower()
    tag = Tag.get_by_name(ident)
    if not tag:
        tag = Tag.get(ident)
        if not tag:
            abort(404)
    page = request.args.get('page', default=1, type=int)
    type = request.args.get('type', default='hot')  # hot/latest
    if type == 'latest':
        posts = PostTag.get_posts_by_tag(ident, page)
    elif type == 'hot':
        # 热点使用es的热点搜索功能, 比mysql临时统计要方便的多
        posts = Item.get_post_ids_by_tag(ident, page, type)
        posts.items = Post.get_multi(posts.items)  # posts是Pagination对象
    else:
        # 未知类型
        posts = []
    return render_template('tag.html', tag=tag, ident=ident, posts=posts)

@bp.route('/search')
def search():
    # 本项目只搜索Post
    query = request.args.get('q', '')
    page = request.args.get('page', default=1, type=int)
    posts = Item.new_search(query, page)
    return render_template('search.html', query=query, posts=posts)