from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from . import db
from .models import User, Device

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
