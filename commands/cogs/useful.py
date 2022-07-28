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

    @slash_command(description="Display bot's ping")
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

    @slash_command(description="Displays bot's help")
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

        await ctx.respond(embed=message_embed)

    @slash_command(description="Display information about a user or the command author")
    async def ui(self, ctx, member: discord.Member = None):
        user_id = member.id if member else ctx.author.id
        user = ctx.guild.get_member(user_id)

        fetch_user = await self.bot.fetch_user(user_id)
        user_color = fetch_user.accent_color

        username = "{}#{}".format(user.name, user.discriminator)
        nickname = user.display_name
        status_emoji = {"online": "🟢", "offline": "🔴", "dnd": "⛔", "idle": "🌙"}

        status = user.status.value
        if status in status_emoji:
            status = f"{status_emoji[status]} {status}"
        avatar_url = user.display_avatar.url
        mutual_guild = len(user.mutual_guilds)

        join_date = user.joined_at
        date_joined = join_date.date().strftime("%Y/%m/%d")
        time_joined = join_date.time().strftime("%H:%M:%S")

        create_date = user.created_at
        date_created = create_date.date().strftime("%Y/%m/%d")
        time_created = create_date.time().strftime("%H:%M:%S")

        activity = user.activity
        if activity:
            activity_name = activity.name
            if isinstance(activity, discord.activity.CustomActivity):
                activity = activity_name
            elif isinstance(activity, discord.activity.Game):
                activity = f"Playing {activity_name}"
            elif isinstance(activity, discord.activity.Streaming):
                activity = f"Streaming {activity_name} on {activity.platform}, [stream url]({activity.url})"
            elif isinstance(activity, discord.activity.Spotify):
                activity = f"Listening {activity.title}({activity.duration}), [track url]({activity.track_url})"
        else:
            activity = "Nothing"

        separator = "-" * 20
        embed_description = (
            f"**Username** | {username}",
            f"**Nickname** | {nickname}",
            f"**Status** | {status}",
            f"**Activity** | {activity}",
            separator,
            f"**Joined** | {date_joined} at {time_joined}",
            f"**Created** | {date_created} at {time_created}",
            separator,
            f"**Common Guild** | {mutual_guild}",
        )
        embed_description = "\n".join(embed_description)
        ui_embed = fonction.create_embed(
            title=nickname,
            thumbnail=avatar_url,
            description=embed_description,
            color=user_color,
        )

        await ctx.respond(embed=ui_embed)


def setup(bot):
    bot.add_cog(BotTools(bot))