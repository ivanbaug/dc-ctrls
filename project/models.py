from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    __tablename__ = "users"
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    # TODO: create show prices column to save if
    # the user wants to show the prices during his session.
    # show_prices = db.Column(db.Boolean)


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
    # TODO: Create relation with the user that created it, may not be neccesary
    user_created = db.Column(db.String(1000))
    user_modified = db.Column(db.String(1000))
