
from discord import ApplicationContext, Embed
from discord.ext import commands

from settings import Setting, DB, CommandResponse, process_command


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='ping',
        description='Проверь пинг бота',
        integration_types=Setting.integration_types,
        contexts=Setting.contexts,
        guild_ids=Setting.guilds_ids
    )
    @process_command()
    async def ping(
        self,
        ctx: ApplicationContext
    ):
        latency = self.bot.latency
        ping = DB.get_db_ping(ctx)
        ping_ms = round(ping * 1000, 2)
        ping_s = round(ping, 2)
        embed = Embed(title='Задержка бота')
        embed.colour = DB.get_color(ctx)
        embed.add_field(name="Задержка до бота" ,value=f'{latency * 1000:.2f}мс/{latency:.2f}с', inline=False)
        embed.add_field(name="Задержка до базы", value=f'{ping_ms}мс/{ping_s:.2f}с', inline=False)

        return CommandResponse(
            embed=embed,
        )


def setup(bot):
    bot.add_cog(Ping(bot))