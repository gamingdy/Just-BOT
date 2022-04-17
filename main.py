import discord

from config import TOKEN

bot = discord.Bot(
    intents=discord.Intents.all(), debug_guilds=[703389879706320980, 703008423738081311]
)


@bot.event
async def on_ready():
    print("Bot started")


cog_list = ["commands.cogs.user_slow"]

for cog in cog_list:
    bot.load_extension(cog)

bot.run(TOKEN)
