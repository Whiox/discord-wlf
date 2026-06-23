
from discord import ApplicationContext, Embed, Option, SlashCommandGroup
from discord.ext import commands

from thunderget import get_user_data, user_search, squadron_search

from settings import Setting, DB, CommandResponse, measure_execution_time


class WarThunder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    warthunder_group = SlashCommandGroup(
        name="warthunder",
        description="Статистика War Thunder",
        integration_types=Setting.integration_types,
        contexts=Setting.contexts,
        guild_ids=Setting.guilds_ids
    )

    @warthunder_group.command(
        name='stats',
        description='Статистика игрока по нику'
    )
    @measure_execution_time()
    async def stats(
        self,
        ctx: ApplicationContext,
        username: str = Option(str, "Ник игрока"),
        mode: str = Option(str, "Выберите игровой режим", choices=["AB", "RB", "SB"], default="RB"),
        vehicle_type: str = Option(str, "Выберите тип игры", name="type", choices=["Air", "Ground"], default="Ground"),
        period: str = Option(str, "За какой период", choices=["Month", "All"], default="All"),
    ):
        embed = Embed(color=DB.get_color(ctx))

        user = user_search(username)

        if user['id'] == 0:
            embed.title = f"Не удалось найти игрока {username}"

            return CommandResponse(
                embed=embed,
            )

        period = 'current' if period == 'All' else 'month'

        user_stats = get_user_data(user['id'])

        mode_stats = user_stats['stats'][str(vehicle_type).lower()][str(mode).lower()]

        embed.title = f"{user_stats['username']} {user_stats['id']}"
        embed.description = f"Статистика в {mode} для {vehicle_type} за {'всё время' if period == 'current' else 'месяц'}"

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
            embed.description = f"Статистика в {mode} для {vehicle_type} не найдена"

        return CommandResponse(
            embed=embed,
        )


    @warthunder_group.command(
        name='squadron',
        description='Поиск полка по названию'
    )
    @measure_execution_time()
    async def squadron(
        self,
        ctx: ApplicationContext,
        name: Option(str, "Название полка")
    ):
        data = squadron_search(name)

        embed = Embed(color=DB.get_color(ctx))

        if data:
            embed.title = f"{data['name']}   {data['tag']}"
            embed.description = data['slogan']
            embed.add_field(name='id', value=data['id'], inline=True)
            embed.add_field(name='status', value=data['status'], inline=True)
            embed.add_field(name='members', value=data['member_count'], inline=True)

        return CommandResponse(
            embed=embed,
        )


def setup(bot):
    bot.add_cog(WarThunder(bot))
