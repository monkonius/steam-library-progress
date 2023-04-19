from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user

from .api import get_library, get_player
from .models import User
from . import db

bp = Blueprint('views', __name__)


@bp.route('/')
def index():
    if current_user.is_authenticated:
        user = db.get_or_404(User, current_user.id)
        steamid = user.steamid
        player_raw = get_player(steamid)
        player = player_raw['response']['players'][0]
        avatar = player['avatarfull']

        return render_template('index.html', avatar=avatar)

    return render_template('index.html')


@bp.route('/home')
@login_required
def home():
    user = db.get_or_404(User, current_user.id)
    steamid = user.steamid
    library_raw = get_library(steamid)
    player_raw = get_player(steamid)

    library = library_raw['response']['games']
    games = sorted(library,
                    key=lambda value: value['playtime_forever'], reverse=True)
    games_playtime = list(
        map(lambda x: x['playtime_forever'], games))
    total_playtime = sum(games_playtime)

    player = player_raw['response']['players'][0]
    name = player['personaname']
    avatar = player['avatarfull']

    return render_template('home.html',
                            steamid=steamid,
                            games=games,
                            total_playtime=total_playtime,
                            name=name,
                            avatar=avatar)