from settings import Setting
from discord import ApplicationContext
from discord.ext import commands
import discord

class Color(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='color',
        description='Установите цвет в формате <hex> для ваших сообщений или выберите один из стандартных',
        integration_types=Setting.integration_types,
        contexts=Setting.contexts,
        guild_ids=Setting.guilds_ids
    )
    @Setting.measure_execution_time()
    async def color(
        self,
        ctx: ApplicationContext,
        color: discord.Option(
            str,"Выберите один из стандартных цветов",
            choices=list(Setting.Basic.Color.default_colors.keys()),
            default=None
        ),
        custom_color: discord.Option(
            str,"Напишите свой Hex цвет",
            default=None
        )
    ):
        if color and custom_color:
            # Введено слишком много параметров
            embed = Setting.Basic.Color.get_embed()
            embed.description = f"Ошибка вводимого значения"
            embed.add_field(name="Ошибка", value=f"Выберите только один из двух вариантов ввода - {color}", inline=False)
            return [2, embed]

        embed = Setting.Basic.Color.get_embed()
        embed.description = f"Текущий цвет - {color}"

        # Color = значение в словаре/кастомное
        if color is not None and custom_color is None:
            color = Setting.Basic.Color.default_colors[color]
        elif custom_color is not None and color is None:
            color = custom_color
        else:
            # Не было введено ни одного параметра
            embed.title = "Ваш цвет не был изменён"
            embed.description = f"Ошибка вводимого значения"
            embed.add_field(name="Ошибка", value=f"Выберите один вариант ввода", inline=False)

        try:
            # Меняем цвет
            embed.description = f"Текущий цвет - {color}"
            embed.color = int(color, 16)
            Setting.set_color(ctx, color)

        except ValueError:
            embed.title = "Ваш цвет не был изменён"
            embed.description = f"Ошибка вводимого значения"
            embed.add_field(name="Ошибка", value=f"Введённый вами цвет не существует - "
                                                 f"{color if color else custom_color}", inline=False)
            embed.add_field(name="Используйте конвертер", value="Используйте любой rgb to hex конвертер", inline=False)
            embed.color = Setting.get_color(ctx)
        return [2, embed]


def setup(bot):
    bot.add_cog(Color(bot))