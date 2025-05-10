from settings import Setting
from discord import ApplicationContext
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='help',
        description='Информация о командах бота',
        integration_types=Setting.integration_types,
        contexts=Setting.contexts,
        guild_ids=Setting.guilds_ids
    )
    @Setting.measure_execution_time()
    async def user(
        self,
        ctx: ApplicationContext
    ):
        embed = Setting.Basic.Help.get_embed()
        embed.title = 'Чтобы узнать подробности выберите нужный вам раздел'
        embed.add_field(name="Basic", value=Setting.Basic.Help.help_command["Basic"], inline=False)
        embed.add_field(name="Converter", value=Setting.Basic.Help.help_command["Converter"], inline=False)
        embed.color = Setting.get_color(ctx)
        return [8, embed, Setting.Basic.Help.get_view()]


def setup(bot):
    bot.add_cog(Help(bot))