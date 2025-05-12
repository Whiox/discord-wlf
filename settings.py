import time
import json
import random
import discord
import asyncio
from discord import Embed
from functools import wraps
from database import Database
from discord import IntegrationType
from discord import ApplicationContext
from discord import InteractionContextType


class Setting:
    db = Database()

    extensions = [
        'basic.ping',
        'basic.rand',
        'basic.color',
        'basic.user',
        'basic.mode',
        'basic.help',
        'converter.gif',
        'converter.png',
        'converter.reply',
    ]

    integration_types = [
        IntegrationType.user_install,
        IntegrationType.guild_install,
    ]

    contexts = [
        InteractionContextType.guild,
        InteractionContextType.bot_dm,
        InteractionContextType.private_channel,
    ]

    guilds_ids = None

    @staticmethod
    def check_user(ctx: ApplicationContext):
        if Setting.db.check_user(ctx.user.id): pass
        else: Setting.db.add_user(ctx)

    @staticmethod
    def get_color(ctx: ApplicationContext):
        Setting.check_user(ctx)
        color = Setting.db.get_color(ctx.user.id)
        if color == '1':
            color = f"#{random.randint(0, 0xFFFFFF):06X}"[1:]
        return int(color, 16)

    @staticmethod
    def get_private(ctx: ApplicationContext):
        Setting.check_user(ctx)
        return Setting.db.get_private(ctx.user.id)

    @staticmethod
    def set_private(ctx: ApplicationContext, private):
        Setting.check_user(ctx)
        Setting.db.set_private(ctx.user.id, private)

    @staticmethod
    def set_color(ctx: ApplicationContext, color):
        Setting.check_user(ctx)
        Setting.db.set_color(ctx.user.id, color)

    @staticmethod
    def get_first_command(ctx):
        Setting.check_user(ctx)
        return Setting.db.get_first_command(ctx.user.id)

    @staticmethod
    def get_db_ping(ctx: ApplicationContext):
        Setting.check_user(ctx)
        return Setting.db.get_ping(ctx.user.id)

    @staticmethod
    def get_current_time():
        return time.time()

    @staticmethod
    def get_delta_time(old_time: float):
        return round(time.time() - old_time, 2)

    @staticmethod
    def measure_execution_time():
        def decorator(func):
            @wraps(func)
            async def wrapper(self, ctx, *args, **kwargs):
                try:
                    private = Setting.get_private(ctx)
                    if func.__name__ == 'mode': private = True

                    if not ctx.response.is_done(): await ctx.defer(ephemeral=private)

                    start_time = Setting.get_current_time()
                    response = await func(self, ctx, *args, **kwargs)
                    embed = response[1]
                    embed.set_footer(
                        text=f"Время на выполнение: {Setting.get_delta_time(start_time)}с"
                    )

                    code = response[0]
                    if code == 2:
                        await ctx.respond(embed=embed, ephemeral=private)
                    elif code == 4:
                        file = response[2]
                        await ctx.respond(embed=embed, file=file, ephemeral=private)
                    elif code == 8:
                        view = response[2]
                        await ctx.respond(embed=embed, view=view, ephemeral=private)

                except Exception as e:
                    print(f"Ошибка в команде {func.__name__}: {e}")
                    if not ctx.response.is_done():
                        await ctx.respond("Произошла ошибка при выполнении команды.", ephemeral=True)
            return wrapper
        return decorator

    @staticmethod
    def view_measure_execution_time():
        def decorator(func):
            @wraps(func)
            async def wrapper(self, select, interaction, *args, **kwargs):
                try:
                    start_time = Setting.get_current_time()
                    response = await func(self, select, interaction, *args, **kwargs)
                    embed = response[0]
                    embed.set_footer(
                        text=f"Время на выполнение: {Setting.get_delta_time(start_time)}с"
                    )
                    await interaction.edit(embed=embed)
                except Exception as e:
                    print(f"Ошибка в команде {func.__name__}: {e}")
                    if not interaction.response.is_done():
                        await interaction.respond("Произошла ошибка при выполнении команды.", ephemeral=True)
            return wrapper
        return decorator

    class Basic:

        class Ping:
            @staticmethod
            def get_embed():
                return Embed(
                    title='Задержка бота',
                )
            ping_title = "Задержка бота"

        class Rand:
            rand_bad = "Вам пизда черти ебаные"
            rand_good = "Играйте пб умнички ;3"
            rand_desc_bad = "(Даже не пытайтесь дебики)"
            rand_desc_good = "(Попробуйте, хуже не будет ;3)"
            rand_embed = Embed()

            images = [
                'https://cdn.discordapp.com/attachments/1266472308235571261/1309271448094773299/'
                'a922aa26e575735d59359ce3d3ab6cf9.png?ex=6740f98e&is=673fa80e&hm=73d524bae14997a'
                          'c28a0f5a2a673e5cce3ad7765a0365743043c20b9446914fc&',

                'https://tenor.com/view/%D0%BF%D0%BE%D0%BD%D0%B0%D0%B1%D0%B8%D1%80%D0%B0%D1%8E%D1%82-%D0%BF%'
                'D0%BE%D0%BD%D0%B0%D0%B1%D0%B8%D1%80%D0%B0%D1%8E%D1%82-%D0%B2%D1%81%D1%8F%D0%BA%D0%B8%D1%85-%'
                'D0%BF%D0%BE%D0%BD%D0%B0%D0%B1%D0%B8%D1%80%D0%B0%D1%8E%D1%82-%D0%B2%D1%81%D1%8F%D0%BA%D0%B8%D'
                '1%85-%D0%BC%D0%B4-murder-drones-%D0%BF%D0%BE%D0%BD%D0%B0%D0%B1%D0%B8%D1%80%D0%B0%D1%8E%D1%82'
                '-murder-drones-copper-9-gif-12858669765758162211'
            ]

            def get_image(self):
                return random.choice(self.images)


        class Color:
            @staticmethod
            def get_embed():
                return Embed(
                    title="Ваш цвет изменён"
                )

            default_colors = {
                'random': '1',
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

        class User:
            @staticmethod
            def get_embed():
                return Embed()

        class Mode:
            @staticmethod
            def get_embed():
                return Embed(
                    title="Ваши настройки приватности были изменены"
                )

        class Help:
            @staticmethod
            def get_embed():
                return Embed()

            options = [
                discord.SelectOption(
                    label="Basic",
                    description="Получить информацию о базовых функциях"
                ),
                discord.SelectOption(
                    label="Converter",
                    description="Получить информацию о функциях с конвертацией"
                ),
            ]

            help_command = {
                'Basic': '`help`, `user`, `ping`, `color`, `mode`',
                'Converter': '`gif`, `png`, `reply`',
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
            }

            @staticmethod
            def get_view():
                class MyView(discord.ui.View):
                    def __init__(self):
                        super().__init__(timeout=None)

                    @discord.ui.select(placeholder="Выберите нужный раздел", custom_id="select-help",
                                       options=Setting.Basic.Help.options)
                    @Setting.view_measure_execution_time()
                    async def select_callback(self, select, interaction):
                        embed = discord.Embed(
                            title=select.values[0],
                            description=Setting.Basic.Help.help_data[select.values[0]],
                            color=Setting.get_color(interaction))
                        return [embed]

                return MyView()

    class Converter:

        class Png:
            @staticmethod
            def get_embed():
                return Embed(
                    title="PNG"
                )

        class Gif:
                @staticmethod
                def get_embed():
                    return Embed(
                        title="GIT"
                    )

        class Reply:
            @staticmethod
            def get_embed():
                return Embed(
                    title="reply-GIF"
                )
