import discord
import requests.exceptions
from discord.ext import commands
from dotenv import load_dotenv

from fetchers import TRNFetcher
from database import get_user, create_user


load_dotenv()  # load env variables

DEFAULT_PFP_URL = 'https://images-eds-ssl.xboxlive.com/image?url=8Oaj9Ryq1G1_p3lLnXlsaZgGzAie6Mnu24_PawYuDYIoH77' \
                  'pJ.X5Z.MqQPibUVTcS9jr0n8i7LY1tL3U7AiafX4CBXlmeNYIlNDtmq5GybCrf_ehzIV6VDRULqrr283j'
GUILD_IDS = [852338789506613278]  # VGA_ID: 756176094335467601
DESCRIPTIONS = ['Retrieve a player\'s Rocket League ranks!',
                'Retrieve a linked player\'s Rocket League ranks!',
                'Link your Rocket League ranks to your Discord account.',
                'Plug for Bakkesmod.']


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
        avatar_url = DEFAULT_PFP_URL

    embed.set_thumbnail(url=avatar_url)
    embed.set_footer(text=f'You are in the top {100 - best_percentile:.2f}% in {best_gamemode}!')

    return embed


class RocketLeague(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description=DESCRIPTIONS[0], guild_ids=GUILD_IDS)
    async def ranks(self, ctx, platform, *, identifier):
        try:
            try:
                trn_fetcher = TRNFetcher(platform, identifier)
            except requests.exceptions.RequestException as e:
                await ctx.respond(e)
                return

            embed = create_embed(trn_fetcher)

            await ctx.respond(embed=embed)
        except KeyError:
            await ctx.respond('User could not be found.')

    @commands.slash_command(description=DESCRIPTIONS[1], guild_ids=GUILD_IDS)
    async def myranks(self, ctx, mention: discord.User = None):
        if mention is None:
            user_id = ctx.author.id
        else:
            user_id = mention.id

        user = await get_user(user_id)

        if user is None:
            await ctx.respond('You don\'t have a linked account, try `/link` first.')
        else:
            platform = user['platform']
            identifier = user['identifier']

            await self.ranks(ctx, platform=platform, identifier=identifier)

    @commands.slash_command(description=DESCRIPTIONS[2], guild_ids=GUILD_IDS)
    async def link(self, ctx, platform, *, identifier):
        await create_user(ctx.author.id, platform, identifier)
        await ctx.respond('Linked ranks successfully.')
