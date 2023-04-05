from flask import Flask, render_template, request, redirect, flash

from helpers import api_query, SECRET_KEY


app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        steamid = request.form.get('steamid')
        data = api_query(steamid)

        if data:
            games = sorted(data['response']['games'], key=lambda value: value['playtime_forever'], reverse=True)
            games_playtime = list(map(lambda x: x['playtime_forever'], games))
            total_playtime = sum(games_playtime)
        else:
            flash('Invalid Steam ID', 'error')
            return redirect('/')

        return render_template('index.html', steamid=steamid, games=games, total_playtime=total_playtime)
    
    return render_template('index.html')