import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
import typing


class ManageSlowmode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    slowmode_commands = SlashCommandGroup("slowmode", "Manage channel slowmode")

    async def get_role_user(self, role_object):
        return user.id for user in role_object.members

    @slowmode_commands.command()
    async def enable_slowmode(
        self, ctx, target: typing.Union[discord.User, discord.Role], slowmode_delay: int
    ):
        print(type(target))
        if isinstance(target, discord.role.Role):
            target_ids = await self.get_role_user(target)
            
        else:
            target_ids = [target.id]

        await ctx.respond(f"target --> {target} --> {target.id}")


def setup(bot):
    bot.add_cog(ManageSlowmode(bot))
