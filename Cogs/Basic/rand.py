from random import randint
from discord import ApplicationContext
from settings import Setting
from discord.ext import commands


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
        embed = Setting.Basic.Rand.rand_embed
        embed.title = Setting.Basic.Rand.rand_bad if randint(0, 1) == 0 else Setting.Basic.Rand.rand_good
        embed.description = Setting.Basic.Rand.rand_desc_bad if randint(0, 1) == 0 else Setting.Basic.Rand.rand_desc_good
        embed.color = Setting.get_color(ctx)
        embed.set_image(url=Setting.Basic.Rand().get_image())
        return [2, embed]


def setup(bot):
    bot.add_cog(Rand(bot))