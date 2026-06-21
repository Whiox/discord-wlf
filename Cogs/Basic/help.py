from settings import Setting, DB
from discord import ApplicationContext, Embed, SelectOption
from discord.ext import commands
from discord.ui import select, View


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
        embed = Embed()
        embed.title = 'Чтобы узнать подробности выберите нужный вам раздел'
        embed.add_field(name="Basic", value=Help.help_command["Basic"], inline=False)
        embed.add_field(name="Converter", value=Help.help_command["Converter"], inline=False)
        embed.add_field(name="War Thunder", value=Help.help_command["War Thunder"], inline=False)
        embed.color = DB.get_color(ctx)
        return [8, embed, Help.get_view()]

    options = [
        SelectOption(
            label="Basic",
            description="Получить информацию о базовых функциях"
        ),
        SelectOption(
            label="Converter",
            description="Получить информацию о функциях с конвертацией"
        ),
        SelectOption(
            label="War Thunder",
            description="Получить информацию о возможностях функций с тундрой"
        ),
    ]

    help_command = {
        'Basic': '`help`, `user`, `ping`, `color`, `mode`',
        'Converter': '`gif`, `png`, `reply`',
        'War Thunder': '`squadron`, `stats`'
    }

    help_data = {
        'Basic': '`help`\n'
                 'Выводит сообщение с выпадающим списком команд\n\n'
                 '`user`\n'
                 'Выводит информацию о пользователе (аватарка, баннер, id, дата регистрации)\n\n'
                 '`ping`\n'
                 'Проверьте работоспособность бота и его связь с бд\n\n'
                 '`color`\n'
                 'Измените цвет ваших embed (выберите 1 заготовленный из списка или напиши свой hex-код)\n\n'
                 '`mode`\n'
                 'Измените свои настройки приватности (True - все сообщения видны только вам)',
        'Converter': '`gif`\n'
                     'Конвертирует png, jpeg, webp изображения в Gif-фаил\n\n'
                     '`png`\n'
                     'Конвертирует jpeg, webp, gif(первый кадр) изображения в png картинку\n\n'
                     '`reply`\n'
                     'Создать из png, jpeg, webp, gif изображений "reply" gif',
        'War Thunder': '`squadron`\n'
                       'Ищет полк по названию\n\n'
                       '`stats`\n'
                       'Выводит статистику игрока по нику'
    }

    @staticmethod
    def get_view():
        class MyView(View):
            def __init__(self):
                super().__init__(timeout=None)

            @select(placeholder="Выберите нужный раздел", custom_id="select-help", options=Help.options)
            @Setting.view_measure_execution_time()
            async def select_callback(self, select, interaction):
                embed = Embed(
                    title=select.values[0],
                    description=Help.help_data[select.values[0]],
                    color=DB.get_color(interaction))
                return [embed]

        return MyView()


def setup(bot):
    bot.add_cog(Help(bot))