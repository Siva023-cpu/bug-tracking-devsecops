from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")  # admin / user


class Bug(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default="Open")

    reported_by = db.Column(db.String(50))
    attachment = db.Column(db.String(255))


class Solution(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.Text, nullable=False)
    attachment = db.Column(db.String(255))

    bug_id = db.Column(db.Integer, db.ForeignKey('bug.id'), nullable=False)
    user = db.Column(db.String(50))

    bug = db.relationship('Bug', backref=db.backref('solutions', lazy=True))


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    message = db.Column(db.String(255))
    user = db.Column(db.String(100))
    is_read = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
