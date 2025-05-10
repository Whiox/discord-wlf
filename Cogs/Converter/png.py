import discord
from discord.ext import commands
from discord import ApplicationContext
from settings import Setting
from PIL import Image
from io import BytesIO


class Png(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='png',
        description='Конвертируйте фаил в png',
        integration_types=Setting.integration_types,
        contexts=Setting.contexts
    )
    @Setting.measure_execution_time()
    async def png(
            self,
            ctx: ApplicationContext,
            file: discord.Option(discord.Attachment,
                                 description="Выберите изображение для конвертации (jpeg, webp, gif)")
    ):
        private = Setting.get_private(ctx)
        if not ctx.response.is_done():
            await ctx.defer(ephemeral=private)
        embed = Setting.Converter.Png.get_embed()
        embed.color = discord.Color(Setting.get_color(ctx))

        valid_formats = ['jpeg', 'jpg', 'webp', 'gif']
        if not file.filename.lower().split('.')[-1] in valid_formats:
            embed.description = "Неверный формат файла. Допустимые форматы: jpeg, webp, gif."
            return [2, embed]

        try:
            file_bytes = await file.read()
            with BytesIO(file_bytes) as byte_stream:
                with Image.open(byte_stream) as image:
                    if image.format == 'GIF':
                        image = image.convert('RGB')
                    else:
                        image = image.convert('RGBA')
                    result = BytesIO()
                    image.save(result, format="PNG")
                    result.seek(0)

            discord_file = discord.File(fp=result, filename=f"{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.png")
            embed.description = "Успешно конвертировано в PNG!"
            embed.set_image(url=f"attachment://{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.png")
            return [4, embed, discord_file]

        except UnicodeDecodeError as e:
            print(f"Ошибка кодировки: {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    @commands.message_command(
        name="Конвертация в PNG",
        integration_types=Setting.integration_types,
        contexts=Setting.contexts
    )
    async def convert_to_png(self, ctx: discord.ApplicationContext, message: discord.Message):
        private = Setting.get_private(ctx)
        if not ctx.response.is_done():
            await ctx.defer(ephemeral=private)
        embed = Setting.Converter.Png.get_embed()
        embed.color = discord.Color(Setting.get_color(ctx))

        if not message.attachments:
            embed.description = "В этом сообщении нет вложений."
            return [2, embed]

        valid_formats = ['jpeg', 'jpg', 'webp', 'gif']
        file = message.attachments[0]
        file_format = file.filename.lower().split('.')[-1]
        if file_format not in valid_formats:
            embed.description = "Неверный формат файла. Допустимые форматы: jpeg, webp, gif."
            return [2, embed]

        try:
            file_bytes = await file.read()
            with BytesIO(file_bytes) as byte_stream:
                with Image.open(byte_stream) as image:
                    if image.format == 'GIF':
                        image = image.convert('RGB')
                    else:
                        image = image.convert('RGBA')
                    result = BytesIO()
                    image.save(result, format="PNG")
                    result.seek(0)

            discord_file = discord.File(fp=result, filename=f"{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.png")
            embed.description = "Успешно конвертировано в PNG!"
            embed.set_image(url=f"attachment://{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.png")
            return [4, embed, discord_file]

        except Exception as e:
            print(f"Ошибка при обработке файла: {e}")
            embed.description = "Произошла ошибка при обработке файла."
            return [2, embed]


def setup(bot):
    bot.add_cog(Png(bot))
