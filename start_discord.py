from remote import Remote
from discord.ext import commands
import discord


class Bot(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.client = Remote("localhost")

    async def on_ready(self):
        print("logged in as: ", self.user)
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your server"))


bot = Bot(command_prefix='&')
token = open(".TOKEN", "r").read()
bot.run(token)
