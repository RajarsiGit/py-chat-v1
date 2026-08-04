from flask import session
from flask_socketio import emit, join_room, leave_room

from . import socketio


@socketio.on('joined', namespace='/chat')
def joined(message):
    room = session.get('room')
    name = session.get('name')
    if not room or not name:
        return
    join_room(room)
    emit('status', {'msg': name + ' joined this room'}, room=room, include_self=False)
    emit('self_status', {'msg': 'You joined this room'})


@socketio.on('message', namespace='/chat')
def text(message):
    room = session.get('room')
    name = session.get('name')
    if not room or not name:
        return
    emit('message', {'msg': name + ': ' + message['msg']}, room=room, include_self=False)
    emit('self_message', {'msg': message['msg']})


@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    name = session.get('name')
    if not room:
        return
    leave_room(room)
    emit('status', {'msg': name + ' left this room'}, room=room, include_self=False)


@socketio.on('disconnect', namespace='/chat')
def disconnected():
    room = session.get('room')
    name = session.get('name')
    if not room:
        return
    leave_room(room)
    emit('status', {'msg': name + ' left this room'}, room=room, include_self=False)
