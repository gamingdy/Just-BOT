import math

import discord

from config import ELEMENTS_PER_PAGE


class PageNavigation(discord.ui.View):
    def __init__(self, all_pages, embed, author):
        super().__init__()
        self.disable_on_timeout = True
        self.timeout = 60
        self.embed = embed
        self.all_pages = all_pages
        self.max_page = math.ceil(len(all_pages) / ELEMENTS_PER_PAGE)
        self.actual_page = 0
        self.author = author

        self.generate_page()

    def generate_page(self):
        self.embed.clear_fields()
        for value, name in self.all_pages[
            self.actual_page
            * ELEMENTS_PER_PAGE : (self.actual_page + 1)
            * ELEMENTS_PER_PAGE
        ]:
            self.embed.add_field(name=name, value=value, inline=False)
        self.embed.set_footer(text=f"Page {self.actual_page + 1}/{self.max_page}")

    @discord.ui.button(label="Previous")
    async def previous_page(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        if self.author.id == interaction.user.id:
            self.actual_page = (self.actual_page - 1) % self.max_page
            self.generate_page()

            await interaction.response.edit_message(embed=self.embed)
        else:
            await interaction.response.send_message(
                "Sorry you are not allowed to interacted with this message",
                ephemeral=True,
            )

    @discord.ui.button(label="Next")
    async def next_page(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        if self.author.id == interaction.user.id:
            self.actual_page = (self.actual_page + 1) % self.max_page
            self.generate_page()

            await interaction.response.edit_message(embed=self.embed)
        else:
            await interaction.response.send_message(
                "Sorry you are not allowed to interacted with this message",
                ephemeral=True,
            )
