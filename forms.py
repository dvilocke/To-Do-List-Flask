from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    remind_me = BooleanField('Remember me')
    submit = SubmitField('log In')


class singInForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password= StringField('Password', validators=[DataRequired()])
    submit = SubmitField('check in')
    