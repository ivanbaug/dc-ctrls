import os

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

from .models import User
from .forms import LoginForm, NewUserForm
from . import db

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        user = User.query.filter_by(email=login_form.email.data).first()
        password = login_form.password.data

        if not user or not check_password_hash(user.password, password):
            flash("Please check your login details and try again.")
            # if the user doesn't exist or password is wrong, reload the page
            return redirect(url_for("auth.login"))

        # if the above check passes, then we know the user has the right credentials
        remember = login_form.remember.data
        login_user(user, remember=remember)
        return redirect(url_for("main.index"))
    return render_template("login.html", form=login_form)


@auth.route("/signup", methods=["GET", "POST"])
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
            return redirect(url_for("auth.login"))

        hash_and_salted_password = generate_password_hash(
            nform.password.data, method="pbkdf2:sha256", salt_length=8
        )
        new_user = User(
            email=nform.email.data,
            name=nform.name.data,
            password=hash_and_salted_password,
            # No need to convert to json
            device_options={},
        )
        db.session.add(new_user)
        db.session.commit()

        # Logging in right after registering so the user can access the
        # full page
        login_user(new_user)

        return redirect(url_for("main.index"))
    if request.method == "POST":
        # Send flash messsage
        flash("Error, check the submitted data, did you confirm your password?")
    return render_template(
        "signup.html", info_email=os.environ.get("INFO_EMAIL"), form=nform
    )


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
