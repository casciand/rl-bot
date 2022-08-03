import os
import json
import requests
import discord

from dotenv import load_dotenv


load_dotenv()  # load env variables

TRN_API_KEY = os.environ.get('TRN_API_KEY')


class TRNFetcher:
    def __init__(self, platform, identifier):
        self.platform = platform
        self.identifier = identifier

        link = f'https://api.tracker.gg/api/v2/rocket-league/standard/profile/{self.platform}/{self.identifier}'
        headers = {
            'TRN-Api-Key': TRN_API_KEY,
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
        }

        response = requests.get(link, headers=headers)
        response.raise_for_status()  # raise error if bad status code
        self.response = json.loads(response.text)

    def get_username(self):
        return self.response['data']['platformInfo']['platformUserHandle']

    def get_current_season(self):
        return self.response['data']['metadata']['currentSeason']

    def get_pfp(self):
        return self.response['data']['platformInfo']['avatarUrl']

    def get_ranks(self):
        ranks = {}

        for i in range(1, 10):
            try:
                playlist = self.response['data']['segments'][i]
                gamemode = playlist['metadata']['name']

                rank = playlist['stats']['tier']['metadata']['name']
                division = playlist['stats']['division']['metadata']['name']
                mmr = playlist['stats']['rating']['value']

                stats = {'rank': rank,
                         'division': division,
                         'mmr': mmr}

                ranks[gamemode] = stats
            except IndexError:
                continue

        return ranks

    def get_best_gamemode(self):
        best_gamemode = ''
        best_percentile = 0

        for i in range(1, 10):
            try:
                playlist = self.response['data']['segments'][i]

                percentile = playlist['stats']['tier']['percentile']
                gamemode = playlist['metadata']['name']

                if percentile is not None and percentile > best_percentile:
                    best_percentile = percentile
                    best_gamemode = gamemode
            except IndexError:
                continue

        return best_percentile, best_gamemode

    def get_rank_color(self):
        highest_value = -1

        for i in range(1, 9):
            value = self.response['data']['segments'][i]['stats']['tier']['value']

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
