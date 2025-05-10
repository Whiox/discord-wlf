import discord
from settings import Setting
from discord import ApplicationContext
from discord.ext import commands


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
    @Setting.measure_execution_time()
    async def ping(
        self,
        ctx: ApplicationContext
    ):
        latency = self.bot.latency
        ping = Setting.get_db_ping(ctx)
        ping_ms = round(ping * 1000, 2)
        ping_s = round(ping, 2)
        embed = Setting.Basic.Ping.get_embed()
        embed.color = discord.Color(Setting.get_color(ctx))
        embed.add_field(name="Задержка до бота" ,value=f'{latency * 1000:.2f}мс/{latency:.2f}с', inline=False)
        embed.add_field(name="Задержка до базы", value=f'{ping_ms}мс/{ping_s:.2f}с', inline=False)
        return [2, embed]


def setup(bot):
    bot.add_cog(Ping(bot))