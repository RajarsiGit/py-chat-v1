from flask import Flask
from flask_socketio import SocketIO
from .main import main as main_blueprint

"""Create an application."""
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
app.register_blueprint(main_blueprint)

socketio = SocketIO(app)

if __name__ == "__main__":
    socketio.run(app)