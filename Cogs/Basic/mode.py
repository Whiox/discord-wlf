import discord
from settings import Setting
from discord import ApplicationContext
from discord.ext import commands


class Mode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='mode',
        description='Переключить режим приватности',
        integration_types=Setting.integration_types,
        contexts=Setting.contexts,
        guild_ids=Setting.guilds_ids
    )
    @Setting.measure_execution_time()
    async def mode(
        self,
        ctx: ApplicationContext,
        private = discord.Option(str, "Выберите",
                                 choices=["Включить режим", "Выключить режим"])
    ):
        embed = Setting.Basic.Mode.get_embed()
        embed.color = discord.Color(Setting.get_color(ctx))
        private = (True if private == "Включить режим" else False)
        embed.description = f"Значение для private - {private}"
        Setting.set_private(ctx, private)
        return [2, embed]


def setup(bot):
    bot.add_cog(Mode(bot))