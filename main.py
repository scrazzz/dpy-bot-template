import discord
from discord.ext import commands
import aiohttp

import config

extensions = ()

class TheBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents(
            guild=True,
            members=True,
            messages=True,
            reactions=True,
            message_content=True,
        )
        super().__init__(
            command_prefix=['!'],
            help_attrs=dict(hidden=True),
            intents=intents,
            pm_help=None,
        )
    
    async def setup_hook(self) -> None:
        self.session = aiohttp.ClientSession()
        for ext in extensions:
            await self.load_extension(ext)
    
    async def on_command_error(self, ctx, error: commands.CommandError) -> None:
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('This command cannot be used in private messages.')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('Sorry. This command is disabled and cannot be used.')
        elif isinstance(error, commands.CommandInvokeError):
            original = error.original
            if not isinstance(original, discord.HTTPException):
                # log.exception('In %s:', ctx.command.qualified_name, exc_info=original)
                print('In ', ctx.command.qualified_name)
        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send(str(error))

    async def on_ready(self):
        print('Ready ', self.user, self.user.id)

    async def close(self) -> None:
        await super().close()
        await self.session.close()

bot = TheBot()
bot.run(token=config.token)
