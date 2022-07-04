from discord.ext import commands
import traceback
import sys

from config import database
from Utils.funct import user_slowmode, create_embed


class EventHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        author = ctx.author
        channel = ctx.channel

        db_row = (
            database.cursor()
            .execute(
                "SELECT * FROM slowmode_info WHERE channel_id=(?) AND user_id=(?)",
                (channel.id, author.id),
            )
            .fetchall()
        )
        if db_row:
            await user_slowmode(channel, author, db_row[0][2])

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):

        embed_message = create_embed("AN ERROR OCCURRED 😔")
        if isinstance(error.original, commands.MissingPermissions):
            error = error.original
            missing_permissions_list = [
                f"**{perms.capitalize().replace('_',' ')}**"
                for perms in error.missing_permissions
            ]
            embed_message.description = (
                f"Missing permissions : {','.join(missing_permissions_list)}"
            )

            await ctx.respond(
                embed=embed_message,
                ephemeral=True,
            )
        else:
            embed_message.description = "Oh, it seems that an unknown error occurred, no worries, a very explicit message has been sent to the dev to solve the problem👌."
            await ctx.respond(embed=embed_message, ephemeral=True)

            failed_command = ctx.command
            bot_info = await self.bot.application_info()
            owner = bot_info.owner
            error_traceback = traceback.format_exception(
                type(error), error, error.__traceback__
            )
            end_of_traceback = error_traceback.index(
                "\nThe above exception was the direct cause of the following exception:\n\n"
            )
            error_traceback = error_traceback[:end_of_traceback]
            file_name = error_traceback[-2].split(",")[0].split("/")[-1][:-1]
            line = error_traceback[-2].split(",")[1]
            bad_code = "".join(error_traceback[-2].split(",")[2:])

            embed_message.description = "Hi, new problem 🥳.\nAn unknown error occurred, so good luck finding the solution 🙃. Here is the problematic command and the error."

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
            await owner.send(embed=embed_message)


def setup(bot):
    bot.add_cog(EventHandler(bot))
