import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

from cogs.rocketleague import RocketLeague


load_dotenv()

bot = commands.Bot(command_prefix='!', case_insensitive=True, help_command=None)


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online)
    print(f'{bot.user.name} is online.')


bot.add_cog(RocketLeague(bot))

bot.run(os.environ['DISCORD'])
