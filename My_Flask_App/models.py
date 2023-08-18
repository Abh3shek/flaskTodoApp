from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import datetime

class Note(db.Model):
    sr_no = db.Column(db.Integer, primary_key=True)
    taskTitle = db.Column(db.String(10000))
    taskDescription = db.Column(db.String(10000))
    issue = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(20))
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    notes = db.relationship('Note')