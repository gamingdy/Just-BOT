import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from config import database
from Utils.funct import create_embed
from Utils.custom_error import NotGuildOwner


class AutoVoice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    auto_voice = SlashCommandGroup(name="voice", description="Auto voice command")

    def connected_admin(self, ctx):
        voice_state = ctx.author.voice
        if voice_state:
            voice_cursor = database.cursor()
            is_admin = voice_cursor.execute(
                "SELECT channel_id FROM active_voice WHERE author_id=(?)",
                (ctx.author.id,),
            ).fetchall()
            if len(is_admin) > 0:
                for channel in is_admin:
                    if channel[0] == voice_state.channel.id:
                        return (True, "")
            else:
                return (False, "You are not channel admin")

        return (False, "You are not connected in voice channel")

    async def guild_owner(ctx):
        if ctx.guild.owner_id == ctx.author.id:
            return True
        raise NotGuildOwner("You are not guild owner ")

    @auto_voice.command(description="Configure auto voice channel")
    @commands.check(guild_owner)
    async def config(self, ctx, channel: discord.VoiceChannel):
        voice_cursor = database.cursor()
        active_voice_channel = voice_cursor.execute(
            "SELECT channel_id FROM auto_voice WHERE guild_id=(?)", (ctx.guild.id,)
        ).fetchall()
        if active_voice_channel:
            voice_cursor.execute(
                "UPDATE auto_voice SET channel_id=(?) WHERE guild_id=(?)",
                (
                    channel.id,
                    ctx.guild.id,
                ),
            )
        else:
            voice_cursor.execute(
                "INSERT INTO auto_voice (guild_id, channel_id) VALUES (?,?)",
                (
                    ctx.guild.id,
                    channel.id,
                ),
            )
        database.commit()
        await ctx.respond(
            "The <#{}> channel is now configured as auto voice channel".format(
                channel.id
            )
        )

    @auto_voice.command(description="Disable auto voice channel")
    @commands.check(guild_owner)
    async def disable(self, ctx):
        voice_cursor = database.cursor()
        voice_cursor.execute(
            "DELETE FROM auto_voice WHERE guild_id=(?)", (ctx.guild.id,)
        )
        database.commit()
        await ctx.respond("Auto voice are now disable in this guild")

    @auto_voice.command(description="Change name of current voice channel", name="name")
    async def change_name(self, ctx, name: str):
        connected_admin = self.connected_admin(ctx)
        if connected_admin[0]:
            await ctx.respond("Hello admin")
        else:
            await ctx.respond(connected_admin[1])


def setup(bot):
    bot.add_cog(AutoVoice(bot))
