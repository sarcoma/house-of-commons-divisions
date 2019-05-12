from flask import Flask

from router import router


def register_blueprints(app):
    app.register_blueprint(router)


def create_app(config_filename=None):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    register_blueprints(app)

    return app
