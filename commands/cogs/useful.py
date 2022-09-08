import discord
from discord.ext import commands
from discord.commands import slash_command

import Utils.funct as fonction


class BotTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

        join_date = int(user.joined_at.timestamp())
        date_joined = f"<t:{join_date}:F>"
        since_joined = f"<t:{join_date}:R>"

        create_date = int(user.created_at.timestamp())
        date_created = f"<t:{create_date}:F>"
        since_created = f"<t:{create_date}:R>"

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
            f"**Joined** | {date_joined} ({since_joined})",
            f"**Created** | {date_created} ({since_created})",
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
