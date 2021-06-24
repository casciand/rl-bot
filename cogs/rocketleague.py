import json
import os
import requests

from dotenv import load_dotenv

import discord
from discord.ext import commands


load_dotenv()


class RocketLeague(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ranks(self, ctx, platform, username):
        try:
            player_ranks, current_season, avatar_url = get_ranks(platform, username)
            keys = list(player_ranks.keys())

            embed = discord.Embed(title=f'{username}\'s ranks:', description=f'Season {current_season - 14}')
            embed.set_thumbnail(url=avatar_url)

            for i in range(len(player_ranks)):
                gamemode = keys[i]
                embed.add_field(name=keys[i], value=f'{player_ranks[gamemode][0]}, {player_ranks[gamemode][1]} ({player_ranks[gamemode][2]})')

            await ctx.send(embed=embed)
        except KeyError:
            await ctx.send('Invalid platform/name. Please try again.')


def fetch_json(platform, username):
    trn_link = f'https://api.tracker.gg/api/v2/rocket-league/standard/profile/{platform}/{username}'
    api_key = os.environ['TRN_API_KEY']
    headers = {
        'TRN-Api-Key': api_key,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
    }

    response = requests.get(trn_link, headers=headers)
    json_response = json.loads(response.text)

    return json_response


def get_ranks(platform, username):
    json_response = fetch_json(platform, username)
    current_season = json_response['data']['metadata']['currentSeason']
    avatar_url = json_response['data']['platformInfo']['avatarUrl']
    player_ranks = {}

    for i in range(2, 9):
        gamemode = json_response['data']['segments'][i]['metadata']['name']
        rank = json_response['data']['segments'][i]['stats']['tier']['metadata']['name']
        division = json_response['data']['segments'][i]['stats']['division']['metadata']['name']
        mmr = json_response['data']['segments'][i]['stats']['rating']['value']

        player_ranks[gamemode] = [rank, division, mmr]

    return player_ranks, current_season, avatar_url
