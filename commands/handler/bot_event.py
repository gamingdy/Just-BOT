from discord.ext import commands


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
        if not isinstance(error.original, commands.MissingPermissions):
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
            embed_message.description = "Hi, new problem 🥳.\nAn unknown error occurred, so good luck finding the solution 🙃. Here is the problematic command and the error."

            embed_message.add_field(
                name="🛠 Command", value=failed_command, inline=False
            )
            embed_message.add_field(name="👾 Error", value=error)
            await owner.send(embed=embed_message)


def setup(bot):
    bot.add_cog(EventHandler(bot))
