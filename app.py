from flask import Flask
from controllers import server_blueprint


def create_app():
    app = Flask(__name__)
    return app


def init_app(app:Flask):
    app.register_blueprint(
        server_blueprint
    )
    return app