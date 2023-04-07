from flask import Blueprint, render_template, request, redirect, flash

from .api import get_library, get_player

bp = Blueprint('views', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        steamid = request.form.get('steamid')
        library_raw = get_library(steamid)
        player_raw = get_player(steamid)

        if library_raw and player_raw:
            library = library_raw['response']['games']
            games = sorted(library,
                            key=lambda value: value['playtime_forever'], reverse=True)
            games_playtime = list(
                map(lambda x: x['playtime_forever'], games))
            total_playtime = sum(games_playtime)

            player = player_raw['response']['players'][0]
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
