import sqlite3
import os
import discord
from random import randint

from config import database


def create_embed(title, description=None, color=None, img=None):
    embed = discord.Embed()
    embed.title = title
    embed.description = description
    embed.colour = (
        discord.Colour.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255))
        if not color
        else color
    )
    if img:
        embed.set_image(url=img)
    return embed


def verify_db():
    sql_request = """
    CREATE TABLE "slowmode_info" (
        "channel_id"    INTEGER,
        "user_id"   INTEGER,
        "delay" INTEGER,
        "last_slowmode" INTEGER,
        "channel_name"  TEXT,
        "user_name_discriminator"   TEXT
    );
    """

    curs = database.cursor()
    try:
        curs.execute(
            "SELECT channel_id,user_id,delay,last_slowmode,channel_name,user_name_discriminator FROM slowmode_info"
        )
    except sqlite3.OperationalError:
        print("Database error")
        print("Try to create table in database")
        try:
            curs.execute(sql_request)
        except sqlite3.OperationalError:
            print("Table already exists, but an error occurred")
            print("Try to recreate table")

            curs.execute("DROP TABLE slowmode_info")
            curs.execute(sql_request)
        database.commit()


def load_cog(path, bot):
    for content in os.listdir(path):
        if os.path.isdir(f"{path}/{content}"):
            load_cog(f"{path}/{content}", bot)
        else:
            if content.endswith(".py"):
                bot.load_extension(f"{path}/{content}"[:-3].replace("/", "."))
