from app import socketio

if __name__ == '__main__':
    app = create_app(debug=True)
    socketio.run(app)