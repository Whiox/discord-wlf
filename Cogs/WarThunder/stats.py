import discord
from settings import Setting
from discord import ApplicationContext, Embed, Option
from discord.ext import commands

from thunderget import get_user_data, user_search


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='stats',
        description='Статистика игрока по нику',
        integration_types=Setting.integration_types,
        contexts=Setting.contexts,
        guild_ids=Setting.guilds_ids
    )
    @Setting.measure_execution_time()
    async def stats(
        self,
        ctx: ApplicationContext,
        username: Option(str, "Ник игрока"),
        mode: Option(str, "Выберите игровой режим", choices=["AB", "RB", "SB"]),
        type: Option(str, "Выберите тип игры", choices=["Air", "Ground"])
    ):
        embed = Embed(color=Setting.get_color(ctx))

        user_id = user_search(username)['id']
        user_stats = get_user_data(user_id)

        mode_stats = user_stats['stats'][str(type).lower()][str(mode).lower()]

        embed.title = f"{user_stats['username']} {user_stats['id']}"
        embed.description = f"Статистика в {mode} для {type}"

        embed.add_field(
            name="Соотношение убийств/смертей (Кд)",
            value=f"{round(mode_stats['current']['kills_player']/mode_stats['current']['total_deaths'], 2)}",
            inline=False
        )

        embed.add_field(
            name="Количество игр",
            value=f"{mode_stats['current']['total_sessions']}",
            inline=True
        )

        embed.add_field(
            name="Выйгранные игры",
            value=f"{mode_stats['current']['victories_sessions']}",
            inline=True
        )

        embed.add_field(
            name="Процент побед",
            value=f"{round(int(mode_stats['current']['victories_sessions'])/int(mode_stats['current']['total_sessions']) * 100, 2)}%",
            inline=True
        )

        embed.add_field(
            name="Среднее место в команде",
            value=f"{round(float(mode_stats['current']['relative_position']) * 100, 5)}%",
            inline=False
        )

        embed.add_field(
            name="Средний счёт",
            value=f"{int(mode_stats['current']['average_score'])}",
            inline=False
        )

        return [2, embed]


def setup(bot):
    bot.add_cog(Stats(bot))
