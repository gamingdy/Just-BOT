import time
import typing

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from Utils.create_page import generate_page, PageNavigation
from Utils.funct import create_embed
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
        if isinstance(target, discord.Role):
            target_list = target.members
        else:
            target_list = [target]
        channel = ctx.channel

        bot_status = await ctx.respond(
            f"Activation of the slowmode for {len(target_list)} users..."
        )
        channel_slowmode = [
            user_id[0]
            for user_id in database.cursor()
            .execute("SELECT user_id FROM slowmode_info")
            .fetchall()
        ]
        for user in target_list:

            if user.id != self.bot.user.id:
                user_info = "{}#{}".format(user.name, user.discriminator)
                if user.id in channel_slowmode:
                    database.cursor().execute(
                        "UPDATE slowmode_info SET delay=(?) WHERE channel_id=(?) AND user_id=(?)",
                        (slowmode_delay, channel.id, user.id),
                    )
                else:
                    database.cursor().execute(
                        "INSERT INTO slowmode_info (channel_id,user_id,delay, channel_name,user_name_discriminator) "
                        "VALUES (?,?,?,?,?)",
                        (
                            channel.id,
                            user.id,
                            slowmode_delay,
                            channel.name,
                            user_info,
                        ),
                    )
            else:
                target_list.remove(self.bot.user)
                await ctx.send("You can't slowmode bot")
        database.commit()
        await bot_status.edit_original_response(
            content=f"Slowmode on for {len(target_list)} users"
        )

    @slowmode_commands.command()
    @commands.has_permissions(manage_messages=True)
    async def disable(self, ctx, target: typing.Union[discord.User, discord.Role]):
        target_list = target.members if isinstance(target, discord.Role) else [target]

        channel = ctx.channel
        bot_status = await ctx.respond(
            f"Disable slowmode for {len(target_list)} users..."
        )

        user_nb = 0
        prev = 0
        last_refresh = time.time()
        for user in target_list:
            await channel.set_permissions(user, overwrite=None)

            database.cursor().execute(
                "DELETE FROM slowmode_info WHERE channel_id=(?) AND user_id=(?)",
                (channel.id, user.id),
            )
            user_nb += 1
            prev, last_refresh = await self.loading_bar(
                bot_status, user_nb / len(target_list), prev, last_refresh
            )
        database.commit()
        await bot_status.edit_original_response(
            content=f"Slowmode off for {len(target_list)} users"
        )

    @slowmode_commands.command()
    @commands.has_permissions(manage_messages=True)
    async def list(self, ctx):
        channel = ctx.channel
        element = (
            database.cursor()
            .execute(
                "SELECT delay,user_name_discriminator,channel_name FROM slowmode_info WHERE channel_id = (?) ORDER BY "
                "delay DESC",
                (channel.id,),
            )
            .fetchall()
        )
        my_embed = create_embed("Slowmode list")
        if element:
            my_embed.description = f"*List of active slowmode in #{element[0][2]}*"
            all_page = [element[i : i + 5] for i in range(0, len(element), 5)]

            all_page = list(
                map(
                    lambda l: list(map(lambda i: (f"Delay: {i[0]}", i[1]), l)),
                    all_page,
                )
            )

            generate_page(my_embed, *iter(all_page[0]))
            my_embed.set_footer(text=f"Page 1/{len(all_page)}")

            my_navigation = PageNavigation(len(all_page), all_page, my_embed)
            await ctx.respond(embed=my_embed, view=my_navigation)
        else:
            my_embed.description = "**No slowmode users in this channel**"
            await ctx.respond(embed=my_embed)


def setup(bot):
    bot.add_cog(ManageSlowmode(bot))
