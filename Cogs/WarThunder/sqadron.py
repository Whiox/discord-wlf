from discord import ApplicationContext, Embed, Option
from settings import Setting
from discord.ext import commands

from thunderget import squadron_search


class Squadron(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='squadron',
        description='Поиск полка по названию',
        integration_types=Setting.integration_types,
        contexts=Setting.contexts,
        guild_ids=Setting.guilds_ids
    )
    @Setting.measure_execution_time()
    async def squadron(
            self,
            ctx: ApplicationContext,
            name: Option(str, "Название полка")
    ):
        data = squadron_search(name)

        embed = Embed(color=Setting.get_color(ctx))

        if data:
            embed.title = f"{data['name']}   {data['tag']}"
            embed.description = data['slogan']
            embed.add_field(name='id', value=data['id'], inline=False)
            embed.add_field(name='status', value=data['status'], inline=False)
            embed.add_field(name='members', value=data['member_count'], inline=False)

        return [2, embed]


def setup(bot):
    bot.add_cog(Squadron(bot))
