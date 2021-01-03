import discord
from discord.ext import commands


class Trial(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.command()
    async def reee(self, ctx: commands.Context) -> None:
        await ctx.send(ctx.guild.chunked)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Trial(bot))
