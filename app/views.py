from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user

from .api import get_library, get_player, get_game, get_recent_games
from .models import User, Todo
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
    recent_raw = get_recent_games(steamid)

    player = player_raw['response']['players'][0]
    name = player['personaname']
    avatar = player['avatarfull']

    library = library_raw['response']['games']
    games = sorted(library,
                   key=lambda value: value['playtime_forever'], reverse=True)
    games_playtime = list(
        map(lambda x: x['playtime_forever'], games))
    total_playtime = sum(games_playtime)
    top_games = games[0:3]

    todo = db.session.execute(db.select(Todo).filter_by(player=current_user.id)).scalars().all()
    todo_dict = dict(playing=list(filter(lambda x: x.state.value == 'playing', todo)),
                     finished=list(filter(lambda x: x.state.value == 'finished', todo)),
                     on_hold=list(filter(lambda x: x.state.value == 'on hold', todo)),
                     dropped=list(filter(lambda x: x.state.value == 'dropped', todo)),
                     to_play=list(filter(lambda x: x.state.value == 'to play', todo)))
    
    recent_games = recent_raw['response']['games']
    

    return render_template('home.html',
                           avatar=avatar,
                           name=name,
                           total_playtime=total_playtime,
                           top_games=top_games,
                           todo=todo,
                           todo_dict=todo_dict,
                           recent_games=recent_games)


@bp.route('/playtime')
@login_required
def playtime():
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
    avatar = player['avatarfull']

    return render_template('playtime.html',
                            steamid=steamid,
                            games=games,
                            total_playtime=total_playtime,
                            avatar=avatar)


@bp.route('/gamelist', methods=['GET', 'POST'])
@login_required
def gamelist():
    user = db.get_or_404(User, current_user.id)
    steamid = user.steamid
    library_raw = get_library(steamid)
    player_raw = get_player(steamid)

    games = library_raw['response']['games']
    game_names = list(map(lambda x: x['name'], games))

    player = player_raw['response']['players'][0]
    avatar = player['avatarfull']

    states = ['playing', 'finished', 'on hold', 'dropped', 'to play']

    if request.method == 'POST':
        new_state = request.form.get('state')
        todo_id = request.form.get('id')
        todo_item = db.get_or_404(Todo, todo_id)
        todo_item.state = new_state
        db.session.commit()

        return redirect(url_for('views.gamelist'))

    todo = db.session.execute(db.select(Todo).filter_by(player=current_user.id).order_by(
        db.case((Todo.state == 'playing', 1), (Todo.state == 'finished', 2),
                (Todo.state == 'on hold', 3), (Todo.state == 'dropped', 4),
                (Todo.state == 'to play', 5)).asc(),
        db.collate(Todo.game, 'NOCASE'))).scalars().all()
    if todo:
        listed_games = list(map(lambda x: x.game, todo))

    if not todo:
        for game in games:
            new_game = Todo(game=game['name'], game_id=game['appid'], player=current_user.id)
            db.session.add(new_game)
            db.session.commit()

        return redirect(url_for('views.gamelist'))
    elif sorted(listed_games) != sorted(game_names):
        for game in games:
            if game['name'] not in listed_games:
                new_game = Todo(game=game['name'], game_id=game['appid'], player=current_user.id)
                db.session.add(new_game)
                db.session.commit()
        for todo_item in todo:
            if todo_item.game not in game_names:
                db.session.delete(todo_item)
                db.session.commit()

    return render_template('gamelist.html', avatar=avatar, todo=todo, states=states)


@bp.route('/game/<int:appid>')
@login_required
def game(appid):
    user = db.get_or_404(User, current_user.id)
    steamid = user.steamid
    library_raw = get_library(steamid)
    player_raw = get_player(steamid)
    game_raw = get_game(appid)

    player = player_raw['response']['players'][0]
    avatar = player['avatarfull']

    game = game_raw[str(appid)]['data']

    library = library_raw['response']['games']
    data = [x for x in library if x['appid'] == appid]
    playtime = data[0]['playtime_forever'] / 60

    todo_item = db.session.execute(db.select(Todo).filter_by(player=current_user.id, game_id=appid)).scalar_one()
    state = todo_item.state.value.title()

    return render_template('game.html',
                           avatar=avatar,
                           game=game,
                           playtime=playtime,
                           state=state)