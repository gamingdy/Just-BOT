import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
import sqlite3

from Utils.funct import create_embed
from Utils.create_page import generate_page, PageNavigation


class TestCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect("data/bot_db.db")

    test_command = SlashCommandGroup("test", "Test command")

    @test_command.command()
    async def test(self, ctx):
        channel = ctx.channel
        element = (
            self.db.cursor()
            .execute(
                "SELECT delay,user_name_discriminator FROM slowmode_info WHERE channel_id = (?) ORDER BY delay DESC",
                (channel.id,),
            )
            .fetchall()
        )
        if element:
            all_page = [element[i : i + 5] for i in range(0, len(element), 5)]
            my_embed = create_embed("Slowmode list")
            all_page = list(
                map(
                    lambda l: list(map(lambda i: (f"Delay: {i[0]}", i[1]), l)),
                    all_page,
                )
            )

            generate_page(my_embed, *iter(all_page[0]))
            my_embed.set_footer(text=f"1/{len(all_page)}")

            my_navigation = PageNavigation(len(all_page), all_page, my_embed)
            await ctx.respond(embed=my_embed, view=my_navigation)


def setup(bot):
    bot.add_cog(TestCommand(bot))
