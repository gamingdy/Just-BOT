import discord

from config import TOKEN

bot = discord.Bot()


@bot.event
async def on_ready():
    print("Bot started")


bot.run(TOKEN)
