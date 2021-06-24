import os
import json
import requests

from dotenv import load_dotenv


load_dotenv()


class TRNFetcher:
    def __init__(self, platform, username):
        self.platform = platform
        self.username = username

        link = f'https://api.tracker.gg/api/v2/rocket-league/standard/profile/{self.platform}/{self.username}'
        api_key = os.environ['TRN_API_KEY']
        headers = {
            'TRN-Api-Key': api_key,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
        }

        try:
            response = requests.get(link, headers=headers)
            json_response = json.loads(response.text)
            self.json_response = json_response
        except:
            print('TRNFetcher not initialized with attribute: json_response')

    def get_current_season(self):
        return self.json_response['data']['metadata']['currentSeason']

    def get_pfp(self):
        return self.json_response['data']['platformInfo']['avatarUrl']

    def get_ranks(self):
        player_ranks = {}

        for i in range(1, 9):
            gamemode = self.json_response['data']['segments'][i]['metadata']['name']
            rank = self.json_response['data']['segments'][i]['stats']['tier']['metadata']['name']
            division = self.json_response['data']['segments'][i]['stats']['division']['metadata']['name']
            mmr = self.json_response['data']['segments'][i]['stats']['rating']['value']

            player_ranks[gamemode] = [rank, division, mmr]

        return player_ranks


class SteamFetcher:
    def __init__(self, steamid):
        self.steamid = steamid

        api_key = os.environ['STEAM_API_KEY']
        link = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={self.steamid}'

        try:
            response = requests.get(link)
            json_response = json.loads(response.text)
            self.json_response = json_response
        except:
            print('SteamFetcher not initialized with attribute: json_response')

    def get_username(self):
        return self.json_response['response']['players'][0]['personaname']
