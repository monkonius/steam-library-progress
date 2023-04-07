from flask import Blueprint, render_template, request, redirect, flash

from .api import get_library, get_player

bp = Blueprint('views', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        steamid = request.form.get('steamid')
        library = get_library(steamid)['response']['games']
        player = get_player(steamid)['response']['players'][0]

        if library and player:
            games = sorted(library,
                            key=lambda value: value['playtime_forever'], reverse=True)
            games_playtime = list(
                map(lambda x: x['playtime_forever'], games))
            total_playtime = sum(games_playtime)

            name = player['personaname']
            avatar = player['avatarfull']
        else:
            flash('Invalid Steam ID', 'error')
            return redirect('/')

        return render_template('index.html',
                                steamid=steamid,
                                games=games,
                                total_playtime=total_playtime,
                                name=name,
                                avatar=avatar)

    return render_template('index.html')
