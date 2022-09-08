import discord

from config import TOKEN, debug_guild
from Utils.funct import load_cog, verify_db, verify_user_slowmode

statut = discord.Status.do_not_disturb
bot = discord.Bot(
    intents=discord.Intents.all(), status=statut, debug_guilds=debug_guild
)


@bot.event
async def on_ready():
    print("Bot started")
    print("Checking users in slowmode")
    await verify_user_slowmode(bot)
    print("Checking completed")


verify_db()
load_cog("commands", bot)
bot.run(TOKEN)
