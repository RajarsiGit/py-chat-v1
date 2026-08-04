from flask import Blueprint, render_template, request, session, url_for, redirect

from .forms import LoginForm

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for('.chat'))
    elif request.method == 'POST':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('index.html', form=form)


@main.route('/chat')
def chat():
    name = session.get('name', '')
    room = session.get('room', '')
    if not name or not room:
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room)
