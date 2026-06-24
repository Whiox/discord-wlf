
from discord import ApplicationContext, Embed, Option
from discord.ext import commands

from src.settings import Setting, DB, CommandResponse, process_command


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
    @process_command()
    async def mode(
        self,
        ctx: ApplicationContext,
        private = Option(str, "Выберите", choices=["Приватный", "Публичный"])
    ):
        embed = Embed(title="Ваши настройки приватности были изменены")
        embed.colour = DB.get_color(ctx)
        private = (True if private == "Включить режим" else False)
        embed.description = "Сообщения видны только вам" if private else "Сообщения видны всем"
        DB.set_private(ctx, private)

        return CommandResponse(
            embed=embed,
        )


def setup(bot):
    bot.add_cog(Mode(bot))