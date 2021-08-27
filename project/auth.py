from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash)
from flask_login import login_user, logout_user, login_required
import os
from .models import User
from .forms import NewUserForm
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template("login.html")


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        # if the user doesn't exist or password is wrong, reload the page
        return redirect(url_for('auth.login'))

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    # Set form as none if users are to be invited since the project is very very small.
    # nform = None

    nform = NewUserForm()

    if nform.validate_on_submit():
        # If user's email already exists
        if User.query.filter_by(email=nform.email.data).first():
            # Send flash messsage
            flash("You've already signed up with that email, log in instead!")
            # Redirect to /login route.
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            nform.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=nform.email.data,
            name=nform.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()

        # Logging in right after registering so the user can access the
        # full page

        login_user(new_user)

        return redirect(url_for("main.index"))
    return render_template("signup.html", info_email=os.environ.get('INFO_EMAIL'), form=nform)


# @auth.route('/signup', methods=['POST'])
# def signup_post():
#     email = request.form.get('email')
#     name = request.form.get('name')
#     password = request.form.get('password')

#     if not (email and name and password):
#         flash('All fields are required')
#         return redirect(url_for('auth.signup'))

#     # if this returns a user, then the email already exists in database
#     user = User.query.filter_by(email=email).first()

#     if user:  # if a user is found, we want to redirect back to signup page so user can try again
#         flash('Email address already exists')
#         return redirect(url_for('auth.login'))

#     # create a new user with the form data. Hash the password so the plaintext version isn't saved.
#     new_user = User(email=email, name=name,
#                     password=generate_password_hash(password, method='sha256'))

#     # add the new user to the database
#     db.session.add(new_user)
#     db.session.commit()

#     return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
