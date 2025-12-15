from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Bug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), nullable=False)  # ✅ ADD THIS
    status = db.Column(db.String(20), default="Open")
    reported_by = db.Column(db.String(50))

 

class Solution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    bug_id = db.Column(db.Integer, db.ForeignKey('bug.id'), nullable=False)
    user = db.Column(db.String(50))

    bug = db.relationship('Bug', backref=db.backref('solutions', lazy=True))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    user = db.Column(db.String(50), nullable=False)   # ✅ THIS MUST EXIST

    bug_id = db.Column(db.Integer, db.ForeignKey('bug.id'), nullable=False)
    bug = db.relationship('Bug', backref='comments')
