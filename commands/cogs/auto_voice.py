import time

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from config import database
from Utils.funct import create_embed, guild_owner
from Utils.voice_tools import (
    add_user,
    remove_user,
    update_channel,
    channel_list,
    connected_admin,
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

        block_user = add_user(voice_channel, user, "blocklist")

        if block_user["result"]:
            message = block_user["msg"]
            await voice_channel.set_permissions(user, connect=False)
            if user.voice:
                if user.voice.channel.id == voice_channel.id:
                    await user.move_to(None)

        else:
            message = "User is already blocked and can't be blocked twice 😀"

        embed = create_embed(
            title="Blocklist update", description=message, color=discord.Color.red()
        )
        await ctx.respond(embed=embed)

    @whitelist.command(description="Add user to voice channel whitelist")
    @commands.check(connected_admin)
    async def add(self, ctx, user: discord.Member):
        voice_channel = ctx.author.voice.channel
        whitelist_user = add_user(voice_channel, user, "whitelist")

        if not whitelist_user["result"]:
            message = "User is already whitelisted"
        else:
            message = whitelist_user["msg"]
            await voice_channel.set_permissions(user, connect=True)

        color = discord.Colour.from_rgb(255, 128, 243)
        embed = create_embed(title="Whitelist update", description=message, color=color)

        await ctx.respond(embed=embed)

    @blocklist.command(description="Remove user from channel blocklist")
    @commands.check(connected_admin)
    async def remove(self, ctx, user: discord.Member):
        voice_channel = ctx.author.voice.channel
        message = await remove_user(voice_channel, user, "blocklist")
        embed = create_embed(title="Blocklist update", description=message)
        await ctx.respond(embed=embed)

    @whitelist.command(description="Remove user from channel whitelist")
    @commands.check(connected_admin)
    async def remove(self, ctx, user: discord.Member):
        voice_channel = ctx.author.voice.channel
        message = await remove_user(voice_channel, user, "whitelist")
        embed = create_embed(title="Whitelist update", description=message)
        await ctx.respond(embed=embed)

    @auto_voice.command(description="Set current channel as private channel")
    @commands.check(connected_admin)
    async def private(self, ctx):
        voice_channel = ctx.author.voice.channel
        everyone_role = ctx.guild.default_role
        await update_channel(voice_channel, everyone_role, False)
        embed = create_embed("Channel Update", description="The channel is now private")

        await ctx.respond(embed=embed)

    @auto_voice.command(description="Set current channel as public channel")
    @commands.check(connected_admin)
    async def public(self, ctx):
        voice_channel = ctx.author.voice.channel
        everyone_role = ctx.guild.default_role
        await update_channel(voice_channel, everyone_role, True)
        embed = create_embed("Channel Update", description="The channel is now public")

        await ctx.respond(embed=embed)

    @blocklist.command(description="Show current channel blocklist")
    @commands.check(connected_admin)
    async def list(self, ctx):
        voice_channel = ctx.author.voice.channel
        message = channel_list(voice_channel, ctx.guild, "blocklist")
        embed = create_embed("Blocklist", message)
        await ctx.respond(embed=embed)

    @whitelist.command(description="Show current channel whitelist")
    @commands.check(connected_admin)
    async def list(self, ctx):
        voice_channel = ctx.author.voice.channel
        message = channel_list(voice_channel, ctx.guild, "whitelist")
        embed = create_embed("Whitelist", message)
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(AutoVoice(bot))
