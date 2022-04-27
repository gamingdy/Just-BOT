import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
import sqlite3

from Utils.funct import create_embed, create_page


class TestCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect("data/bot_db.db")

    test_command = SlashCommandGroup("test", "Test command")

    @test_command.command()
    async def test(self, ctx):
        channel = ctx.channel
        element = (
            self.db.cursor()
            .execute(
                "SELECT * FROM slowmode_info WHERE channel_id = (?)  ORDER BY delay DESC",
                (channel.id,),
            )
            .fetchall()
        )
        if element:
            all_page = {}
            for i in range(0, len(element), 5):
                t = 1 if i == 0 else (i // 5) + 1
                all_page[t] = element[i : i + 5]

            actual_page = 1


def setup(bot):
    bot.add_cog(TestCommand(bot))
