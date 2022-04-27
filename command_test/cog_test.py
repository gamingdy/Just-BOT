import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
import sqlite3

from Utils.funct import create_embed


class TestCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    test_command = SlashCommandGroup("test", "Test command")

    @test_command.command()
    async def test(self, ctx):
        print("oui")


def setup(bot):
    bot.add_cog(TestCommand(bot))
