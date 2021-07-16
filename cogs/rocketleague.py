import os
from dotenv import load_dotenv

from fetchers import TRNFetcher
from database import initiate_cluster, create_user

import discord
from discord.ext import commands
from discord_slash import cog_ext


load_dotenv()  # load env variables


CONNECTION_URL = os.environ['CONNECTION_URL']
GUILD_IDS = [756176094335467601, 852338789506613278]
DESCRIPTIONS = ['Retrieve a player\'s Rocket League ranks!',
                'Retrieve a linked player\'s Rocket League ranks!',
                'Link your Rocket League ranks to your Discord account.',
                'Plug for Bakkesmod.']

# VGA_ID: 756176094335467601


class RocketLeague(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(description=DESCRIPTIONS[0], guild_ids=GUILD_IDS)
    async def ranks(self, ctx, platform, *, identifier):
        try:
            trn_fetcher = TRNFetcher(platform, identifier)
            embed = create_embed(trn_fetcher)

            await ctx.send(embed=embed)
        except KeyError:
            await ctx.send('User could not be found.')

    @cog_ext.cog_slash(description=DESCRIPTIONS[1], guild_ids=GUILD_IDS)
    async def myranks(self, ctx, mention: discord.User=None):
        collection = initiate_cluster(CONNECTION_URL)

        if mention is None:
            query = {'_id': ctx.author.id}
        else:
            query = {'_id': mention.id}

        user = collection.find_one(query)

        if user is None:
            await ctx.send('You don\'t have a linked account, try `/link` first.')
        else:
            platform = user['platform']
            identifier = user['identifier']

	    # can't call another command so copied for now
            try:
                trn_fetcher = TRNFetcher(platform, identifier)
                embed = create_embed(trn_fetcher)

                await ctx.send(embed=embed)
            except KeyError:
                await ctx.send('User could not be found.')

    @cog_ext.cog_slash(description=DESCRIPTIONS[2], guild_ids=GUILD_IDS)
    async def link(self, ctx, platform, *, identifier):
        collection = initiate_cluster(CONNECTION_URL)
        query = {'_id': ctx.author.id}

        if collection.find_one(query) is not None:
            collection.update_one(query, {"$set": {'platform': platform}})
            collection.update_one(query, {"$set": {'identifier': identifier}})

            await ctx.send('Updated ranks successfully.')
        else:
            create_user(collection, ctx.author.id, platform, identifier)
            await ctx.send('Linked ranks successfully.')

    @cog_ext.cog_slash(description=DESCRIPTIONS[3], guild_ids=GUILD_IDS)
    async def bakkes(self, ctx):
        link = 'https://www.bakkesmod.com/download.php'
        await ctx.send(f'Bakkesmod is a mod for Rocket League that adds a wide variety of features to the game including customized '
                       f'training, client-side access to all cosmetic items, and the ability to see real-time MMR in-game\n'
                       f'Download here: {link}')


def create_embed(trn_fetcher):
    username = trn_fetcher.get_username()
    avatar_url = trn_fetcher.get_pfp()

    ranks = trn_fetcher.get_ranks()
    current_season = trn_fetcher.get_current_season()
    best_percentile, best_gamemode = trn_fetcher.get_best_gamemode()

    embed = discord.Embed(title=f'{username}\'s ranks:',
                          description=f'Season {current_season - 14}',
                          color=trn_fetcher.get_rank_color())

    for gamemode in list(ranks.keys()):
        if gamemode != 'Un-Ranked':
            embed.add_field(name=gamemode,
                            value=f"{ranks[gamemode]['rank']}, {ranks[gamemode]['division']} ({ranks[gamemode]['mmr']})",
                            inline=False)

    if avatar_url is None:
        avatar_url = 'https://images-eds-ssl.xboxlive.com/image?url=8Oaj9Ryq1G1_p3lLnXlsaZgGzAie6Mnu24_PawYuDYIoH77pJ.X5Z.MqQPibUVTcS9jr0n8i7LY1tL3U7AiafX4CBXlmeNYIlNDtmq5GybCrf_ehzIV6VDRULqrr283j'

    embed.set_thumbnail(url=avatar_url)
    embed.set_footer(text=f'You are in the top {100 - best_percentile:.2f}% in {best_gamemode}!')

    return embed
