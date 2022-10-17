import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from config import database


class AutoVoice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    auto_voice = SlashCommandGroup(name="voice", description="Auto voice command")

    @auto_voice.command(description="Config auto voice channel")
    async def config(self, ctx, channel: discord.VoiceChannel):
        voice_cursor = database.cursor()
        active_voice_channel = voice_cursor.execute("SELECT channel_id FROM auto_voice WHERE guild_id=(?)",
                                                    (ctx.guild.id, )).fetchall()
        if active_voice_channel:
            voice_cursor.execute("UPDATE auto_voice SET channel_id=(?) WHERE guild_id=(?)", (channel.id, ctx.guild.id))
        else:
            voice_cursor.execute("INSERT INTO auto_voice (guild_id, channel_id) VALUES (?,?)",
                                 (ctx.guild.id, channel.id,))
        database.commit()
        await ctx.respond("The <#{}> channel is now configured as auto voice channel".format(channel.id))


def setup(bot):
    bot.add_cog(AutoVoice(bot))
