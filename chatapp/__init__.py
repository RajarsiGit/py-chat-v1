from flask import Flask
from flask_socketio import SocketIO

from .config import Config

socketio = SocketIO()


def create_app(config_class=Config):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(config_class)

    from .routes import main
    app.register_blueprint(main)

    socketio.init_app(app)

    from . import sockets  # noqa: F401  (registers socketio event handlers)

    return app
