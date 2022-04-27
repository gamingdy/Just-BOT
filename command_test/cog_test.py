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
                "SELECT delay,user_name_discriminator FROM slowmode_info WHERE channel_id = (?) ORDER BY delay DESC",
                (channel.id,),
            )
            .fetchall()
        )
        if element:
            all_page = [elem[i : i + 5] for i in range(0, len(elem), 5)]

            actual_page = 1


def setup(bot):
    bot.add_cog(TestCommand(bot))
