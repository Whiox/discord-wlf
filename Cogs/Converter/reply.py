import discord
from discord.ext import commands
from discord import ApplicationContext
from settings import Setting
from PIL import Image, ImageDraw, ImageChops
from io import BytesIO

class Reply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='reply',
        description='Наложить шаблон на изображение',
        integration_types=Setting.integration_types,
        contexts=Setting.contexts
    )
    @Setting.measure_execution_time()
    async def reply(
            self,
            ctx: ApplicationContext,
            file: discord.Option(discord.Attachment,
                                 description="Загрузите изображение (png, jeg, webp, gif)"),
            height: discord.Option(int, description="Высота в процентах (целое число от 0 до 100)",
                                   default=20)
    ):
        private = Setting.get_private(ctx)
        if not ctx.response.is_done():
            await ctx.defer(ephemeral=private)

        embed = Setting.Converter.Png.get_embed()
        embed.color = discord.Color(Setting.get_color(ctx))

        valid_formats = ['png', 'jpeg', 'jpg', 'webp', 'gif']
        file_format = file.filename.lower().split('.')[-1]
        if file_format not in valid_formats:
            embed = discord.Embed(
                title="Ошибка",
                description="Неверный формат файла. Допустимые форматы: png, jpeg, webp, gif.",
                color=Setting.get_color(ctx)
            )
            return [2, embed]

        try:
            file_bytes = await file.read()
            with BytesIO(file_bytes) as byte_stream:
                with Image.open(byte_stream) as image:
                    image = image.convert("RGBA")

                    mask = Image.new("L", image.size, 255)
                    draw = ImageDraw.Draw(mask)

                    # Определяем размеры облачка
                    width_, height_ = image.size
                    cloud_height = int(height_ * height * 0.01)  # Высота облачка (height% от высоты изображения)
                    cloud_width = int(width_ * 1)  # Ширина облачка (100% от ширины изображения)
                    start_x = (width_ - cloud_width) // 2  # Центрируем по горизонтали
                    start_y = 0  # Начинаем с верхнего края изображения

                    # Рисуем форму облачка
                    draw.rectangle([start_x, start_y, start_x + cloud_width, start_y + cloud_height // 2],
                                   fill=0)  # Прямоугольник
                    draw.ellipse([start_x, start_y + cloud_height // 2 - cloud_height // 2,
                                  start_x + cloud_width, start_y + cloud_height], fill=0)  # Полуовал (перевёрнут вниз)

                    # Добавляем стрелочку
                    arrow_tip_x = width_ // 2  # Координаты наконечника стрелки (по центру)
                    arrow_tip_y = cloud_height + int(height_ * 0.05)  # Наконечник стрелки чуть ниже облачка
                    arrow_base_width = int(width_ * 0.1)  # Ширина основания стрелки
                    arrow_base_y = cloud_height  # Верхняя часть основания стрелки

                    # Рисуем стрелочку как треугольник
                    draw.polygon([
                        (arrow_tip_x, arrow_tip_y),  # Наконечник
                        (arrow_tip_x - arrow_base_width // 2, arrow_base_y),  # Левый угол основания
                        (arrow_tip_x + arrow_base_width // 2, arrow_base_y)  # Правый угол основания
                    ], fill=0)

                    alpha = image.getchannel("A")
                    alpha = ImageChops.multiply(alpha, mask)
                    image.putalpha(alpha)

                    result = BytesIO()
                    image.save(result, format="GIF")
                    result.seek(0)

            discord_file = discord.File(fp=result, filename=f"{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.gif")
            embed.set_image(url=f"attachment://{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.gif")
            return [4, embed, discord_file]

        except Exception as e:
            print(f"Ошибка обработки изображения: {e}")
            embed = discord.Embed(
                title="Ошибка",
                description="Произошла ошибка при обработке изображения.",
                color=Setting.get_color(ctx)
            )
            return [2, embed]

    @commands.message_command(
        name="Конвертировать в reply-GIF",
        integration_types=Setting.integration_types,
        contexts=Setting.contexts)
    @Setting.measure_execution_time()
    async def convert_to_reply(
            self,
            ctx: ApplicationContext,
            message: discord.Message,
    ):
        private = Setting.get_private(ctx)
        if not ctx.response.is_done():
            await ctx.defer(ephemeral=private)

        embed = Setting.Converter.Png.get_embed()
        embed.color = discord.Color(Setting.get_color(ctx))

        if not message.attachments:
            embed.description = "В этом сообщении нет вложений."
            return [2, embed]

        valid_formats = ['png', 'jpeg', 'jpg', 'webp', 'gif']
        file = message.attachments[0]
        file_format = file.filename.lower().split('.')[-1]
        if file_format not in valid_formats:
            embed = discord.Embed(
                title="Ошибка",
                description="Неверный формат файла. Допустимые форматы: png, jpeg, webp, gif.",
                color=Setting.get_color(ctx)
            )
            return [2, embed]

        try:
            file_bytes = await file.read()
            with BytesIO(file_bytes) as byte_stream:
                with Image.open(byte_stream) as image:
                    image = image.convert("RGBA")

                    mask = Image.new("L", image.size, 255)
                    draw = ImageDraw.Draw(mask)

                    # Определяем размеры облачка
                    width, height = image.size
                    cloud_height = int(height * 0.2)  # Высота облачка (20% от высоты изображения)
                    cloud_width = int(width * 1)  # Ширина облачка (100% от ширины изображения)
                    start_x = (width - cloud_width) // 2  # Центрируем по горизонтали
                    start_y = 0  # Начинаем с верхнего края изображения

                    # Рисуем форму облачка
                    draw.rectangle([start_x, start_y, start_x + cloud_width, start_y + cloud_height // 2],
                                   fill=0)  # Прямоугольник
                    draw.ellipse([start_x, start_y + cloud_height // 2 - cloud_height // 2,
                                  start_x + cloud_width, start_y + cloud_height], fill=0)  # Полуовал (перевёрнут вниз)

                    # Добавляем стрелочку
                    arrow_tip_x = width // 2  # Координаты наконечника стрелки (по центру)
                    arrow_tip_y = cloud_height + int(height * 0.05)  # Наконечник стрелки чуть ниже облачка
                    arrow_base_width = int(width * 0.1)  # Ширина основания стрелки
                    arrow_base_y = cloud_height  # Верхняя часть основания стрелки

                    # Рисуем стрелочку как треугольник
                    draw.polygon([
                        (arrow_tip_x, arrow_tip_y),  # Наконечник
                        (arrow_tip_x - arrow_base_width // 2, arrow_base_y),  # Левый угол основания
                        (arrow_tip_x + arrow_base_width // 2, arrow_base_y)  # Правый угол основания
                    ], fill=0)

                    alpha = image.getchannel("A")
                    alpha = ImageChops.multiply(alpha, mask)
                    image.putalpha(alpha)

                    result = BytesIO()
                    image.save(result, format="GIF")
                    result.seek(0)

            discord_file = discord.File(fp=result, filename=f"{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.gif")
            embed = discord.Embed(
                title="Обработанное изображение",
                color=Setting.get_color(ctx)
            )
            embed.set_image(url=f"attachment://{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.gif")
            return [4, embed, discord_file]

        except Exception as e:
            print(f"Ошибка обработки изображения: {e}")
            embed = discord.Embed(
                title="Ошибка",
                description="Произошла ошибка при обработке изображения.",
                color=Setting.get_color(ctx)
            )
            return [2, embed]


def setup(bot):
    bot.add_cog(Reply(bot))
