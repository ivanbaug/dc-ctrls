from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from . import db
from .models import User

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
