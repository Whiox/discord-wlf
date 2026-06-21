import discord
from settings import Setting
from discord import ApplicationContext, Embed
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
        private = discord.Option(str, "Выберите", choices=["Приватный", "Публичный"])
    ):
        embed = Embed(title="Ваши настройки приватности были изменены")
        embed.color = discord.Color(Setting.get_color(ctx))
        private = (True if private == "Включить режим" else False)
        embed.description = "Сообщения видны только вам" if private else "Сообщения видны всем"
        Setting.set_private(ctx, private)
        return [2, embed]


def setup(bot):
    bot.add_cog(Mode(bot))