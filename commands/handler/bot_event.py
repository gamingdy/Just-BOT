import traceback

import discord
from discord.ext import commands

from Utils.funct import user_slowmode, create_embed, get_traceback_info
from config import database


class EventHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return
        author = ctx.author
        author_roles = [role.id for role in author.roles]

        channel = ctx.channel
        ids = [author.id] + author_roles
        sql_request = (
            "SELECT delay FROM slowmode_info WHERE channel_id=(?) AND id IN {}".format(
                tuple(ids)
            )
        )
        if db_row:
            await user_slowmode(channel, author, db_row[0][2])


class VoiceHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_channel(self, auto_chan, before):
        old_chan = self.bot.get_channel(before.channel.id)
        meb = old_chan.voice_states
        if len(meb) == 0 and old_chan.id != auto_chan:
            tables = ["active_voice", "blocklist", "whitelist"]
            for table in tables:
                database.cursor().execute(
                    f"DELETE FROM {table} WHERE channel_id=(?)", (old_chan.id,)
                )
            database.commit()
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

                    voice_cursor.execute(
                        "INSERT INTO active_voice (author_id, channel_id) VALUES(?,?)",
                        (
                            member.id,
                            created_channel.id,
                        ),
                    )
                    database.commit()
            else:
                await self.check_channel(auto_chan, before)


def setup(bot):
    bot.add_cog(EventHandler(bot))
    bot.add_cog(VoiceHandler(bot))
