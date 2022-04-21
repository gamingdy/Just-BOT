import discord
from discord.ext import commands
import sqlite3
import asyncio


class EventHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect("data/bot_db.db")

    async def user_slowmode(self, channel, user, delay):
        await channel.set_permissions(user, send_messages=False)
        await asyncio.sleep(delay)
        await channel.set_permissions(user, send_messages=None)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        author = ctx.author
        channel = ctx.channel

        db_row = (
            self.db.cursor()
            .execute(
                "SELECT * FROM slowmode_info WHERE channel_id=(?) AND user_id=(?)",
                (channel.id, author.id),
            )
            .fetchall()
        )
        if db_row:
            await self.user_slowmode(channel, author, db_row[0][2])


def setup(bot):
    bot.add_cog(EventHandler(bot))
