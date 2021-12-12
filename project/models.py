from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime

from . import db


class User(UserMixin, db.Model):
    __tablename__ = "users"
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(250))
    show_prices = db.Column(db.Boolean, default=False)
    device_options = db.Column(JSON)
    has_privileges = db.Column(db.Boolean, default=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)


class Device(db.Model):
    __tablename__ = "devices"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), unique=True)
    dev_type = db.Column(db.String(50))
    di = db.Column(db.Integer)
    ai = db.Column(db.Integer)
    ui = db.Column(db.Integer)
    do = db.Column(db.Integer)
    ao = db.Column(db.Integer)
    co = db.Column(db.Integer)
    has_clock = db.Column(db.Boolean)
    price = db.Column(db.Float)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    user_created = db.Column(db.String(250))
    user_modified = db.Column(db.String(250))
    is_default = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "name": self.name,
            "di": self.di,
            "ai": self.ai,
            "ui": self.ui,
            "do": self.do,
            "ao": self.ao,
            "co": self.co,
            "price": self.price,
            "is_controller": True if self.dev_type == "controller" else False,
        }
