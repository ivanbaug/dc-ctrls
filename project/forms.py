from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, URL, EqualTo, InputRequired
from wtforms.fields.html5 import EmailField


class NewUserForm(FlaskForm):
    name = StringField("Your Name:", validators=[DataRequired()])
    email = EmailField("Your email:", validators=[DataRequired(), Email(
        "This field requires a valid email address")])
    password = PasswordField("Password:", validators=[
                             InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password', validators=[InputRequired()])
    submit = SubmitField("Sign Up!")


class LoginForm(FlaskForm):
    email = EmailField("Your email:", validators=[DataRequired(), Email(
        "This field requires a valid email address")])
    password = PasswordField("Password:", validators=[InputRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Log In")
