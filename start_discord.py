import json
from remote import Remote
from discord.ext import commands
import discord


class Bot(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)

        self.config = json.load(open("config.json", "r"))
        self.r = Remote(self.config["server_address"])

        @self.command(name="start", help="Starts the Minecraft server.")
        async def start(ctx):
            if self.r.status() == "stopped" or self.r.status() == "crashed":
                self.r.start()
                await self.announcement_channel.send("Starting the Minecraft server.")
            else:
                self.announcement_channel.send("Already started.")
            await self.verify_channel(ctx)

        @self.command(name="status", help="Shows the current status of the Minecraft server.")
        async def status(ctx):
            await self.announcement_channel.send("The server's current status is: " + self.r.status())
            await self.verify_channel(ctx)

        @self.command(name="stop", help="Stops the Minecraft server and displays its log.")
        async def stop(ctx):
            if self.r.status() == "running":
                await self.announcement_channel.send("Stopping server.")
                open("mclog.txt", "w").write(self.r.stop())
                await self.announcement_channel.send("Server stopped", file=discord.File("mclog.txt"))
            else:
                self.announcement_channel.send("Already stopped.")
            await self.verify_channel(ctx)

        @self.command(name="log", help="Displays the Minecraft server's log.")
        async def log(ctx):
            open("mclog.txt", "w").write(self.r.log())
            await self.announcement_channel.send("Server stopped", file=discord.File("mclog.txt"))
            await self.verify_channel(ctx)

        @self.command(name="setchannel", help="Changes the bot channel.")
        async def setchannel(ctx):
            self.announcement_channel = ctx.channel
            await self.announcement_channel.send("This channel is now set as the announcement channel.")
            self.config["bot_channel"] = ctx.channel.id
            json.dump(self.config, open("config.json", "w"))

    async def verify_channel(self, ctx):
        if self.announcement_channel is None:
            self.announcement_channel = ctx.channel
            await self.announcement_channel.send("This channel is now set as the announcement channel. "
                                                 "Use &setchannel in another channel to change it.")
            self.config["bot_channel"] = ctx.channel.id
            json.dump(self.config, open("config.json", "w"))

    async def set_announcement_channel(self, channel_id):
        self.announcement_channel = await self.fetch_channel(channel_id)
        await self.announcement_channel.send("The Discord bot is now started.")

    async def on_ready(self):
        print("logged in as: ", self.user)
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your server"))
        if self.config["bot_channel"] is None:
            self.announcement_channel = None
        else:
            await self.set_announcement_channel(self.config["bot_channel"])


bot = Bot(command_prefix='&')
token = open(".TOKEN", "r").read()
bot.run(token)
