import os

from fetchers import TRNFetcher, SteamFetcher
from database import initiate_cluster, create_user
from dotenv import load_dotenv

import discord
from discord.ext import commands
from discord_slash import cog_ext
import asyncio


load_dotenv()  # load env variables


CONNECTION_URL = os.environ['CONNECTION_URL']
GUILD_IDS = [852338789506613278]


def create_embed(trn_fetcher, identifier):
    player_ranks = trn_fetcher.get_ranks()
    current_season = trn_fetcher.get_current_season()
    avatar_url = trn_fetcher.get_pfp()
    best_percentile, best_gamemode = trn_fetcher.get_highest_percentile()

    keys = list(player_ranks.keys())

    embed = discord.Embed(title=f'{identifier}\'s ranks:',
                          description=f'Season {current_season - 14}',
                          color=trn_fetcher.get_rank_color())
    embed.set_thumbnail(url=avatar_url)
    embed.set_footer(text=f'You are in the top {100 - best_percentile:.2f}% in {best_gamemode}!')

    for i in range(len(keys)):
        gamemode = keys[i]

        if gamemode != 'Un-Ranked':
            embed.add_field(name=gamemode,
                            value=f'{player_ranks[gamemode][0]}, {player_ranks[gamemode][1]} ({player_ranks[gamemode][2]})',
                            inline=False)

    return embed


class RocketLeague(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(description='Retrieve a players Rocket League ranks!', guild_ids=GUILD_IDS)
    async def rlranks(self, ctx, platform=None, *, identifier=None):
        if not (platform or identifier):
            collection = initiate_cluster(CONNECTION_URL)
            query = {'_id': ctx.author.id}

            user = collection.find_one(query)
            platform = user['platform']
            identifier = user['identifier']
            trn_fetcher = TRNFetcher(platform, identifier)
        else:
            trn_fetcher = TRNFetcher(platform, identifier)  # gets json containing player info

        if platform == 'steam':
            steam_fetcher = SteamFetcher(identifier)
            identifier = steam_fetcher.get_username()

        embed = create_embed(trn_fetcher, identifier)

        await ctx.send(embed=embed)
        print(f'Successfully retrieved {identifier}\'s ranks')

    @cog_ext.cog_slash(description='Link your Rocket League ranks to your Discord account.', guild_ids=GUILD_IDS)
    async def linkrl(self, ctx, platform, *, identifier):
        collection = initiate_cluster(CONNECTION_URL)
        query = {'_id': ctx.author.id}

        if collection.find_one(query) is not None:
            collection.update_one(query, {"$set": {'platform': platform}})
            collection.update_one(query, {"$set": {'identifier': identifier}})
            await ctx.send('Updated rank link.')
        else:
            create_user(collection, ctx.author.id, platform, identifier)
            await ctx.send('Your ranks have been linked to your account.')

    @cog_ext.cog_slash(name='bakkes', description='Plug for Bakkesmod.', guild_ids=GUILD_IDS)
    async def bakkesmod(self, ctx):
        link = 'https://www.bakkesmod.com/download.php'
        await ctx.send(f'Bakkesmod is a mod for Rocket League that adds a wide variety of features to the game including customized '
                       f'training, client-side access to all cosmetic items, and the ability to see real-time MMR in-game\n'
                       f'Download here: {link}')

    @cog_ext.cog_slash(description='Toxicity at its finest.', guild_ids=GUILD_IDS)
    async def goal(self, ctx):
        for _ in range(3):
            await ctx.send('What a save!')
            await asyncio.sleep(.2)
