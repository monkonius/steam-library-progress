from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    steamid = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    todo = db.relationship('Todo', backref='user', passive_deletes=True)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String(400))
    state = db.Column(db.String(8), default='to play')
    player = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)