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
import asyncio
import datetime
import logging
import traceback
from contextlib import contextmanager

import discord
import jishaku
import wavelink
from discord.ext import commands

import config

class RoboUmbra(commands.Bot):
    """
    Robotic Umbra, what more could you want?
    Umbra#0009, but only speaks when spoken to.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix=self.prefix,
                         allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False),
                         activity=discord.Activity(
                             type=discord.ActivityType.listening, name="Umbral Shadows"),
                         **kwargs)
        self.version = {'discord.py': discord.__version__,
                        'wavelink': wavelink.__version__,
                        'jishaku': jishaku.__version__} #pylint: disable=no-member
        self.config = config
        self.description = self.__doc__
        self.emoji = {True: "<:TickYes:735498312861351937>",
                      False: "<:CrossNo:735498453181923377>",
                      None: "<:QuestionMaybe:738038828928860269>"}
        self.ignored_exceptions = (commands.CommandNotFound,)
        self.loop.create_task(self.owner_setter())
        self.add_check(self.owner_call)

        for extension in config.EXTENSIONS:
            try:
                self.load_extension(extension)
            except Exception:
                traceback.print_exc()
                continue

    async def owner_setter(self):
        """ A quick coro to set the bot's owner. """
        await self.wait_until_ready()
        if not self.owner_id:
            self.owner_id = (await self.application_info()).owner.id

    async def owner_call(self, ctx: commands.Context):
        """ Bot check. """
        return await self.is_owner(ctx.author)

    async def _exception_handle(self, exception: Exception):
        exception_fmt = traceback.format_exception(type(exception), exception, exception.__traceback__, 4)
        embed = discord.Embed(title="Error Chief.")
        embed.description = f"```py\n{''.join(exception_fmt)}\n```"
        embed.timestamp = datetime.datetime.utcnow()
        await self.get_user(self.owner_id).send(embed=embed)

    async def on_ready(self):
        """ Robo Umbra is alive and working. """
        await asyncio.sleep(5)
        return print(f"Logged in :: {self.user.name} & {self.user.id} with owner {self.owner_id}")

    async def prefix(self, bot: commands.Bot, message: discord.Message):
        """ Return my prefixes. """
        return commands.when_mentioned_or(">:")(bot, message)

    async def on_message(self, message: discord.Message):
        """ Overridden message event. """
        if message.author.id == self.owner_id:
            await self.process_commands(message)

    async def on_message_edit(self, _: discord.Message, after: discord.Message):
        """ Process commands after edit too. """
        if after.author.id == self.owner_id:
            await self.process_commands(after)

    async def on_command_error(self, ctx: commands.Context, error: Exception):
        """ Global error handler. Suppress the noise. """
        error = getattr(error, "original", error)
        if isinstance(error, self.ignored_exceptions):
            await ctx.message.add_reaction(self.emoji[None])
            return
        else:
            raise error


@contextmanager
def setup_logging():
    """ Setup my logger. """
    try:
        logging.getLogger('discord').setLevel(logging.INFO)
        logging.getLogger('discord.http').setLevel(logging.WARNING)

        log = logging.getLogger()
        log.setLevel(logging.INFO)
        handler = logging.FileHandler(
            filename='RUmbra.log', encoding='utf-8', mode='w')
        dt_fmt = '%Y-%m-%d %H:%M:%S'
        fmt = logging.Formatter(
            '[{asctime}] [{levelname:<7}] {name}: {message}', dt_fmt, style='{')
        handler.setFormatter(fmt)
        log.addHandler(handler)

        yield
    finally:
        # __exit__
        handlers = log.handlers[:]
        for hdlr in handlers:
            hdlr.close()
            log.removeHandler(hdlr)


def run_bot():
    """ Start the bot. """
    bot = RoboUmbra()
    bot.run(config.BOT_TOKEN)

with setup_logging():
    run_bot()
