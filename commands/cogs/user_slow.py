import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
import typing

from Utils.funct import create_embed
from config import database


class ManageSlowmode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    slowmode_commands = SlashCommandGroup("slowmode", "Manage channel slowmode")

    async def get_role_user(self, role_object):
        return (
            [user.id for user in role_object.members],
            [user for user in role_object.members],
        )

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

    @slowmode_commands.command()
    async def enable(
        self, ctx, target: typing.Union[discord.User, discord.Role], slowmode_delay: int
    ):
        if isinstance(target, discord.role.Role):
            target_list = await self.get_role_user(target)

        else:
            target_list = ([target.id], [target])
        channel = ctx.channel

        bot_status = await ctx.respond(
            f"Activation of the slowmode for {len(target_list[1])} users..."
        )
        user_nb = 0
        for user in target_list[1]:
            user_info = "{}#{}".format(
                target_list[1][user_nb].name, target_list[1][user_nb].discriminator
            )
            database.cursor().execute(
                "INSERT INTO slowmode_info (channel_id,user_id,delay, channel_name,user_name_discriminator) VALUES (?,?,?,?,?)",
                (
                    channel.id,
                    target_list[0][user_nb],
                    slowmode_delay,
                    channel.name,
                    user_info,
                ),
            )
            user_nb += 1
            await bot_status.edit_original_message(
                content=f"Permissions updated for {user_nb}/{len(target_list[1])}"
            )

        database.commit()
        await bot_status.edit_original_message(
            content=f"Slowmode on for {len(target_list[1])} users"
        )

    @slowmode_commands.command()
    async def disable(self, ctx, target: typing.Union[discord.User, discord.Role]):
        if isinstance(target, discord.role.Role):
            target_list = await self.get_role_user(target)

        else:
            target_list = ([target.id], [target])
        channel = ctx.channel
        bot_status = await ctx.respond(
            f"Disable slowmode for {len(target_list[1])} users..."
        )

        user_nb = 0
        for user in target_list[1]:
            await channel.set_permissions(user, overwrite=None)

            database.cursor().execute(
                "DELETE FROM slowmode_info WHERE channel_id=(?) AND user_id=(?)",
                (channel.id, target_list[0][user_nb]),
            )
            user_nb += 1
            await bot_status.edit_original_message(
                content=f"Permissions updated for {user_nb}/{len(target_list[1])}"
            )
        database.commit()
        await bot_status.edit_original_message(
            content=f"Slowmode off for {len(target_list[1])} users"
        )

    @slowmode_commands.command()
    async def list(self, ctx):
        channel = ctx.channel
        list_user = (
            database.cursor()
            .execute(
                "SELECT * FROM slowmode_info WHERE channel_id=(?) ORDER BY delay DESC",
                (channel.id,),
            )
            .fetchall()
        )
        my_color = discord.Colour.from_rgb(8, 155, 239)
        emb_message = create_embed("Slowmode list", color=my_color)
        emb_message.url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        if list_user:
            emb_message.description = f"*List of active slowmode in #{list_user[0][4]}*"
            field_value = "Delay `{}s`"
            if len(list_user) > 5:
                bin_message = f"{emb_message.description}\n"
                user_info = "\n{}: {} | {}"
                bin_message = await self.add_user_in_field(
                    emb_message, list_user, field_value, bin_message, user_info
                )

                emb_message.add_field(
                    name="_ _",
                    value="[**More ...**](http://127.0.0.1)",
                )
            else:
                await self.add_user_in_field(emb_message, list_user, field_value)
        else:
            emb_message.description = "**No slowmode users in this channel**"

        await ctx.respond(embed=emb_message)


def setup(bot):
    bot.add_cog(ManageSlowmode(bot))
