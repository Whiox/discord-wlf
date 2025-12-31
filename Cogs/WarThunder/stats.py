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
        mode: Option(str, "Выберите игровой режим", choices=["AB", "RB", "SB"], default="RB"),
        type: Option(str, "Выберите тип игры", choices=["Air", "Ground"], default="Ground"),
        period: Option(str, "За какой период", choices=["Month", "All"], default="All"),
    ):
        embed = Embed(color=Setting.get_color(ctx))

        user = user_search(username)

        if user['id'] == 0:
            embed.title = f"Не удалось найти игрока {username}"

            return [2, embed]

        period = 'current' if period == 'All' else 'month'

        user_stats = get_user_data(user['id'])

        mode_stats = user_stats['stats'][str(type).lower()][str(mode).lower()]

        embed.title = f"{user_stats['username']} {user_stats['id']}"
        embed.description = f"Статистика в {mode} для {type} за {'всё время' if period == 'current' else 'месяц'}"

        embed.add_field(name="Статистика игрока", value='', inline=False)

        if mode_stats[period]['kills_player'] and mode_stats[period]['total_deaths']:
            embed.add_field(
                name="К/Д",
                value=f"{round(mode_stats[period]['kills_player']/mode_stats[period]['total_deaths'], 2)}",
                inline=True
            )
        if mode_stats[period]['kills_player'] and mode_stats[period]['total_deaths']:
            embed.add_field(
                name="К/В",
                value=f"{round(mode_stats[period]['kills_player']/mode_stats[period]['total_spawns'], 2)}",
                inline=True
            )

        embed.add_field(name="Статистика по играм", value='', inline=False)

        if mode_stats[period]['total_sessions'] and mode_stats[period]['victories_sessions']:
            embed.add_field(
                name="Количество игр",
                value=f"{mode_stats[period]['total_sessions']}",
                inline=True
            )

            embed.add_field(
                name="Выйгранные игры",
                value=f"{mode_stats[period]['victories_sessions']}",
                inline=True
            )

            embed.add_field(
                name="Процент побед",
                value=f"{round(int(mode_stats[period]['victories_sessions'])/int(mode_stats[period]['total_sessions']) * 100, 2)}%",
                inline=True
            )

        if mode_stats['current']['relative_position']:
            embed.add_field(
                name="Среднее место в команде",
                value=f"{round(float(mode_stats[period]['relative_position']) * 100, 5)}%",
                inline=False
            )

        if mode_stats[period]['average_score']:
            embed.add_field(
                name="Средний счёт",
                value=f"{int(mode_stats[period]['average_score'])}",
                inline=False
            )

        if embed.fields:
            embed.add_field(
                name=f"Статистика от <t:{int(user_stats['timestamp'])}:F>",
                value=f"Данные обновятся в течении 24 часов",
                inline=False
            )

        else:
            embed.description = f"Статистика в {mode} для {type} не найдена"

        return [2, embed]


def setup(bot):
    bot.add_cog(Stats(bot))
