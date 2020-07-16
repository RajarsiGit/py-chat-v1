from flask import Flask, render_template, request, session, url_for, redirect, Blueprint
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired, AnyOf
import os

main = Blueprint('main', __name__)

secret_key = str(os.urandom(24))

app = Flask(__name__)
app.config['TESTING'] = False
app.config['DEBUG'] = True
app.config['FLASK_ENV'] = 'deployment'
app.config['SECRET_KEY'] = secret_key
app.config['DEBUG'] = True
app.register_blueprint(main)

socketio = SocketIO(app)

clients = []

class LoginForm(FlaskForm):
    form_pin = '2468'
    name = StringField('Name', validators=[DataRequired()])
    room = StringField('Room', validators=[DataRequired()])
    pin = StringField('Pin', validators=[DataRequired(), AnyOf(form_pin, message='Wrong PIN')])
    submit = SubmitField('Enter Chatroom')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        session['pin'] = form.pin.data
        return redirect(url_for('.chat'))
    elif request.method == 'POST':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
        form.pin.data = session.get('pin', '')
    return render_template('index.html', form=form)

@app.route('/chat')
def chat():
    name = session.get('name', '')
    room = session.get('room', '')
    pin = session.get('pin', '')
    if name == '' or room == '' or pin == '':
        return redirect(url_for('.index'))
    #return render_template('chat_https.html', name=name, room=room, pin=pin)
    return render_template('chat_http.html', name=name, room=room, pin=pin)

@socketio.on('joined', namespace='/chat')
def joined(message):
    clients.append(request.sid)
    room = session.get('room')
    join_room(room)
    for client in clients:
        if not client == request.sid:
            emit('status', {'msg' : session.get('name') + ' joined this room'}, room=client)
        else:
            emit('self_status', {'msg' : 'You joined this room'}, room=client)

@socketio.on('message', namespace='/chat')
def text(message):
    room = session.get('room')
    for client in clients:
        if not client == request.sid:
            emit('message', {'msg' : session.get('name') + ': ' + message['msg']}, room=client)
        else:
            emit('self_message', {'msg' : message['msg']}, room=client)

@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg' : session.get('name') + ' left this room'}, room=room)
    
if __name__ == "__main__":
    socketio.run(app, host='192.168.2.3')