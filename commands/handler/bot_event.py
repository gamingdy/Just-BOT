from discord.ext import commands


from config import database
from Utils.funct import user_slowmode


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


def setup(bot):
    bot.add_cog(EventHandler(bot))
