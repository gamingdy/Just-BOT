import asyncio
import os
import sqlite3
import time
from random import randint

import discord

from config import database


def create_embed(title, description=None, color=None, image=None, thumbnail=None):
    embed = discord.Embed()
    embed.title = title
    embed.description = description
    embed.colour = (
        discord.Colour.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255))
        if not color
        else color
    )
    if image:
        embed.set_image(url=image)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    return embed


def verify_db():
    sql_request = {
        "slowmode_info": [
            "SELECT channel_id,user_id,delay,last_slowmode,channel_name,user_name_discriminator FROM slowmode_info",
            "DROP TABLE slowmode_info",
            """CREATE TABLE "slowmode_info" (
                "channel_id"    INTEGER,
                "user_id"   INTEGER,
                "delay" INTEGER,
                "last_slowmode" INTEGER,
                "channel_name"  TEXT,
                "user_name_discriminator"   TEXT
            );
            """,
        ]
    }
    curs = database.cursor()
    for table in sql_request:
        try:
            curs.execute(sql_request[table][0])
        except sqlite3.OperationalError:
            print("Database error")
            print("Try to create table in database")
            try:
                curs.execute(sql_request[table][2])
            except sqlite3.OperationalError:
                print("Table already exists, but an error occurred")
                print("Try to recreate table")

                curs.execute(sql_request[table][1])
                curs.execute(sql_request[table][2])
    database.commit()


def load_cog(path, bot):
    for content in os.listdir(path):
        if os.path.isdir(f"{path}/{content}"):
            load_cog(f"{path}/{content}", bot)
        else:
            if content.endswith(".py"):
                bot.load_extension(f"{path}/{content}"[:-3].replace("/", "."))


async def user_slowmode(channel, user, delay):
    await channel.set_permissions(user, send_messages=False)
    database.cursor().execute(
        "UPDATE slowmode_info SET last_slowmode=(?) WHERE channel_id=(?) AND user_id=(?)",
        (round(time.time()), channel.id, user.id),
    )
    database.commit()
    await asyncio.sleep(delay)
    await channel.set_permissions(user, send_messages=None)


async def verify_user_slowmode(bot):
    my_database = database.cursor().execute("SELECT * FROM slowmode_info").fetchall()
    if my_database:
        for row in my_database:
            if row[3]:
                channel = bot.get_channel(row[0])
                user = bot.get_user(row[1])
                slowmode_delay = row[2]
                last_slowmode = row[3]
                actual_time = round(time.time())
                if actual_time - slowmode_delay > last_slowmode:
                    await user_slowmode(channel, user, 0)
                else:
                    await user_slowmode(channel, user, actual_time - slowmode_delay)


def get_traceback_info(traceback_error):
    end_of_traceback = traceback_error.index(
        "\nThe above exception was the direct cause of the following exception:\n\n"
    )
    traceback_error = traceback_error[:end_of_traceback]
    file_name = traceback_error[-2].split(",")[0].replace("\\", "/").split("/")[-1][:-1]
    line = traceback_error[-2].split(",")[1]
    bad_code = "".join(traceback_error[-2].split(",")[2:])

    return file_name, line, bad_code
