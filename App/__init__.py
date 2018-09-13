from flask import Flask
from App.ext import init_ext
from App.settings import Config
from App.views import user_blue


def create_app():
    app = Flask(__name__)
    app.register_blueprint(blueprint=user_blue)
    app.config.from_object(Config)
    init_ext(app)

    return app