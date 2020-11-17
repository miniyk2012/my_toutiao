from flask import render_template

import config
from corelib.flask import Flask
from ext import security, db
from views import index


def create_app():
    from models.user import user_datastore
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    _state = security.init_app(app, user_datastore)
    security._state = _state

    app.register_blueprint(index.bp, url_prefix='/')

    return app


app = create_app()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
