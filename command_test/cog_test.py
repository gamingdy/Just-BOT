import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

from Utils.funct import create_embed
from Utils.create_page import generate_page, PageNavigation
from config import database


class TestCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    test_command = SlashCommandGroup("test", "Test command")

    @test_command.command()
    async def test(self, ctx):
        print(42 / 0)


def setup(bot):
    bot.add_cog(TestCommand(bot))
