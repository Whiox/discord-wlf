
from discord import ApplicationContext, Embed, Option
from discord.ext import commands

from src.settings import Setting, DB, CommandResponse, process_command


default_colors = {
    'dark_teal': '11806A',
    'brand_green': '57F287',
    'green': '2ECC71',
    'dark_green': '1F8B4C',
    'blue': '3498DB',
    'dark_blue': '206694',
    'gold': 'F1C40F',
    'dark_gold': 'C27C0E',
    'orange': 'E67E22',
    'dark_orange': 'A84300',
    'brand_red': 'ED4245',
    'red': 'E74C3C',
    'dark_red': '992D22',
    'lighter_grey': '95A5A6',
    'dark_grey': '607D8B',
    'light_grey': '979C9F',
    'darker_grey': '546E7A',
    'og_blurple': '7289DA',
    'blurple': '5865F2',
    'greyple': '99AAB5',
    'dark_theme': '36393F',
    'fuchsia': 'EB459E',
    'yellow': 'FEE75C',
    'nitro_pink': 'F47FFF'
}


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
    @process_command()
    async def color(
        self,
        ctx: ApplicationContext,
        color: Option(
            str,"Выберите один из стандартных цветов",
            choices=list(default_colors.keys()),
            default=None
        ),
        custom_color: Option(
            str,"Напишите свой Hex цвет",
            default=None
        )
    ):
        embed = Embed()

        if bool(color) == bool(custom_color):
            embed.title = "Ваш цвет не был изменён"
            embed.description = f"Ошибка вводимого значения"
            embed.add_field(name="Ошибка", value=f"Выберите один из двух вариантов ввода - {color}", inline=False)
            return [2, embed]

        embed.description = f"Текущий цвет - {color}"

        if color:
            color = default_colors[color]
        if custom_color:
            color = custom_color

        try:
            # Меняем цвет
            embed.description = f"Текущий цвет - {color}"
            embed.colour = int(color, 16)
            DB.set_color(ctx, color)

        except ValueError:
            embed.title = "Ваш цвет не был изменён"
            embed.description = f"Ошибка вводимого значения"
            embed.add_field(name="Ошибка", value=f"Введённый вами цвет не существует - "
                                                 f"{color if color else custom_color}", inline=False)
            embed.add_field(name="Используйте конвертер", value="Используйте любой rgb to hex конвертер", inline=False)
            embed.colour = DB.get_color(ctx)

        return CommandResponse(
            embed=embed,
        )


def setup(bot):
    bot.add_cog(Color(bot))