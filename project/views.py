import os
from project.models import Device, User
from project.forms import NewDeviceForm
from flask import Blueprint, redirect, render_template, request, url_for, jsonify, flash
from flask_login import login_required, current_user
from datetime import datetime
from pytz import timezone
from . import db
from .prj_requests import select_from_all

main = Blueprint("main", __name__)

tz = timezone("America/Lima")
INFO_EMAIL = os.environ.get("INFO_EMAIL")


@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            req_di = int(request.form["di"])
            req_ai = int(request.form["ai"])
            req_do = int(request.form["do"])
            req_ao = int(request.form["ao"])
        except Exception as e:
            msg = "One or more of your inputs are not a number between 0 and 128"
        else:
            selected = select_from_all(req_di, req_ai, req_do, req_ao)
            return render_template(
                "index.html",
                selected=selected,
                req_di=req_di,
                req_ai=req_ai,
                req_do=req_do,
                req_ao=req_ao,
            )

    return render_template("index.html")


@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@main.route("/man-dev", methods=["GET", "POST"])
@login_required
def manage_devices():
    devices = Device.query.all()
    # devices = []
    return render_template("managedevices.html", info_email=INFO_EMAIL, devices=devices)


@main.route("/new-dev", methods=["GET", "POST"])
@login_required
def add_device():
    new_device_form = NewDeviceForm()
    # TODO:handle devices with same name
    if new_device_form.validate_on_submit():

        print("this was a post request")
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
            user_created=current_user.name,
            user_modified=current_user.name,
        )
        print("generated new device, trying to add")
        # print('trying to create a new device')
        db.session.add(new_device)
        db.session.commit()
        print("this should be enough, it should have committed")
        return redirect(url_for("main.manage_devices"))
    print("this was a get request")
    return render_template(
        "newdevice.html", info_email=INFO_EMAIL, form=new_device_form
    )


@main.route("/about")
@login_required
def about():
    return render_template("about.html", info_email=INFO_EMAIL)


@main.route("/delete/<int:device_id>")
@login_required
def delete_device(device_id):
    device_to_delete = Device.query.get(device_id)
    db.session.delete(device_to_delete)
    db.session.commit()
    return redirect(url_for("main.manage_devices"))


# TODO: make this available for privileged users only
@main.route("/toggle-price-display", methods=["PATCH"])
@login_required
def toggle_price():
    user = User.query.get(current_user.id)
    if user:
        user.show_prices = not user.show_prices
        db.session.commit()
        return jsonify(response={"success": "Sucessfully updated price display."}), 200
    else:
        return (
            jsonify(error={"Not Found": "Sorry, we don't have a user with that id."}),
            404,
        )
