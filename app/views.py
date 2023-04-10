from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user

from .api import get_library, get_player
from .models import User

bp = Blueprint('views', __name__)


@bp.route('/')
@login_required
def index():
    user = User.query.filter_by(id=current_user.id).first()
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

    return render_template('index.html',
                            steamid=steamid,
                            games=games,
                            total_playtime=total_playtime,
                            name=name,
                            avatar=avatar)