import enum
from . import db
from flask_login import UserMixin


class StateEnum(enum.Enum):
    PLAYING = 'playing'
    FINISHED = 'finished'
    ON_HOLD = 'on hold'
    DROPPED = 'dropped'
    TO_PLAY = 'to play'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    steamid = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    todo = db.relationship('Todo', backref='user', passive_deletes=True)

    def __repr__(self):
        return f'<User with Steam ID: {self.steamid}>'


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String(400))
    game_id = db.Column(db.Integer, nullable=False)
    state = db.Column(db.Enum(StateEnum, values_callable=lambda x: [
                                 str(member.value) for member in x]), default=StateEnum.TO_PLAY)
    player = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    
    def __repr__(self):
        return f'<{self.game}, {self.state.value} by User {self.player}>'