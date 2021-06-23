import discord
from discord.ext import commands


class RocketLeague(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rl(self, ctx):
        await ctx.send('rocket league')
