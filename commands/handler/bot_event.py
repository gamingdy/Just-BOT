import discord
from discord.ext import commands
import sqlite3


class EventHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect("data/bot_db.db")

    @commands.Cog.listener()
    async def on_message(self, message):
        pass


def setup(bot):
    bot.add_cog(EventHandler(bot))
