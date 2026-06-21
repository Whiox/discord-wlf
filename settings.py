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

from target_cloud_detect import Model


class Setting:
    db = Database()

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

        class ReplySmart:
            model = None

            @staticmethod
            def get_embed():
                return Embed(
                    title="reply-GIF"
                )

            @staticmethod
            def process_image(bytes):
                if not Setting.Converter.ReplySmart.model:
                    Setting.Converter.ReplySmart.model = Model()
                return Setting.Converter.ReplySmart.model.predict_from_bytes(bytes)
