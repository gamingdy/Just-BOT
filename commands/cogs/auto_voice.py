from discord.commands import SlashCommandGroup
from discord.ext import commands
import discord


class AutoVoice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    auto_voice = SlashCommandGroup(name="voice", description="Auto voice command")

    @auto_voice.command(description="Config auto voice channel")
    async def config(self, ctx, channel_name):
        ...


def setup(bot):
    bot.add_cog(AutoVoice(bot))
