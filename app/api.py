import os
import requests
import json

from dotenv import load_dotenv


load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
STEAMKEY = os.getenv('STEAM_API_KEY')


def get_library(steamid):
    try:
        url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
        params = '&include_appinfo=true&include_played_free_games=true'
        response = requests.get(f'{url}?key={STEAMKEY}&steamid={steamid}{params}')
        response.raise_for_status()

    except requests.RequestException:
        return None
    
    data = json.loads(response.text)
    return data


def get_player(steamid):
    try:
        url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
        response = requests.get(f'{url}?key={STEAMKEY}&steamids={steamid}')
        response.raise_for_status()

    except requests.RequestException:
        return None
    
    data = json.loads(response.text)
    return data


def get_game(appid):
    try:
        url = 'https://store.steampowered.com/api/appdetails'
        response = requests.get(f'{url}?appids={appid}&l=english')
        response.raise_for_status()
    
    except requests.RequestException:
        return None
    
    data = json.loads(response.text)
    return data