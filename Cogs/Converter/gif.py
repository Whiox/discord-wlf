
from discord import ApplicationContext, Embed, Attachment, Option, File, Message
from discord.ext import commands

from PIL import Image
from io import BytesIO

from src.settings import Setting, DB, CommandResponse, process_command
from src.file_converting import BaseConverter


class Gif(commands.Cog, BaseConverter):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='gif',
        description='Конвертируйте изображение в формат GIF',
        integration_types=Setting.integration_types,
        contexts=Setting.contexts
    )
    @process_command()
    async def gif(
            self,
            ctx: ApplicationContext,
            file: Option(Attachment, description="Выберите изображение для конвертации (png, jpeg, webp)")
    ):
        is_valid = self.check_file_format(file)  # CommandResponse | True
        if is_valid is not True:
            return is_valid

        file_bytes = await file.read()
        with BytesIO(file_bytes) as byte_stream:
            with Image.open(byte_stream) as image:
                result = BytesIO()
                image.save(result, format="GIF")
                result.seek(0)

        discord_file = File(fp=result, filename=f"{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.gif")
        image_url = f"attachment://{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.gif"
        embed = Embed(
            title="GIF",
            image=image_url,
        )

        return CommandResponse(
            embed=embed,
            file=discord_file,
        )

    @commands.message_command(
        name="Конвертация в GIF",
        integration_types=Setting.integration_types,
        contexts=Setting.contexts
    )
    @process_command()
    async def convert_to_gif(self, ctx: ApplicationContext, message: Message):
        if not message.attachments:
            embed = Embed(
                title="GIF",
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
        with BytesIO(file_bytes) as byte_stream:
            with Image.open(byte_stream) as image:
                result = BytesIO()
                image.save(result, format="GIF")
                result.seek(0)

        discord_file = File(fp=result, filename=f"{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.gif")
        image_url = f"attachment://{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.gif"
        embed = Embed(
            title="GIF",
            image=image_url,
        )

        return CommandResponse(
            embed=embed,
            file=discord_file,
        )

def setup(bot):
    bot.add_cog(Gif(bot))
