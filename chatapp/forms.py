from flask import current_app
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired, AnyOf


class LoginForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    room = StringField('Room', validators=[DataRequired()])
    pin = StringField('Pin', validators=[DataRequired()])
    submit = SubmitField('Enter Chatroom')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pin.validators.append(
            AnyOf([current_app.config['CHAT_PIN']], message='Wrong PIN')
        )
