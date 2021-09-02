import os
from project.models import Device
from project.forms import NewDeviceForm
from flask import(Blueprint,
                  redirect,
                  render_template,
                  request,
                  url_for,
                  flash)
from flask_login import login_required, current_user
from datetime import datetime
from pytz import timezone
from . import db

main = Blueprint('main', __name__)

tz = timezone("America/Lima")
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
    # TODO:handle devices with same name
    if new_device_form.validate_on_submit():
        new_device = Device(
            name=new_device_form.name.data,
            dev_type=new_device_form.dev_type.data,
            di=new_device_form.di.data,
            ai=new_device_form.ai.data,
            ui=new_device_form.ui.data,
            do=new_device_form.do.data,
            ao=new_device_form.ao.data,
            co=new_device_form.co.data,
            has_clock=new_device_form.has_clock.data,
            price=new_device_form.price.data,
            date_created=datetime.now(tz=tz),
            date_modified=datetime.now(tz=tz),
            # date_created=datetime.strftime(
            #     datetime.now(tz=tz), '%Y-%m-%d %H:%M:%S'),
            # date_modified=datetime.strftime(
            #     datetime.now(tz=tz), '%Y-%m-%d %H:%M:%S'),
            user_created=current_user.name,
            user_modified=current_user.name,
        )
        print('trying to create a new device')
        db.session.add(new_device)
        db.session.commit()
        return redirect(url_for('main.about'))
    return render_template("managedevices.html", info_email=INFO_EMAIL, form=new_device_form)


@main.route('/about')
@login_required
def about():
    return render_template("about.html", info_email=INFO_EMAIL)
