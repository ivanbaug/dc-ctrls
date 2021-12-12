from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from sqlalchemy.orm.attributes import flag_modified

from . import db
from .models import User, Device
from .prj_helper import update_user_dev_options

prj_api = Blueprint("prj_api", __name__)

# TODO: make this available for privileged users only
@prj_api.route("/toggle-price-display", methods=["PATCH"])
@login_required
def toggle_price():
    user = User.query.get(current_user.id)
    if user:
        user.show_prices = not user.show_prices
        db.session.commit()
        return (
            jsonify(
                response={"Success": "Sucessfully updated price display preference."}
            ),
            200,
        )
    else:
        return (
            jsonify(error={"Not Found": "Sorry, wrong user or id."}),
            404,
        )


@prj_api.route("/delete-device/<int:device_id>", methods=["DELETE"])
@login_required
def delete_device(device_id: int):
    device = Device.query.get(device_id)
    if device:
        db.session.delete(device)
        db.session.commit()
        return (
            jsonify(response={"Success": f"Sucessfully deleted {device.name}."}),
            200,
        )
    else:
        return (
            jsonify(error={"Not Found": "The device was not found in the db."}),
            404,
        )


# TODO: make this available for privileged users only
@prj_api.route("/toggle-default-device/<device_name>", methods=["PATCH"])
@login_required
def toggle_default_device(device_name):
    # device = Device.query.get(device_name)
    device = Device.query.filter_by(name=device_name).first()
    if device:
        device.is_default = not device.is_default
        db.session.commit()
        return (
            jsonify(response={"Success": "Sucessfully updated device preference."}),
            200,
        )
    else:
        return (
            jsonify(error={"Not Found": "Sorry, wrong device or id."}),
            404,
        )


# TODO: make this available for privileged users only
@prj_api.route("/toggle-user-device/<device_name>", methods=["PATCH"])
@login_required
def toggle_user_device(device_name):

    user = User.query.get(current_user.id)
    devices = Device.query.order_by(Device.dev_type.asc(), Device.name.asc())
    udevs = update_user_dev_options(devices, user.device_options)["devices"]

    device_idx = next(
        (i for i, item in enumerate(udevs) if item["name"] == device_name), -1
    )

    if device_idx != -1:
        udevs[device_idx]["select_user"] = not udevs[device_idx]["select_user"]
        user.device_options["devices"] = udevs
        flag_modified(user, "device_options")
        db.session.commit()
        return (
            jsonify(response={"Success": "Sucessfully updated device preference."}),
            200,
        )
    else:
        return (
            jsonify(error={"Not Found": "Sorry, wrong device or id."}),
            404,
        )
