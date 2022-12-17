import traceback

from discord.ext import commands

from Utils.funct import create_embed, get_traceback_info
from Utils.custom_error import (
    NotGuildOwner,
    NotConnectedInVoiceChannel,
    NotVoiceChannelAdmin,
)


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
        embed_message = create_embed("AN ERROR OCCURRED 😔")
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

        """
		else:

			embed_message.description = "Oh, it seems that an unknown error occurred, no worries, a very explicit message has been sent to the dev to solve the problem👌."
			await ctx.respond(embed=embed_message, ephemeral=True)

			failed_command = ctx.command
			bot_info = await self.bot.application_info()
			traceback_error = traceback.format_exception(
				type(error), error, error.__traceback__
			)
			file_name, line, bad_code = get_traceback_info(traceback_error)

			embed_message.description = "Hi, new problem 🥳.\nAn unknown error occurred, so good luck finding the  solution 🙃. Here is the problematic command and the error."

			embed_message.add_field(
				name="🛠 Command", value=failed_command, inline=False
			)
			embed_message.add_field(name="👾 Error", value=error, inline=False)
			embed_message.add_field(
				name="🗒️ Traceback",
				value="**File** : {} {}\n**Code** : {}".format(
					file_name, line, bad_code
				),
			)
			print(error)
			# await bot_info.owner.send(embed=embed_message)
		"""


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
