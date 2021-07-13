import os
from dotenv import load_dotenv

import discord
from discord.ext import commands
from discord_slash import SlashCommand

from cogs.rocketleague import RocketLeague


load_dotenv()  # load env variables


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('/link'))
    print(f'{bot.user.name} is online.')


bot.add_cog(RocketLeague(bot))

bot.run(os.environ['DISCORD'])
