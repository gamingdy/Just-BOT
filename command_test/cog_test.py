from discord.commands import SlashCommandGroup
from discord.ext import commands


class TestCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    test_command = SlashCommandGroup("test", "Test command")

    @test_command.command()
    async def test(self, ctx):
        await ctx.respond("test")


def setup(bot):
    bot.add_cog(TestCommand(bot))
