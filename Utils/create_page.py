import discord


def generate_page(embed, *args):
    embed.clear_fields()
    for value, name in args:
        embed.add_field(name=name, value=value, inline=False)


class PageNavigation(discord.ui.View):
    def __init__(self, nb_page, all_pages, embed, author):
        super().__init__()
        self.disable_on_timeout = True
        self.timeout = 60
        self.embed = embed
        self.all_pages = all_pages
        self.max_page = nb_page
        self.actual_page = 0
        self.author = author

    @discord.ui.button(label="Previous")
    async def previous_page(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        if self.author.id == interaction.user.id:
            self.actual_page = (self.actual_page - 1) % self.max_page
            generate_page(self.embed, *iter(self.all_pages[self.actual_page]))
            self.embed.set_footer(text=f"Page {self.actual_page + 1}/{self.max_page}")
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
            generate_page(self.embed, *iter(self.all_pages[self.actual_page]))
            self.embed.set_footer(text=f"Page {self.actual_page + 1}/{self.max_page}")
            await interaction.response.edit_message(embed=self.embed)
        else:
            await interaction.response.send_message(
                "Sorry you are not allowed to interacted with this message",
                ephemeral=True,
            )
