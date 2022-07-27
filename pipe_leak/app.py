from flask import Flask

from pipe_leak import api


def create_app():
    app = Flask("pipe_leak")
    register_blueprints(app)

    return app


def register_blueprints(app):
    app.register_blueprint(api.blueprint)
