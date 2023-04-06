from flask import Flask, render_template, request, redirect, flash

from .api import get_library, SECRET_KEY


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['TEMPLATES_AUTO_RELOAD'] = True


    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            steamid = request.form.get('steamid')
            library = get_library(steamid)

            if library:
                games = sorted(library['response']['games'],
                            key=lambda value: value['playtime_forever'], reverse=True)
                games_playtime = list(map(lambda x: x['playtime_forever'], games))
                total_playtime = sum(games_playtime)
            else:
                flash('Invalid Steam ID', 'error')
                return redirect('/')

            return render_template('index.html', steamid=steamid, games=games, total_playtime=total_playtime)

        return render_template('index.html')

    return app