import discord
from discord.ext import commands
from discord.commands import slash_command, option
from datetime import datetime
import json

import Utils.funct as fonction


class BotTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("data/help.json", encoding="utf8") as help_file:
            self.commands_help = json.load(help_file)

    async def get_command_group(self, ctx):
        return [
            group
            for group in self.commands_help
            if group.lower().startswith(ctx.value.lower())
        ]

    @slash_command(description="Have the bot ping")
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

    @slash_command(description="Displays the bot's help")
    @option("command_group", autocomplete=get_command_group)
    async def help(self, ctx, command_group=None):
        help_embed = fonction.create_embed("Bot commands")
        if command_group:
            help_embed.description = "oui"
        else:
            help_embed.description = "non"
        await ctx.respond(embed=help_embed)


def setup(bot):
    bot.add_cog(BotTools(bot))
