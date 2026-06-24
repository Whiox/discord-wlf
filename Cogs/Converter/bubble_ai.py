
from discord import ApplicationContext, Embed, Attachment, Option, File, Message
from discord.ext import commands

from io import BytesIO
from target_cloud_detect import Model

from src.settings import Setting, CommandResponse, process_command
from src.file_converting import BaseConverter


class BubbleAI(commands.Cog, BaseConverter):
    def __init__(self, bot):
        self.bot = bot
        self.model = Model()

    @commands.slash_command(
        name='bubble_ai',
        description='Добавить пузырь на изображение',
        integration_types=Setting.integration_types,
        contexts=Setting.contexts
    )
    @process_command()
    async def bubble_ai(
            self,
            ctx: ApplicationContext,
            file: Option(Attachment, description="Загрузите изображение (png, jeg, webp, gif)")
    ):
        is_valid = self.check_file_format(file)  # CommandResponse | True
        if is_valid is not True:
            return is_valid

        file_bytes = await file.read()
        result = self.model.predict_from_bytes(file_bytes)

        output = BytesIO()
        result.save(output, format="PNG")
        output.seek(0)

        discord_file = File(fp=output, filename=f"{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.gif")
        image_url = f"attachment://{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.gif"
        embed = Embed(
            title="bubble AI™ GIF",
            image=image_url,
        )

        return CommandResponse(
            embed=embed,
            file=discord_file,
        )


    @commands.message_command(
        name="Добавить пузырь AI™",
        integration_types=Setting.integration_types,
        contexts=Setting.contexts)
    @process_command()
    async def bubble_ai_menu(
            self,
            ctx: ApplicationContext,
            message: Message,
    ):
        if not message.attachments:
            embed = Embed(
                title="bubble AI™ GIF",
                description="В этом сообщении нет вложений.",
            )

            return CommandResponse(
                embed=embed,
            )

        file = message.attachments[0]
        is_valid = self.check_file_format(file)  # CommandResponse | True
        if is_valid is not True:
            return is_valid

        file_bytes = await file.read()
        result = self.model.predict_from_bytes(file_bytes)

        output = BytesIO()
        result.save(output, format="PNG")
        output.seek(0)

        discord_file = File(fp=output, filename=f"{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.gif")
        image_url = f"attachment://{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.gif"
        embed = Embed(
            title="bubble AI™ GIF",
            image=image_url,
        )

        return CommandResponse(
            embed=embed,
            file=discord_file,
        )


def setup(bot):
    bot.add_cog(BubbleAI(bot))
