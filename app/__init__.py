from flask import Flask

from . import auth, db, routes
from .config import Config


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if config:
        app.config.update(config)

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(routes.bp)
    return app
