import traceback

import discord
from discord.ext import commands

from Utils.funct import create_embed, get_traceback_info
from Utils.custom_error import (
    NotGuildOwner,
    NotConnectedInVoiceChannel,
    NotVoiceChannelAdmin,
)
from config import debug_channel


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        error_list = (
            commands.NotOwner,
            NotGuildOwner,
            commands.CommandOnCooldown,
            NotConnectedInVoiceChannel,
            NotVoiceChannelAdmin,
        )
        embed_message = create_embed("AN ERROR OCCURRED 😔", color=discord.Colour.red())
        if isinstance(error, error_list):
            embed_message.description = f"**{str(error)}**"
            await ctx.respond(embed=embed_message, ephemeral=True)

        elif isinstance(error.original, commands.MissingPermissions):
            error = error.original
            missing_permissions_list = [
                f"**{perms.capitalize().replace('_',' ')}**"
                for perms in error.missing_permissions
            ]
            embed_message.description = (
                f"Missing permissions : {','.join(missing_permissions_list)}"
            )

            await ctx.respond(embed=embed_message, ephemeral=True)

        else:
            embed_message.description = "Oh, it seems that an unknown error occurred, no worries, a very explicit message has been sent to the dev to solve the problem👌."
            await ctx.respond(embed=embed_message, ephemeral=True)

            failed_command = ctx.command
            bot_info = await self.bot.application_info()
            traceback_error = traceback.format_exception(
                type(error), error, error.__traceback__
            )

            file_name, line, command, code = get_traceback_info(traceback_error)

            embed_message.description = "Hi, new problem 🥳.\nAn unknown error occurred, so good luck finding the  solution 🙃. Here is the problematic command and the error."

            embed_message.add_field(
                name="🛠 Command", value=failed_command, inline=False
            )
            embed_message.add_field(name="👾 Error", value=error, inline=False)
            embed_message.add_field(
                name="🗒️ Traceback",
                value=f"**File** : `{file_name}` {line}\n**Code** : {command}\n```py\n{code}```",
            )
            debug_channel_ = self.bot.get_channel(debug_channel)
            if debug_channel_ and isinstance(debug_channel_, discord.TextChannel):
                await debug_channel_.send(embed=embed_message)
                return

            message = "It seems that the debug channel id has been misconfigured, but here's the error message anyway"
            await bot_info.owner.send(content=message, embed=embed_message)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
