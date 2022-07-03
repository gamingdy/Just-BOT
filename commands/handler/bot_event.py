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
            await ctx.respond(f"Hmmm {error} occurred", ephemeral=True)


def setup(bot):
    bot.add_cog(EventHandler(bot))
