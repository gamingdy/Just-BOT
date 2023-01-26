from config import database


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

    is_blocked = cursor.execute(
        f"SELECT * FROM {target} WHERE channel_id=(?) AND user_id=(?)",
        (
            channel.id,
            user.id,
        ),
    ).fetchone()

    if not is_blocked:
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
