from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, URL, EqualTo


class NewUserForm(FlaskForm):
    name = StringField("Your Name:", validators=[DataRequired()])
    email = StringField("Your email:", validators=[DataRequired(), Email()])
    password = PasswordField("Password:", validators=[
                             DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField("Sign Up!")
