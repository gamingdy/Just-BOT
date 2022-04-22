import discord
import os

from config import TOKEN

bot = discord.Bot(
    intents=discord.Intents.all(), debug_guilds=[703389879706320980, 703008423738081311]
)


@bot.event
async def on_ready():
    print("Bot started")


def load_cog(path):
    for content in os.listdir(path):
        if os.path.isdir(f"{path}/{content}"):
            load_cog(f"{path}/{content}")
        else:
            if content.endswith(".py"):
                bot.load_extension(f"{path}/{content}"[:-3].replace("/", "."))


load_cog("commands")
bot.run(TOKEN)
