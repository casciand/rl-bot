import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

from cogs.rocketleague import RocketLeague


load_dotenv()


class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()
        self.descriptions = {'ranks': 'Xbox: !ranks xbl <gamertag>\n'
                                      'Playstation: !ranks psn <onlineid>\n'
                                      'Epic: !ranks epic <username>\n'
                                      'Steam: !ranks steam <steamid>'}

    async def send_command_help(self, command):
        embed = discord.Embed(title=f'!{command} help',
                              description=self.descriptions[str(command)])
        await self.get_destination().send(embed=embed)


bot = commands.Bot(command_prefix='!', case_insensitive=True, help_command=CustomHelpCommand())


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online)
    print(f'{bot.user.name} is online.')


bot.add_cog(RocketLeague(bot))

bot.run(os.environ['DISCORD'])
