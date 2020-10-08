from flask.blueprints import Blueprint


bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    return 'Index'
