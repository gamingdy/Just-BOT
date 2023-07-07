from discord.ext import commands


class NotGuildOwner(commands.CheckFailure):
    pass


class NotConnectedInVoiceChannel(commands.CheckFailure):
    pass


class NotVoiceChannelAdmin(commands.CheckFailure):
    pass
