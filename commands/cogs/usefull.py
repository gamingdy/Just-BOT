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
            group.capitalize()
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
            if command_group in self.commands_help:
                category = self.commands_help[command_group]
                category_command = category[1]

                help_embed.title = "{}'s help".format(command_group.capitalize())
                help_embed.description = category[0]

                for command in category_command:
                    help_embed.add_field(
                        name=command, value=category_command[command], inline=False
                    )
            else:
                help_embed.description = f":warning:**The category `{command_group.capitalize()}` is not found**\n\n You can do `/help` to see all available categories"
        else:
            help_embed.description = (
                "You can do `/help <category>` to get help about a category"
            )
            for group in self.commands_help:
                help_embed.add_field(
                    name=group, value=self.commands_help[group][0], inline=False
                )

        await ctx.respond(embed=help_embed)

    @slash_command(description="Displays bot's info")
    async def info(self, ctx):
        total_member = []
        for guilds in self.bot.guilds:
            total_member += [
                members.id
                for members in guilds.members
                if not members.id in total_member
            ]

        total_member = len(total_member)
        message_embed = fonction.create_embed(title="Bot's info")

        message_embed.add_field(name="Total Guilds", value=len(self.bot.guilds))
        message_embed.add_field(name="Total Members", value=total_member)

        bot_info = await self.bot.application_info()
        bot_owner = bot_info.owner
        message_embed.add_field(
            name="Bot owner",
            value="{}#{}".format(bot_owner.name, bot_owner.discriminator),
            inline=False,
        )

        await ctx.respond(embed=message_embed)

    @slash_command(description="Display user information")
    async def ui(self, ctx, member: discord.Member = None):
        user = member.id if member else ctx.author.id
        user = ctx.guild.get_member(user)

        user_color = user.accent_color
        username = "{}#{}".format(user.name, user.discriminator)
        nickname = user.display_name
        status = user.status
        avatar_url = user.display_avatar.url
        mutual_guild = len(user.mutual_guilds)

        join_date = user.joined_at
        date_joined = join_date.date().strftime("%Y/%m/%d")
        time_joined = join_date.time().strftime("%H:%M:%S")

        create_date = user.created_at
        date_created = create_date.date().strftime("%Y/%m/%d")
        time_created = create_date.time().strftime("%H:%M:%S")

        # activity = user.activity.name
        separator = "-" * 20
        embed_description = (
            f"**Username** | {username}",
            f"**Nickname** | {nickname}",
            f"**Status** | {status}",
            "**Activity** | **UNDER DEV**",
            separator,
            f"**Joined** | {date_joined} at {time_joined}",
            f"**Created** | {date_created} at {time_created}",
            separator,
            f"**Common Guild** | {mutual_guild}",
        )
        embed_description = "\n".join(embed_description)
        ui_embed = fonction.create_embed(
            title=nickname, thumbnail=avatar_url, description=embed_description
        )

        await ctx.respond(embed=ui_embed)


def setup(bot):
    bot.add_cog(BotTools(bot))
