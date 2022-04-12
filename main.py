import discord

from config import TOKEN

bot = discord.Bot(
    intents=discord.Intents.all(), debug_guilds=[703389879706320980, 703008423738081311]
)


@bot.event
async def on_ready():
    print("Bot started")


bot.run(TOKEN)
