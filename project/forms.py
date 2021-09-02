from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, URL, EqualTo, InputRequired
from wtforms.fields.html5 import DecimalField, EmailField


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


class NewDeviceForm(FlaskForm):
    name = StringField("Device Name:", validators=[DataRequired()])
    dev_type = SelectField("Device Type:", choices=[
        ('controller', 'Controller'),
        ('expansion', 'Expansion Module'),
        ('thermostat', 'Thermostat'),
        ('other', 'Other')],
        default='controller')
    di = IntegerField("Digital Inputs:", default=0)
    ai = IntegerField("Analog Inputs:", default=0)
    ui = IntegerField("Universal Inputs:", default=0)
    do = IntegerField("Digital Outputs:", default=0)
    ao = IntegerField("Analog Outputs:", default=0)
    co = IntegerField("Configurable Outputs:", default=0)
    has_clock = SelectField("Has internal clock/schedule?",
                            choices=[('True', 'Yes'), ('False', 'No')],
                            default=False,
                            coerce=lambda x: x == 'True')
    price = DecimalField("Price: ", places=2, validators=[DataRequired()])
    submit = SubmitField("Save new device")
