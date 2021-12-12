import os
from project.models import Device, User
from project.forms import NewDeviceForm
from flask import Blueprint, redirect, render_template, request, url_for, jsonify, flash
from flask_login import login_required, current_user
from sqlalchemy.orm.attributes import flag_modified
from datetime import datetime
from . import db
from .prj_helper import select_from_all, update_user_dev_options

main = Blueprint("main", __name__)


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


@main.route("/device_preferences")
@login_required
def device_preferences():
    devices = Device.query.order_by(Device.dev_type.asc(), Device.name.asc())
    user = User.query.get(current_user.id)
    user.device_options = update_user_dev_options(devices, user.device_options)
    flag_modified(user, "device_options")
    db.session.commit()
    return render_template(
        "device_selection.html", devices=user.device_options["devices"]
    )


@main.route("/man-dev", methods=["GET", "POST"])
@login_required
def manage_devices():
    # Display ascending order first by type then by name
    devices = Device.query.order_by(Device.dev_type.asc(), Device.name.asc())
    return render_template("managedevices.html", info_email=INFO_EMAIL, devices=devices)


@main.route("/new-dev", methods=["GET", "POST"])
@login_required
def add_device():
    new_device_form = NewDeviceForm()
    if new_device_form.errors:
        print(new_device_form.errors)
    # TODO:handle devices with same name
    if new_device_form.validate_on_submit():
        # print("this was a post request")
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
            date_created=datetime.utcnow(),
            date_modified=datetime.utcnow(),
            user_created=current_user.name,
            user_modified=current_user.name,
        )
        # print("generated new device, trying to add")
        # print('trying to create a new device')
        db.session.add(new_device)
        db.session.commit()
        # print("this should be enough, it should have committed")
        return redirect(url_for("main.manage_devices"))
    # print("this was a get request")
    return render_template(
        "newdevice.html", info_email=INFO_EMAIL, form=new_device_form
    )


@main.route("/edit-device/<int:dev_id>", methods=["GET", "POST"])
@login_required
def edit_device(dev_id):
    device = Device.query.get(dev_id)
    edit_form = NewDeviceForm(
        name=device.name,
        dev_type=device.dev_type,
        di=device.di,
        ai=device.ai,
        ui=device.ui,
        do=device.do,
        ao=device.ao,
        co=device.co,
        has_clock=str(device.has_clock),
        price=device.price,
    )

    # if edit_form.is_submitted():
    #     print("submitted")
    #     print(edit_form.errors)

    # if edit_form.validate():
    #     print("valid")

    if edit_form.validate_on_submit():
        # print("Validated submission")
        device.dev_type = edit_form.dev_type.data
        device.di = edit_form.di.data
        device.ai = edit_form.ai.data
        device.ui = edit_form.ui.data
        device.do = edit_form.do.data
        device.ao = edit_form.ao.data
        device.co = edit_form.co.data
        device.has_clock = edit_form.has_clock.data
        device.price = edit_form.price.data
        device.user_modified = current_user.name
        device.date_modified = datetime.utcnow()
        # print("trying to commit changes")
        db.session.commit()
        # print("Done, yay")
        return redirect(url_for("main.manage_devices"))

    return render_template(
        "editdevice.html",
        form=edit_form,
        dev_id=dev_id,
        dev_name=device.name.upper(),
        created_date=device.date_created.replace(microsecond=0).isoformat(),
        created_by=device.user_created,
        modified_date=device.date_modified.replace(microsecond=0).isoformat(),
        modified_by=device.user_modified,
    )


@main.route("/about")
@login_required
def about():
    return render_template("about.html", info_email=INFO_EMAIL)


# @main.route("/delete/<int:device_id>")
# @login_required
# def delete_device(device_id):
#     device_to_delete = Device.query.get(device_id)
#     db.session.delete(device_to_delete)
#     db.session.commit()
#     return redirect(url_for("main.manage_devices"))
