import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from cogs.rocketleague import RocketLeague


load_dotenv()  # load env variables

token = os.environ.get('DISCORD')
bot = commands.Bot(token=token)


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('/link'))
    print(f'{bot.user.name} is online.')


bot.add_cog(RocketLeague(bot))
bot.run(token)
