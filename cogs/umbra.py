"""
The MIT License (MIT)

Copyright (c) 2020 AbstractUmbra

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
import datetime

import discord
from discord.ext import commands
from jishaku.codeblocks import codeblock_converter

from utils import formats

class Umbra(commands.Cog):
    """ An owner-only cog, designed for Umbra#0009. """
    def __init__(self, bot: commands.Bot): #TODO: Figure out if we can typehint main bot.
        self.bot = bot

    async def cog_check(self, ctx: commands.Context) -> bool: #pylint: disable=invalid-overridden-method
        return await ctx.bot.is_owner(ctx.author)

    @commands.group(name="robo", aliases=["r"], invoke_without_command=True)
    async def _jsk(self, ctx: commands.Context) -> discord.Message:
        return await self.bot.get_command("jishaku")(ctx)

    @_jsk.command(name="eval", aliases=["py", "dev"])
    async def _eval(self, ctx: commands.Context, *, command_body: codeblock_converter) -> discord.Message:
        return await self.bot.get_command("jishaku python")(ctx, argument=command_body)

    @_jsk.command(name="os", aliases=["system"])
    async def _system(self, ctx: commands.Context, *, shell_body: codeblock_converter) -> discord.Message:
        return await self.bot.get_command("jishaku shell")(ctx, argument=shell_body)

    @_jsk.command(name="broke", aliases=["debug"])
    async def _debug(self, ctx: commands.Context, *, command_string: str) -> discord.Message:
        """ Debugs a command. Disables all local error handling and returns the error. """
        return await self.bot.get_command("jishaku debug")(ctx, command_string=command_string)

    @commands.group(name="cogs", aliases=["cog", "extensions"], invoke_without_command=True)
    async def _cogs(self, ctx: commands.Context) -> discord.Message:
        embed = discord.Embed(title="R. Umbra's loaded cogs.")
        embed.description = formats.to_codeblock("\n".join(map(str, self.bot.cogs)))
        embed.timestamp = datetime.datetime.utcnow()
        return await ctx.send(embed=embed)

    @_cogs.command(name="load", aliases=["start", "enable"])
    async def _load(self, ctx: commands.Context, *, cog_name: str):
        self.bot.load_extension(f"cogs.{cog_name.lower()}")
        return await ctx.message.add_reaction(self.bot.emoji[True])

    @_cogs.command(name="unload", aliases=["stop", "disable"])
    async def _unload(self, ctx: commands.Context, *, cog_name: str):
        self.bot.unload_extension(f"cogs.{cog_name.lower()}")
        return await ctx.message.add_reaction(self.bot.emoji[True])

    @_cogs.command(name="reload", aliases=["restart"])
    async def _reload(self, ctx: commands.Context, *, cog_name: str):
        cog = f"cogs.{cog_name.lower()}"
        try:
            self.bot.reload_extension(cog)
        except commands.ExtensionNotLoaded:
            self.bot.load_extension(cog)
        else:
            return await ctx.message.add_reaction(self.bot.emoji[True])

    @_load.error
    @_unload.error
    @_reload.error
    async def cog_error(self, ctx: commands.Context, error: Exception):
        """ Local error handler for Cog based stuff. """
        error = getattr(error, "original", error)
        if isinstance(error, commands.ExtensionNotFound):
            await ctx.send("That extension wasn't found. Are you sure you're my dev?")
            return await ctx.message.add_reaction(self.bot.emoji[False])
        else:
            print(2)
            await self.bot._exception_handle(error)

def setup(bot: commands.Bot):
    """ Add the cog, generic setup. """
    bot.add_cog(Umbra(bot))
