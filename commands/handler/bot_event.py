import discord
from discord.ext import commands

from Utils.funct import user_slowmode
from config import database


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

    """
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
            
            embed_message.description = "Oh, it seems that an unknown error occurred, no worries, a very explicit 
            message has been sent to the dev to solve the problem👌." await ctx.respond(embed=embed_message, 
            ephemeral=True) 

            failed_command = ctx.command
            bot_info = await self.bot.application_info()
            owner = bot_info.owner
            traceback_error = traceback.format_exception(
                type(error), error, error.__traceback__
            )
            file_name, line, bad_code = get_traceback_info(traceback_error)

            embed_message.description = "Hi, new problem 🥳.\nAn unknown error occurred, so good luck finding the 
            solution 🙃. Here is the problematic command and the error." 

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
            #await owner.send(embed=embed_message)
    """


class VoiceHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_channel(self, auto_chan, before):
        old_chan = self.bot.get_channel(before.channel.id)
        meb = old_chan.voice_states
        if len(meb) == 0 and old_chan.id != auto_chan:
            await old_chan.delete()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        voice_cursor = database.cursor()
        guild = before.channel.guild if before.channel else after.channel.guild
        auto_voice = voice_cursor.execute(
            "SELECT channel_id FROM auto_voice WHERE guild_id=(?)",
            (guild.id,),
        ).fetchall()

        if auto_voice:
            auto_chan = auto_voice[0][0]
            category_id = self.bot.get_channel(auto_chan).category_id
            category = self.bot.get_channel(category_id)

            if after.channel:
                if before.channel:
                    await self.check_channel(auto_chan, before)

                connected_channel = after.channel
                if connected_channel.id == auto_chan:
                    channel_name = f"{member.name}' channel"
                    new_permissions = {
                        member: discord.PermissionOverwrite(read_messages=True)
                    }

                    created_channel = await guild.create_voice_channel(
                        name=channel_name, overwrites=new_permissions, category=category
                    )
                    await member.move_to(created_channel)

            else:
                await self.check_channel(auto_chan, before)


def setup(bot):
    bot.add_cog(EventHandler(bot))
    bot.add_cog(VoiceHandler(bot))
