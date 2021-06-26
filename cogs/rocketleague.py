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
        try:
            trn_fetcher = TRNFetcher(platform, username)  # gets json containing player info

            if platform == 'steam':
                steam_fetcher = SteamFetcher(username)
                username = steam_fetcher.get_username()

            player_ranks = trn_fetcher.get_ranks()
            current_season = trn_fetcher.get_current_season()
            avatar_url = trn_fetcher.get_pfp()
            best_percentile, best_gamemode = trn_fetcher.get_highest_percentile()

            keys = list(player_ranks.keys())

            embed = discord.Embed(title=f'{username}\'s ranks:', description=f'Season {current_season - 14}', color=trn_fetcher.get_rank_color())
            embed.set_thumbnail(url=avatar_url)
            embed.set_footer(text=f'You are in the top {100 - best_percentile:.2f}% in {best_gamemode}!')

            for i in range(len(keys)):
                gamemode = keys[i]

                if gamemode != 'Un-Ranked':
                    embed.add_field(name=gamemode, value=f'{player_ranks[gamemode][0]}, {player_ranks[gamemode][1]} ({player_ranks[gamemode][2]})', inline=False)

            await ctx.send(embed=embed)
            print(f'Successfully retrieved {username}\'s ranks')
        except KeyError as e:
            await ctx.send('Player not found. Please try again.')
            print(f'Failed to retrieve {username}\'s ranks\nerror: {e}')

    @commands.command(aliases=['bakkes'])
    async def bakkesmod(self, ctx):
        link = 'https://www.bakkesmod.com/download.php'
        await ctx.send(f'Bakkesmod is a mod for Rocket League that adds a wide variety of features to the game including customized '
                       f'training, client-side access to all cosmetic items, and the ability to see real-time MMR in-game\n'
                       f'Download here: {link}')

    @commands.command()
    async def goal(self, ctx):
        for _ in range(3):
            await ctx.send('What a save!')
            await asyncio.sleep(.2)
