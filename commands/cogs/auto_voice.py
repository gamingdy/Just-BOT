import time

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from config import database
from Utils.funct import create_embed
from Utils.custom_error import (
    NotGuildOwner,
    NotConnectedInVoiceChannel,
    NotVoiceChannelAdmin,
)


class AutoVoice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    auto_voice = SlashCommandGroup(name="voice", description="Auto voice command")
    blocklist = auto_voice.create_subgroup(
        name="block", description="Manage blocklist channel"
    )
    whitelist = auto_voice.create_subgroup(
        name="white", description="Manage whitelist channel"
    )

    async def connected_admin(ctx):
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
                        return True
            else:
                raise NotVoiceChannelAdmin("You are not channel admin")

        raise NotConnectedInVoiceChannel("You are not connected in voice channel")

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

    @auto_voice.command(description="Change name of current voice channel")
    @commands.check(connected_admin)
    @commands.cooldown(rate=1, per=60, type=commands.BucketType.member)
    async def name(self, ctx, name: str):
        cooldown_time = round(time.time() + 60)
        await ctx.author.voice.channel.edit(name=name)
        await ctx.respond(
            f"The new channel name is `{name}`. You will be able to modify it in <t:{cooldown_time}:R>"
        )

    @blocklist.command(description="Add user to voice channel block list")
    @commands.check(connected_admin)
    async def add(self, ctx, user: discord.Member):
        voice_channel = ctx.author.voice.channel

        cursor = database.cursor()
        is_blocked = cursor.execute(
            "SELECT * FROM blocklist WHERE channel_id=(?) AND user_id=(?)",
            (
                voice_channel.id,
                user.id,
            ),
        ).fetchone()
        if is_blocked:
            message = "User is already blocked and can't be blocked twice 😀"
        else:
            is_whitelisted = cursor.execute(
                "SELECT * FROM whitelist WHERE channel_id=(?) AND user_id=(?)",
                (
                    voice_channel.id,
                    user.id,
                ),
            ).fetchone()
            warn = ""
            if is_whitelisted:
                cursor.execute(
                    "DELETE FROM whitelist WHERE channel_id=(?) AND user_id=(?)",
                    (
                        voice_channel.id,
                        user.id,
                    ),
                )
                warn = ":warning: **The user was whitelisted and has been removed**"

            cursor.execute(
                "INSERT INTO blocklist (channel_id, user_id) VALUES (?,?) ",
                (
                    voice_channel.id,
                    user.id,
                ),
            )
            database.commit()
            message = f"{warn}\n\n{user.mention} is now blocklisted in channel <#{voice_channel.id}>"

            await voice_channel.set_permissions(user, connect=False)
            if user.voice:
                if user.voice.channel.id == voice_channel.id:
                    await user.move_to(None)

        embed = create_embed(
            title="Blocklist update", description=message, color=discord.Color.red()
        )
        await ctx.respond(embed=embed)

    @whitelist.command(description="Add user to voice channel whitelist")
    @commands.check(connected_admin)
    async def add(self, ctx, user: discord.Member):
        voice_channel = ctx.author.voice.channel

        cursor = database.cursor()
        is_whitelisted = cursor.execute(
            "SELECT * FROM whitelist WHERE channel_id=(?) AND user_id=(?)",
            (
                voice_channel.id,
                user.id,
            ),
        ).fetchone()
        if is_whitelisted:
            message = "User is already whitelisted"
        else:
            is_blocked = cursor.execute(
                "SELECT * FROM blocklist WHERE channel_id=(?) AND user_id=(?)",
                (
                    voice_channel.id,
                    user.id,
                ),
            ).fetchone()
            warn = ""
            if is_blocked:
                cursor.execute(
                    "DELETE FROM blocklist WHERE channel_id=(?) AND user_id=(?)",
                    (
                        voice_channel.id,
                        user.id,
                    ),
                )
                warn = ":warning: **The user was blocklisted and has been removed**"

            cursor.execute(
                "INSERT INTO whitelist (channel_id, user_id) VALUES (?,?) ",
                (
                    voice_channel.id,
                    user.id,
                ),
            )
            database.commit()
            message = f"{warn}\n\n{user.mention} is now whitelisted in channel <#{voice_channel.id}>"

        await voice_channel.set_permissions(user, connect=True)

        color = discord.Colour.from_rgb(255, 128, 243)
        embed = create_embed(title="Whitelist update", description=message, color=color)

        await ctx.respond(embed=embed)

    @blocklist.command(description="Remove user from channel blocklist")
    @commands.check(connected_admin)
    async def remove(self, ctx, user: discord.Member):
        voice_channel = ctx.author.voice.channel
        cursor = database.cursor()

        is_blocked = cursor.execute(
            "SELECT * FROM blocklist WHERE channel_id=(?) AND user_id=(?)",
            (
                voice_channel.id,
                user.id,
            ),
        ).fetchone()

        if not is_blocked:
            message = "User is not blocklisted"
        else:

            cursor.execute(
                "DELETE FROM blocklist WHERE channel_id=(?) and user_id=(?)",
                (
                    voice_channel.id,
                    user.id,
                ),
            )

            database.commit()

            message = "User has been removed from blocklist"
            await voice_channel.set_permissions(user, overwrite=None)

        embed = create_embed(title="Blocklist update", description=message)
        await ctx.respond(embed=embed)

    @whitelist.command(description="Remove user from channel whitelist")
    @commands.check(connected_admin)
    async def remove(self, ctx, user: discord.Member):
        voice_channel = ctx.author.voice.channel
        cursor = database.cursor()
        is_whitelisted = cursor.execute(
            "SELECT * FROM whitelist WHERE channel_id=(?) AND user_id=(?)",
            (
                voice_channel.id,
                user.id,
            ),
        ).fetchone()
        if not is_whitelisted:
            message = "User is not whitelisted"
        else:

            cursor.execute(
                "DELETE FROM whitelist WHERE channel_id=(?) and user_id=(?)",
                (
                    voice_channel.id,
                    user.id,
                ),
            )

            database.commit()
            message = "User has been removed from whitelist"
            await voice_channel.set_permissions(user, overwrite=None)

        embed = create_embed(title="Whitelist update", description=message)
        await ctx.respond(embed=embed)

    @auto_voice.command(description="Set current channel as private channel")
    @commands.check(connected_admin)
    async def private(self, ctx):
        voice_channel = ctx.author.voice.channel
        cursor = database.cursor()
        cursor.execute(
            "UPDATE active_voice SET open=(?) WHERE channel_id=(?)",
            (
                False,
                voice_channel.id,
            ),
        )
        database.commit()
        everyone_role = ctx.guild.default_role
        await voice_channel.set_permissions(everyone_role, connect=False)
        embed = create_embed("Channel Update", description="The channel is now private")

        await ctx.respond(embed=embed)

    @auto_voice.command(description="Set current channel as public channel")
    @commands.check(connected_admin)
    async def public(self, ctx):
        voice_channel = ctx.author.voice.channel
        cursor = database.cursor()
        cursor.execute(
            "UPDATE active_voice SET open=(?) WHERE channel_id=(?)",
            (
                True,
                voice_channel.id,
            ),
        )
        database.commit()
        everyone_role = ctx.guild.default_role
        await voice_channel.set_permissions(everyone_role, connect=None)
        embed = create_embed("Channel Update", description="The channel is now public")

        await ctx.respond(embed=embed)
def setup(bot):
    bot.add_cog(AutoVoice(bot))
