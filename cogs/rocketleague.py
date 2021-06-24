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
    async def rl(self, ctx):
        await ctx.send('rocket league')

    @commands.command()
    async def ranks(self, ctx, platform, username):
        pass


def fetch_json(platform, username):
    trn_link = f'https://public-api.tracker.gg/api/v2/rocket-league/standard/profile/{platform}/{username}'
    api_key = os.environ['TRN_API_KEY']
    headers = {
        'TRN-Api-Key': api_key
    }

    response = requests.get(trn_link, headers=headers)
    print(response.content)
    json_response = json.loads(response.text)

    return json_response


print(fetch_json('steam', '76561198971399813'))


def get_ranks(platform, username):
    json_response = fetch_json(platform, username)
