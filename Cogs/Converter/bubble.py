
from discord import ApplicationContext, Embed, Attachment, Option, Message, File
from discord.ext import commands

from io import BytesIO
from PIL import Image, ImageDraw, ImageChops

from src.settings import Setting, DB, CommandResponse, process_command
from src.file_converting import BaseConverter


class Bubble(commands.Cog, BaseConverter):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='bubble',
        description='Добавить пузырь на изображение',
        integration_types=Setting.integration_types,
        contexts=Setting.contexts
    )
    @process_command()
    async def bubble(
            self,
            ctx: ApplicationContext,
            file: Option(Attachment, description="Загрузите изображение (png, jeg, webp, gif)"),
            height: Option(int, description="Высота в процентах (целое число от 0 до 100)", default=20)
    ):
        is_valid = self.check_file_format(file) # CommandResponse | True
        if is_valid is not True:
            return is_valid

        file_bytes = await file.read()
        result = self.add_bubble(file_bytes, height)

        discord_file = File(fp=result, filename=f"{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.gif")
        image_url = f"attachment://{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.gif"
        embed = Embed(
            title="bubble GIF",
            image=image_url,
        )

        return CommandResponse(
            embed=embed,
            file=discord_file,
        )

    @commands.message_command(
        name="Добавить пузырь на изображение",
        integration_types=Setting.integration_types,
        contexts=Setting.contexts)
    @process_command()
    async def bubble_menu(
            self,
            ctx: ApplicationContext,
            message: Message,
    ):
        if not message.attachments:
            embed = Embed(
                title="bubble GIF",
                description = "В этом сообщении нет вложений.",
            )

            return CommandResponse(
                embed=embed,
            )

        file = message.attachments[0]
        is_valid = self.check_file_format(file)  # CommandResponse | True
        if is_valid is not True:
            return is_valid

        file_bytes = await file.read()
        result = self.add_bubble(file_bytes)

        discord_file = File(fp=result, filename=f"{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.gif")
        image_url = f"attachment://{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.gif"
        embed = Embed(
            title="Обработанное изображение",
            image=image_url,
        )

        return CommandResponse(
            embed=embed,
            file=discord_file,
        )



    @staticmethod
    def add_bubble(file_bytes, height = 20):
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
                return result


def setup(bot):
    bot.add_cog(Bubble(bot))
