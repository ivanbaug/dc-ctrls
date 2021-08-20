from flask import Blueprint, render_template
from flask_login import login_required, current_user
# from . import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template("index.html")


@main.route('/profile')
@login_required
def profile():
    return render_template("profile.html", name=current_user.name)


@main.route('/man-dev')
@login_required
def manage_devices():
    return render_template("managedevices.html")


@main.route('/about')
@login_required
def about():
    return render_template("about.html")
