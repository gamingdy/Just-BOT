import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from config import database
from Utils.funct import create_embed


class AutoVoice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    auto_voice = SlashCommandGroup(name="voice", description="Auto voice command")

    @auto_voice.command(description="Configure auto voice channel")
    async def config(self, ctx, channel: discord.VoiceChannel):
        voice_cursor = database.cursor()
        active_voice_channel = voice_cursor.execute("SELECT channel_id FROM auto_voice WHERE guild_id=(?)",
                                                    (ctx.guild.id,)).fetchall()
        if active_voice_channel:
            voice_cursor.execute("UPDATE auto_voice SET channel_id=(?) WHERE guild_id=(?)", (channel.id, ctx.guild.id))
        else:
            voice_cursor.execute("INSERT INTO auto_voice (guild_id, channel_id) VALUES (?,?)",
                                 (ctx.guild.id, channel.id,))
        database.commit()
        await ctx.respond("The <#{}> channel is now configured as auto voice channel".format(channel.id))
    @auto_voice.command(description="Disable auto voice channel")
    async def disable(self, ctx):
        voice_cursor = database.cursor()
        voice_cursor.execute(
            "DELETE FROM auto_voice WHERE guild_id=(?)", (ctx.guild.id,)
        )
        await ctx.respond("Auto voice are now disable in this guild")


def setup(bot):
    bot.add_cog(AutoVoice(bot))
