import time
import json

import discord

from Utils.funct import load_cog, verify_db, verify_user_slowmode
from config import TOKEN, debug_guild

statut = discord.Status.do_not_disturb
bot = discord.Bot(
    intents=discord.Intents.all(), status=statut, debug_guilds=debug_guild
)


@bot.event
async def on_ready():
    print("Bot started")
    with open("data/info.json", "w") as info:
        data = {"boot": time.time()}
        json.dump(data, info, indent=4)
    print("Checking users in slowmode")
    await verify_user_slowmode(bot)
    print("Checking completed")
    total_guild = [
        "{} ({})".format(guild.name, guild.member_count) for guild in bot.guilds
    ]
    print("Found {} guilds: {}".format(len(total_guild), ",".join(total_guild)))


verify_db()
load_cog("commands", bot)
bot.load_extension("command_test.cog_test")
bot.run(TOKEN)
