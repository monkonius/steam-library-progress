from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .models import User, Todo
from .api import get_library, get_player

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in!')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect', 'error')
        else:
            flash('That user does not exist', 'error')

    return render_template('login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        steamid = request.form.get('steamid')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        player_raw = get_player(steamid)

        if not player_raw or not player_raw['response']['players']:
            flash('Invalid Steam ID', 'error')
        else:
            user = User.query.filter_by(steamid=steamid).first()
            if user:
                flash('Steam ID or email already in use', 'error')
            elif password != confirm:
                flash('Passwords do not match', 'error')
            else:
                new_user = User(
                    steamid=steamid,
                    email=email,
                    password=generate_password_hash(password))
                db.session.add(new_user)
                db.session.commit()

                library_raw = get_library(steamid)
                games = library_raw['response']['games']
                for game in games:
                    new_game = Todo(
                        game=game['name'],
                        game_id=game['appid'],
                        player=new_user.id)
                    db.session.add(new_game)
                    db.session.commit()

                login_user(new_user, remember=True)
                flash('Registration successful!')
                return redirect(url_for('views.home'))

    return render_template('register.html')


@bp.route('/reset', methods=['GET', 'POST'])
@login_required
def reset():
    user = db.get_or_404(User, current_user.id)
    player_raw = get_player(user.steamid)
    player = player_raw['response']['players'][0]
    avatar = player['avatarfull']

    if request.method == 'POST':

        old_password = request.form.get('old-password')
        new_password = request.form.get('new-password')
        confirm = request.form.get('confirm')

        if not check_password_hash(user.password, old_password):
            flash('Incorrect password', 'error')
        elif new_password != confirm:
            flash('Passwords do not match', 'error')
        else:
            user.password = generate_password_hash(new_password)
            db.session.commit()
            flash('Password reset successful!')
            return redirect(url_for('views.home'))

    return render_template('reset.html', avatar=avatar)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out!')
    return redirect(url_for('auth.login'))