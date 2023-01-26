from config import database
from Utils.custom_error import (
    NotConnectedInVoiceChannel,
    NotVoiceChannelAdmin,
)


async def connected_admin(ctx):
    voice_state = ctx.author.voice
    if voice_state:
        voice_cursor = database.cursor()
        is_admin = voice_cursor.execute(
            "SELECT channel_id FROM active_voice WHERE author_id=(?)",
            (ctx.author.id,),
        ).fetchall()
        if len(is_admin) > 0:
            for channel in is_admin:
                if channel[0] == voice_state.channel.id:
                    return True
        else:
            raise NotVoiceChannelAdmin("You are not channel admin")

    raise NotConnectedInVoiceChannel("You are not connected in voice channel")


def add_user(channel, user, target):
    cursor = database.cursor()
    opposite = "whitelist" if target == "blocklist" else "blocklist"

    user_exist = cursor.execute(
        f"SELECT * FROM {target} WHERE channel_id=(?) AND user_id=(?)",
        (
            channel.id,
            user.id,
        ),
    ).fetchone()
    if user_exist:
        return {"result": False, "msg": ""}
    else:
        is_listed = cursor.execute(
            f"SELECT * FROM {opposite} WHERE channel_id=(?) AND user_id=(?)",
            (
                channel.id,
                user.id,
            ),
        ).fetchone()
        warn = ""
        if is_listed:
            cursor.execute(
                f"DELETE FROM {opposite} WHERE channel_id=(?) AND user_id=(?)",
                (
                    channel.id,
                    user.id,
                ),
            )
            warn = f":warning: **The user was {opposite}ed and has been removed**"

        cursor.execute(
            f"INSERT INTO {target} (channel_id, user_id) VALUES (?,?) ",
            (
                channel.id,
                user.id,
            ),
        )
        database.commit()
        message = (
            f"{warn}\n\n{user.mention} is now {target}ed in channel {channel.mention}"
        )

        return {"result": True, "msg": message}


async def remove_user(channel, user, target):
    cursor = database.cursor()

    is_listed = cursor.execute(
        f"SELECT * FROM {target} WHERE channel_id=(?) AND user_id=(?)",
        (
            channel.id,
            user.id,
        ),
    ).fetchone()

    if not is_listed:
        message = f"User is not {target}ed"
    else:

        cursor.execute(
            f"DELETE FROM {target} WHERE channel_id=(?) and user_id=(?)",
            (
                channel.id,
                user.id,
            ),
        )

        database.commit()

        message = f"User has been removed from {target}"
        await channel.set_permissions(user, overwrite=None)

    return message


async def update_channel(channel, everyone, status):
    cursor = database.cursor()
    cursor.execute(
        "UPDATE active_voice SET open=(?) WHERE channel_id=(?)",
        (
            status,
            channel.id,
        ),
    )
    database.commit()
    await channel.set_permissions(everyone, connect=None if status else False)


def channel_list(channel, guild, target):
    cursor = database.cursor()
    listed = cursor.execute(
        f"SELECT user_id FROM {target} WHERE channel_id=(?)", (channel.id,)
    ).fetchall()

    if listed:
        message = f"Active {target} in {channel.mention}"
        user_list = []
        for row in listed:
            user = guild.get_member(row[0]).mention
            user_list.append(user)

        message += f"\n\n{','.join(user_list)}"
    else:
        message = f"No {target}ed user in this channel"

    return message
