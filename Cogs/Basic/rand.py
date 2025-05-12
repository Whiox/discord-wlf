from discord import ApplicationContext, Embed
from settings import Setting
from discord.ext import commands

from Cogs.Basic.Rand import random_logic as rl


class Rand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='rand',
        description='Узнайте ваш таинственный исход на пб',
        integration_types=Setting.integration_types,
        contexts=Setting.contexts,
        guild_ids=Setting.guilds_ids
    )
    @Setting.measure_execution_time()
    async def rand(
        self,
        ctx: ApplicationContext
    ):
        embed = rl.RandomLogic().get_embed(ctx)
        return [2, embed]


def setup(bot):
    bot.add_cog(Rand(bot))
