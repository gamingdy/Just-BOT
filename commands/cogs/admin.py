import json

from discord.commands import SlashCommandGroup, option
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.extensions_list = False

    the_admin = SlashCommandGroup("admin", "Only bot admin can use this group")

    def load_extension_list(self):
        with open("data/extension.json", "r") as file:
            self.extensions = json.load(file)

    async def extension_name(self, ctx):
        if not self.extensions_list:
            self.load_extension_list()
            self.extensions_list = True
        return [key for key in self.extensions if key.startswith(ctx.value.lower())]

    @the_admin.command(description="Reload cogs extension")
    @option("extension", autocomplete=extension_name)
    @commands.is_owner()
    async def cog_reload(self, ctx, extension):
        if extension in self.extensions:
            self.bot.reload_extension(self.extensions[extension])
            await ctx.respond(f"{extension} reloaded", ephemeral=True)
        else:
            await ctx.respond(f"Extensions `{extension}` not found", ephemeral=True)


def setup(bot):
    bot.add_cog(Admin(bot))
