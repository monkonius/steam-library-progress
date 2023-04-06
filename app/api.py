import os
import requests
import json

from dotenv import load_dotenv


load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')


def get_library(steamid):
    try:
        steamkey = os.getenv('STEAM_API_KEY')
        url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
        response = requests.get(f'{url}?key={steamkey}&steamid={steamid}&include_appinfo=true&include_played_free_games=true&format=json')
        response.raise_for_status()

    except requests.RequestException:
        return None
    
    data = json.loads(response.text)
    return data