from datetime import datetime, timedelta
import time
import json

from discord.commands import slash_command, option
from discord.ext import commands
from yaml import safe_load

import Utils.funct as fonction
from Utils.create_page import PageNavigation


class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("data/help.yml", encoding="utf8") as help_file:
            self.commands_help = safe_load(help_file)

    async def get_command_group(self, ctx):
        return [
            group.capitalize()
            for group in self.commands_help
            if group.lower().startswith(ctx.value.lower())
        ]

    @slash_command(description="Display bot's ping")
    async def ping(self, ctx):
        ping_start = datetime.now()
        latency = self.bot.latency * 1000
        await ctx.send("Pong", delete_after=0.1)

        latency_ms = f"**{str(round(latency, 0))[:-2]}** ms"
        ping_end = (datetime.now() - ping_start).microseconds / 1000
        bot_ping = f"**{round(ping_end)}** ms"

        ping_emb = fonction.create_embed(title="Bot latency")
        ping_emb.add_field(name=":satellite: API", value=latency_ms, inline=True)
        ping_emb.add_field(name=":robot: BOT", value=bot_ping)
        await ctx.respond(embed=ping_emb)

    @slash_command(description="Displays bot's help")
    @option("command_group", autocomplete=get_command_group)
    async def help(self, ctx, command_group=None):
        help_embed = fonction.create_embed("Bot commands")
        if command_group:
            if command_group in self.commands_help:
                category = self.commands_help[command_group]
                category_commands = category["commands"]
                all_pages = []
                for command in category_commands:
                    warn = ""
                    if "warn" in category_commands[command]:
                        warn = f"**:warning: {category_commands[command]['warn']} :warning:**"

                    arguments = "__This command does not take any argument__"
                    if "args" in category_commands[command]:
                        arguments = "__Arguments__:\n"
                        all_args = []
                        for args in category_commands[command]["args"]:
                            all_args.append(
                                f"`{args}` ({category_commands[command]['args'][args]})"
                            )
                        arguments += ", ".join(all_args)

                    description = category_commands[command]["description"]
                    page = (f"{warn}\n{description}\n\n{arguments}", command)
                    all_pages.append(page)


                help_embed.title = command_group.capitalize()
                help_embed.description = category["description"]

                my_navigation = PageNavigation(
                    all_pages, help_embed, ctx.author
                )
                await ctx.respond(embed=help_embed, view=my_navigation)
                return

            else:
                help_embed.description = (
                    f":warning:**The category `{command_group.capitalize()}` is not found**\n\n "
                    f"You can do `/help` to see all available categories "
                )
        else:
            help_embed.description = (
                "You can do `/help <category>` to get help about a category"
            )

            for group in self.commands_help:
                help_embed.add_field(
                    name=group,
                    value=self.commands_help[group]["description"],
                    inline=False,
                )

        await ctx.respond(embed=help_embed)

    @slash_command(description="Displays bot's info")
    async def info(self, ctx):
        message_embed = fonction.create_embed(title="Bot's info")

        message_embed.add_field(name="Total Guilds", value=len(self.bot.guilds))
        message_embed.add_field(name="Total Members", value=len(self.bot.users))

        bot_info = await self.bot.application_info()
        bot_owner = bot_info.owner
        message_embed.add_field(
            name="Bot owner",
            value="{}#{}".format(bot_owner.name, bot_owner.discriminator),
            inline=False,
        )
        with open("data/info.json") as info:
            data = json.load(info)
            boot_time = timedelta(seconds=data["boot"])

        actual_time = timedelta(seconds=time.time())
        uptime = (str(actual_time - boot_time)).split(".")[0]

        message_embed.add_field(name="Uptime", value=uptime)

        await ctx.respond(embed=message_embed)


def setup(bot):
    bot.add_cog(BotInfo(bot))
