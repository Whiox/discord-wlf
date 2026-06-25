
from discord import ApplicationContext, Embed, Attachment, Option, File, Message
from discord.ext import commands

from io import BytesIO
from PIL import Image

from src.settings import Setting, CommandResponse, process_command
from src.file_converting import BaseConverter


class Png(commands.Cog, BaseConverter):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='png',
        description='Конвертируйте файл в png',
        integration_types=Setting.integration_types,
        contexts=Setting.contexts
    )
    @process_command()
    async def png(
            self,
            ctx: ApplicationContext,
            file: Option(Attachment, description="Выберите изображение для конвертации (jpeg, webp, gif)")
    ):
        is_valid = self.check_file_format(file)  # CommandResponse | True
        if is_valid is not True:
            return is_valid

        return await self.process_file(file, ctx)

    @commands.message_command(
        name="Конвертация в PNG",
        integration_types=Setting.integration_types,
        contexts=Setting.contexts
    )
    @process_command()
    async def convert_to_png(self, ctx: ApplicationContext, message: Message):
        if not message.attachments:
            embed = Embed(
                title="PNG",
                description = "В этом сообщении нет вложений.",
            )

            return CommandResponse(
                embed=embed,
            )

        file = message.attachments[0]
        is_valid = self.check_file_format(file)  # CommandResponse | True
        if is_valid is not True:
            return is_valid

        return await self.process_file(file, ctx)


    async def process_file(self, file, ctx):
        file_bytes = await file.read()
        with BytesIO(file_bytes) as byte_stream:
            with Image.open(byte_stream) as image:
                image = image.convert('RGBA')
                result = BytesIO()
                image.save(result, format="PNG")
                result.seek(0)

        discord_file = File(fp=result, filename=f"{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.png")
        image_url = f"attachment://{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.png"
        embed = Embed(
            title="PNG",
            image=image_url,
        )

        return CommandResponse(
            embed=embed,
            file=discord_file,
        )


def setup(bot):
    bot.add_cog(Png(bot))
