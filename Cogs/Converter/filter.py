
from discord import ApplicationContext, Embed, Attachment, Option, File, Message
from discord.ext import commands

from io import BytesIO
from PIL import Image, ImageOps
from PIL.ImageFilter import GaussianBlur

from src.settings import Setting, CommandResponse, process_command
from src.file_converting import BaseConverter
from src.filter_content import FilterOptions


class Filter(commands.Cog, BaseConverter):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='filter',
        description='Добавить фильтры на изображение',
        integration_types=Setting.integration_types,
        contexts=Setting.contexts
    )
    @process_command()
    async def filter(
            self,
            ctx: ApplicationContext,
            file: Option(
                Attachment,
                description="Выберите изображение",
            ),
            output: Option(
                str,
                description="Формат результата",
                choices=["png", "gif"],
                default="png",
            ),
            blur: Option(
                bool,
                description="Добавить размытие",
                default=False,
            ),
            black_white: Option(
                bool,
                description="Сделать изображение чёрно-белым",
                default=False,
            ),
            pixelate: Option(
                bool,
                description="Добавить пикселизацию",
                default=False,
            ),
            invert: Option(
                bool,
                description="Инвертировать цвета",
                default=False,
            ),
    ):
        is_valid = self.check_file_format(file)  # CommandResponse | True
        if is_valid is not True:
            return is_valid

        options = FilterOptions(
            output=output,
            blur=blur,
            black_white=black_white,
            pixelate=pixelate,
            invert=invert,
        )

        return await self.process_file(file, ctx, options)

    async def process_file(self, file, ctx, options: FilterOptions):
        file_bytes = await file.read()
        with BytesIO(file_bytes) as byte_stream:
            with Image.open(byte_stream) as image:
                image = image.convert('RGBA')
                if options.blur:
                    image = image.filter(GaussianBlur(radius=30))
                if options.black_white:
                    image = image.convert('L')
                if options.pixelate:
                    w, h = image.size
                    image = image.resize((w // 16, h // 16), Image.Resampling.LANCZOS)
                    image = image.resize((w, h), Image.Resampling.NEAREST)
                if options.invert:
                    image = image.convert('RGB')
                    image = ImageOps.invert(image)
                    image = image.convert('RGBA')
                result = BytesIO()
                image.save(result, format=options.output.upper())
                result.seek(0)

        discord_file = File(fp=result, filename=f"{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.{options.output}")
        image_url = f"attachment://{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.{options.output}"
        embed = Embed(
            title=options.output.upper(),
            image=image_url,
        )

        return CommandResponse(
            embed=embed,
            file=discord_file,
        )


def setup(bot):
    bot.add_cog(Filter(bot))
