from flask import Flask

import config
from ext import db
from views import index


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    app.register_blueprint(index.bp, url_prefix='/')

    return app


app = create_app()
