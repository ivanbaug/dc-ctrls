from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    __tablename__ = "users"
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Device(db.Model):
    __tablename__ = "devices"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), unique=True)
    dev_type = db.Column(db.String(50))
    di = db.Columns(db.Integer)
    ai = db.Columns(db.Integer)
    ui = db.Columns(db.Integer)
    do = db.Columns(db.Integer)
    ao = db.Columns(db.Integer)
    co = db.Columns(db.Integer)
    has_clock = db.Columns(db.Boolean)
    date_created = db.Columns(db.DateTime)
    date_modified = db.Columns(db.DateTime)
    # TODO: Create relation with the user that created it, may not be neccesary
    user_created = db.Column(db.String(1000))
    user_modified = db.Column(db.String(1000))
