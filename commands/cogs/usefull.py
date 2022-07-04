import discord
from discord.ext import commands
from discord.commands import slash_command
from datetime import datetime

import Utils.funct as fonction


class BotTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Connaître le ping du bot")
    async def ping(self, ctx):
        ping_start = datetime.now()
        latency = self.bot.latency * 1000
        await ctx.send("Pong", delete_after=0.1)

        latency_ms = f"**{str(round(latency,0))[:-2]}** ms"
        ping_end = (datetime.now() - ping_start).microseconds / 1000
        bot_ping = f"**{round(ping_end)}** ms"

        ping_emb = fonction.create_embed(title="Bot latency")
        ping_emb.add_field(name=":satellite: API", value=latency_ms, inline=True)
        ping_emb.add_field(name=":robot: BOT", value=bot_ping)
        await ctx.respond(embed=ping_emb)


def setup(bot):
    bot.add_cog(BotTools(bot))
