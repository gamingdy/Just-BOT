import discord

from config import TOKEN, debug_guild
from Utils.funct import load_cog, verify_db

bot = discord.Bot(intents=discord.Intents.all(), debug_guilds=debug_guild)


@bot.event
async def on_ready():
    print("Bot started")


verify_db()
load_cog("commands", bot)
bot.load_extension("command_test.cog_test")
bot.run(TOKEN)
