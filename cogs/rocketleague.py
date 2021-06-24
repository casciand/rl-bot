from fetchers import TRNFetcher, SteamFetcher
from dotenv import load_dotenv

import discord
from discord.ext import commands
import asyncio


load_dotenv()


class RocketLeague(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ranks(self, ctx, platform, *, username):
        await ctx.send('Fetching ranks...')
        try:
            trn_fetcher = TRNFetcher(platform, username)  # gets json containing player info

            if platform == 'steam':
                steam_fetcher = SteamFetcher(username)
                username = steam_fetcher.get_username()

            player_ranks = trn_fetcher.get_ranks()
            current_season = trn_fetcher.get_current_season()
            avatar_url = trn_fetcher.get_pfp()

            keys = list(player_ranks.keys())

            embed = discord.Embed(title=f'{username}\'s ranks:', description=f'Season {current_season - 14}', color=discord.Colour.dark_purple())
            embed.set_thumbnail(url=avatar_url)

            for i in range(len(keys)):
                gamemode = keys[i]

                if gamemode != 'Un-Ranked':
                    embed.add_field(name=keys[i], value=f'{player_ranks[gamemode][0]}, {player_ranks[gamemode][1]} ({player_ranks[gamemode][2]})', inline=False)

            await ctx.send(embed=embed)
            print(f'Successfully retrieved {username}\'s ranks')
        except:
            await ctx.send('Invalid platform/name. Please try again.')
            print(f'Failed to retrieve {username}\'s ranks')

    @commands.command(aliases=['bakkes'])
    async def bakkesmod(self, ctx):
        link = 'https://www.bakkesmod.com/'
        await ctx.send(f'Bakkesmod is a mod for Rocket League that adds a wide variety of features to the game including customized '
                       f'training, client-side access to all cosmetic items, and the ability to see real-time MMR in-game\n'
                       f'Bakkesmod can be downloaded here: {link}')

    @commands.command()
    async def goal(self, ctx):
        for _ in range(3):
            await ctx.send('What a save!')
            await asyncio.sleep(.2)

