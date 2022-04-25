import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
import typing
import sqlite3


class ManageSlowmode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect("data/bot_db.db")

    slowmode_commands = SlashCommandGroup("slowmode", "Manage channel slowmode")

    async def get_role_user(self, role_object):
        return (
            [user.id for user in role_object.members],
            [user for user in role_object.members],
        )

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
            self.db.cursor().execute(
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

        self.db.commit()
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

            self.db.cursor().execute(
                "DELETE FROM slowmode_info WHERE channel_id=(?) AND user_id=(?)",
                (channel.id, target_list[0][user_nb]),
            )
            user_nb += 1
            await bot_status.edit_original_message(
                content=f"Permissions updated for {user_nb}/{len(target_list[1])}"
            )
        self.db.commit()
        await bot_status.edit_original_message(
            content=f"Slowmode off for {len(target_list[1])} users"
        )


def setup(bot):
    bot.add_cog(ManageSlowmode(bot))
