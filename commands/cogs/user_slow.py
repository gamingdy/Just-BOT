import time
import typing

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from discord.utils import escape_markdown

from Utils.create_page import PageNavigation
from Utils.funct import create_embed, get_active_slowmode
from config import database


class ManageSlowmode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    slowmode_commands = SlashCommandGroup("slowmode", "Manage channel slowmode")

    async def add_user_in_field(
        self, emb_message, list_user, field_value, bin_message=None, user_info=None
    ):
        for keys, user in enumerate(list_user):
            if keys < 5:
                emb_message.add_field(
                    name=user[5],
                    value=field_value.format(user[2]),
                    inline=False,
                )
            if bin_message:
                bin_message += user_info.format(
                    keys + 1, user[5], field_value.format(user[2])
                )
        return bin_message

    async def loading_bar(self, message, pourcentage, prev, last_refresh):
        pourc = int(pourcentage * 10)
        loaded = "🟩"
        unloaded = "🟥"
        if prev != pourc:
            prev = pourc
            if time.time() - last_refresh > 1:
                last_refresh = time.time()
                await message.edit_original_reponse(
                    content=(loaded * prev) + (unloaded * (10 - prev))
                )

        return prev, last_refresh

    @slowmode_commands.command()
    @commands.has_permissions(manage_messages=True)
    async def enable(
        self, ctx, target: typing.Union[discord.User, discord.Role], slowmode_delay: int
    ):
        is_role = isinstance(target, discord.Role)
        if not is_role and target.id == self.bot.user.id:
            await ctx.respond("You can't slowmode bot")
            return

        if slowmode_delay <= 0:
            await ctx.respond("Slowmode delay must be greater than 0")
            return

        channel = ctx.channel

        active_slowmode = (
            database.cursor()
            .execute(
                "SELECT id FROM slowmode_info WHERE channel_id=(?) AND id=(?)",
                (channel.id, target.id),
            )
            .fetchone()
        )

        if active_slowmode:
            database.cursor().execute(
                "UPDATE slowmode_info SET delay=(?) WHERE channel_id=(?) AND id=(?)",
                (slowmode_delay, channel.id, target.id),
            )
        else:
            database.cursor().execute(
                "INSERT INTO slowmode_info (channel_id,id,delay,is_role) VALUES (?,?,?,?)",
                (channel.id, target.id, slowmode_delay, int(is_role)),
            )
        database.commit()
        await ctx.respond(content=f"Slowmode on for <@{target.id}>", ephemeral=True)

    @slowmode_commands.command()
    @commands.has_permissions(manage_messages=True)
    async def disable(self, ctx, target: typing.Union[discord.User, discord.Role]):
        is_role = isinstance(target, discord.Role)
        channel = ctx.channel

        target_list = get_active_slowmode(channel, target) if is_role else [target]

        bot_status = await ctx.respond(
            f"Disable slowmode for {len(target_list)} users..."
        )

        user_nb = 0
        prev = 0
        last_refresh = time.time()
        database.cursor().execute(
            "DELETE FROM slowmode_info WHERE channel_id=(?) AND id=(?)",
            (channel.id, target.id),
        )
        for user in target_list:
            await channel.set_permissions(user, overwrite=None)

            user_nb += 1
            prev, last_refresh = await self.loading_bar(
                bot_status, user_nb / len(target_list), prev, last_refresh
            )
        database.commit()
        await bot_status.edit_original_response(
            content=f"Slowmode off for <@{target.id}>", ephemeral=True
        )

    @slowmode_commands.command()
    @commands.has_permissions(manage_messages=True)
    async def list(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel 
        element = (
            database.cursor()
            .execute(
                "SELECT delay,user_id,channel_id FROM slowmode_info WHERE channel_id = (?) ORDER BY delay DESC",
                (channel.id,),
            )
            .fetchall()
        )
        my_embed = create_embed("Slowmode list")
        if element:
            channel_name = self.bot.get_channel(element[0][2])
            if channel_name is None:
                my_embed.description = "Deleted channel"
                await ctx.respond(embed=my_embed)
                return

            my_embed.description = f"*List of active slowmode in #{channel_name.name}*"
            all_pages = []
            for slowmode_info in element:
                user = await self.bot.get_or_fetch_user(slowmode_info[1])
                if user is None:
                    continue

                all_pages.append((f"Delay: {slowmode_info[0]}", escape_markdown(user.name)))

            my_navigation = PageNavigation(
                all_pages, my_embed, ctx.author
            )
            await ctx.respond(embed=my_embed, view=my_navigation)
        else:
            my_embed.description = "**No slowmode users in this channel**"
            await ctx.respond(embed=my_embed)


def setup(bot):
    bot.add_cog(ManageSlowmode(bot))
