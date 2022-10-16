import discord


def generate_page(embed, *args):
    embed.clear_fields()
    for value, name in args:
        embed.add_field(name=name, value=value, inline=False)


class PageNavigation(discord.ui.View):
    def __init__(self, nb_page, all_pages, embed):
        super().__init__()
        self.embed = embed
        self.all_pages = all_pages
        self.max_page = nb_page
        self.actual_page = 0

    @discord.ui.button(label="Previous")
    async def previous_page(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self.actual_page = (self.actual_page - 1) % self.max_page
        generate_page(self.embed, *iter(self.all_pages[self.actual_page]))
        self.embed.set_footer(
            text=f"Page {self.actual_page + 1}/{self.max_page}")
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(label="Next")
    async def next_page(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self.actual_page = (self.actual_page + 1) % self.max_page
        generate_page(self.embed, *iter(self.all_pages[self.actual_page]))
        self.embed.set_footer(
            text=f"Page {self.actual_page + 1}/{self.max_page}")
        await interaction.response.edit_message(embed=self.embed)
