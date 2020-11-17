from flask import render_template
from flask_security import current_user

import config
from corelib.flask import Flask
from ext import security, db
from views import index


def _inject_processor():
    return dict(isinstance=isinstance, current_user=current_user,
                getattr=getattr, len=len)


def _inject_template_global(app):
    app.add_template_global(dir)
    app.add_template_global(len)
    app.add_template_global(hasattr)
    app.add_template_global(current_user, 'current_user')


def create_app():
    from models.user import user_datastore
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    app.context_processor(_inject_processor)
    _inject_template_global(app)
    
    _state = security.init_app(app, user_datastore)
    security._state = _state

    app.register_blueprint(index.bp, url_prefix='/')

    return app


app = create_app()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
