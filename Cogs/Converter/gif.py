import discord
from discord.ext import commands
from discord import ApplicationContext
from settings import Setting
from PIL import Image
from io import BytesIO


class Gif(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='gif',
        description='Конвертируйте изображение в формат GIF',
        integration_types=Setting.integration_types,
        contexts=Setting.contexts
    )
    @Setting.measure_execution_time()
    async def gif(
            self,
            ctx: ApplicationContext,
            file: discord.Option(discord.Attachment,
                                 description="Выберите изображение для конвертации (png, jpeg, webp)")
    ):
        private = Setting.get_private(ctx)
        if not ctx.response.is_done():
            await ctx.defer(ephemeral=private)
        embed = Setting.Converter.Gif.get_embed()
        embed.color = discord.Color(Setting.get_color(ctx))

        valid_formats = ['png', 'jpeg', 'jpg', 'webp']
        if not file.filename.lower().split('.')[-1] in valid_formats:
            embed.description = "Неверный формат файла. Допустимые форматы: png, jpeg, webp."
            return [2, embed]

        try:
            file_bytes = await file.read()
            with BytesIO(file_bytes) as byte_stream:
                with Image.open(byte_stream) as image:
                    result = BytesIO()
                    image.save(result, format="GIF")
                    result.seek(0)

            discord_file = discord.File(fp=result, filename=f"{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.gif")
            embed.description = "Успешно конвертировано в GIF!"
            embed.set_image(url=f"attachment://{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.gif")
            return [4, embed, discord_file]

        except UnicodeDecodeError as e:
            print(f"Ошибка кодировки: {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    @commands.message_command(
        name="Конвертация в GIF",
        integration_types=Setting.integration_types,
        contexts=Setting.contexts
    )
    @Setting.measure_execution_time()
    async def convert_to_gif(self, ctx: discord.ApplicationContext, message: discord.Message):
        private = Setting.get_private(ctx)
        if not ctx.response.is_done():
            await ctx.defer(ephemeral=private)

        embed = Setting.Converter.Gif.get_embed()
        embed.color = discord.Color(Setting.get_color(ctx))

        if not message.attachments:
            embed.description = "В этом сообщении нет вложений."
            return [2, embed]

        valid_formats = ['png', 'jpeg', 'jpg', 'webp']
        file = message.attachments[0]
        file_format = file.filename.lower().split('.')[-1]
        if file_format not in valid_formats:
            embed.description = "Неверный формат файла. Допустимые форматы: png, jpeg, webp."
            return [2, embed]

        try:
            file_bytes = await file.read()
            with BytesIO(file_bytes) as byte_stream:
                with Image.open(byte_stream) as image:
                    if image.mode in ("RGBA", "LA"):
                        image = image.convert("RGB")

                    result = BytesIO()
                    image.save(result, format="GIF")
                    result.seek(0)

            discord_file = discord.File(fp=result,
                                        filename=f"{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.gif")
            embed.set_image(url=f"attachment://{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.gif")
            return [4, embed, discord_file]

        except Exception as e:
            print(f"Ошибка при обработке файла: {e}")
            embed.description = "Произошла ошибка при обработке файла."
            return [2, embed]

def setup(bot):
    bot.add_cog(Gif(bot))
