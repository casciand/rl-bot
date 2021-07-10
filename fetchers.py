import os
import json
import requests

from dotenv import load_dotenv
import discord


load_dotenv()  # load env variables


class TRNFetcher:
    def __init__(self, platform, username):
        self.platform = platform
        self.username = username

        link = f'https://api.tracker.gg/api/v2/rocket-league/standard/profile/{self.platform}/{self.username}'
        headers = {
            'TRN-Api-Key': os.environ['TRN_API_KEY'],
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

    def get_highest_percentile(self):
        best_gamemode = ''
        best_percentile = -1

        for i in range(1, 9):
            percentile = self.json_response['data']['segments'][i]['stats']['tier']['percentile']
            gamemode = self.json_response['data']['segments'][i]['metadata']['name']

            if percentile is not None and percentile > best_percentile:
                best_percentile = percentile
                best_gamemode = gamemode

        return best_percentile, best_gamemode

    def get_rank_color(self):
        highest_value = -1

        for i in range(1, 9):
            value = self.json_response['data']['segments'][i]['stats']['tier']['value']

            if value is not None and value > highest_value:
                highest_value = value
        if highest_value >= 22:
            color = discord.Colour.from_rgb(246, 246, 246)  # silver
        elif highest_value >= 19:
            color = discord.Colour.from_rgb(244, 16, 69)  # light red
        elif highest_value >= 16:
            color = discord.Colour.from_rgb(144, 96, 216)  # light purple
        elif highest_value >= 13:
            color = discord.Colour.from_rgb(10, 117, 255)  # dark blue
        elif highest_value >= 10:
            color = discord.Colour.from_rgb(168, 235, 252)  # light blue
        elif highest_value >= 7:
            color = discord.Colour.from_rgb(210, 165, 40)  # gold
        elif highest_value >= 4:
            color = discord.Colour.from_rgb(122, 122, 122)  # silver
        else:
            color = discord.Colour.from_rgb(119, 63, 2)  # bronze

        return color


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
