from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .models import User
from .api import get_player

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        steamid = request.form.get('steamid')
        password = request.form.get('password')

        user = User.query.filter_by(steamid=steamid).first()
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
    if request.method == 'POST':
        steamid = request.form.get('steamid')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        player_raw = get_player(steamid)

        if not player_raw or not player_raw['response']['players']:
            flash('Invalid Steam ID', 'error')
        else:
            user = User.query.filter_by(steamid=steamid).first()
            if user:
                flash('Steam ID is already in use', 'error')
            elif password != confirm:
                flash('Passwords do not match', 'error')
            else:
                new_user = User(steamid=steamid, password=generate_password_hash(password))
                db.session.add(new_user)
                db.session.commit()

                login_user(new_user, remember=True)
                flash('Registration successful!')
                return redirect(url_for('views.index'))

    return render_template('register.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out!')
    return redirect(url_for('auth.login'))