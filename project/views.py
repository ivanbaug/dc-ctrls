import os
from project.forms import NewDeviceForm
from flask import(Blueprint,
                  redirect,
                  render_template,
                  request,
                  url_for,
                  flash)
from flask_login import login_required, current_user
from datetime import datetime

main = Blueprint('main', __name__)

INFO_EMAIL = os.environ.get('INFO_EMAIL')


@main.route('/')
def index():
    return render_template("index.html")


@main.route('/profile')
@login_required
def profile():
    return render_template("profile.html")


@main.route('/man-dev', methods=['GET', 'POST'])
@login_required
def manage_devices():
    new_device_form = NewDeviceForm()
    if new_device_form.validate_on_submit():
        pass
    return render_template("managedevices.html", info_email=INFO_EMAIL, form=new_device_form)


@main.route('/about')
@login_required
def about():
    return render_template("about.html", info_email=INFO_EMAIL)
