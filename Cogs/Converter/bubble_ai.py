
from discord import ApplicationContext, Embed, Attachment, Option, File, Message
from discord.ext import commands

from io import BytesIO
from target_cloud_detect import Model

from settings import Setting, DB, CommandResponse, measure_execution_time


class BubbleAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.model = Model()

    @commands.slash_command(
        name='bubble_ai',
        description='Добавить пузырь на изображение',
        integration_types=Setting.integration_types,
        contexts=Setting.contexts
    )
    @measure_execution_time()
    async def bubble_ai(
            self,
            ctx: ApplicationContext,
            file: Option(Attachment, description="Загрузите изображение (png, jeg, webp, gif)")
    ):
        private = DB.get_private(ctx)
        if not ctx.response.is_done():
            await ctx.defer(ephemeral=private)

        embed = Embed(title="GIF")
        embed.colour = DB.get_color(ctx)

        valid_formats = ['png', 'jpeg', 'jpg', 'webp', 'gif']
        file_format = file.filename.lower().split('.')[-1]
        if file_format not in valid_formats:
            embed = Embed(
                title="Ошибка",
                description="Неверный формат файла. Допустимые форматы: png, jpeg, webp, gif.",
                color=DB.get_color(ctx)
            )

            return CommandResponse(
                embed=embed,
            )

        try:
            file_bytes = await file.read()
            result = self.model.predict_from_bytes(file_bytes)

            output = BytesIO()
            result.save(output, format="PNG")
            output.seek(0)

            discord_file = File(fp=output, filename=f"{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.gif")
            embed.set_image(url=f"attachment://{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.gif")

            return CommandResponse(
                embed=embed,
                file=discord_file,
            )

        except Exception as e:
            print(f"Ошибка обработки изображения: {e}")
            embed = Embed(
                title="Ошибка",
                description="Произошла ошибка при обработке изображения.",
                color=DB.get_color(ctx)
            )

            return CommandResponse(
                embed=embed,
            )

    @commands.message_command(
        name="Добавить пузырь AI™",
        integration_types=Setting.integration_types,
        contexts=Setting.contexts)
    @measure_execution_time()
    async def bubble_ai_menu(
            self,
            ctx: ApplicationContext,
            message: Message,
    ):
        private = DB.get_private(ctx)
        if not ctx.response.is_done():
            await ctx.defer(ephemeral=private)

        embed = Embed(title="GIF")
        embed.colour = DB.get_color(ctx)

        if not message.attachments:
            embed.description = "В этом сообщении нет вложений."
            return [2, embed]

        valid_formats = ['png', 'jpeg', 'jpg', 'webp', 'gif']
        file = message.attachments[0]
        file_format = file.filename.lower().split('.')[-1]
        if file_format not in valid_formats:
            embed = Embed(
                title="Ошибка",
                description="Неверный формат файла. Допустимые форматы: png, jpeg, webp, gif.",
                color=DB.get_color(ctx)
            )

            return CommandResponse(
                embed=embed,
            )

        try:
            file_bytes = await file.read()
            result = self.model.predict_from_bytes(file_bytes)

            output = BytesIO()
            result.save(output, format="PNG")
            output.seek(0)

            discord_file = File(fp=output, filename=f"{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.gif")
            embed = Embed(
                title="Обработанное изображение",
                color=DB.get_color(ctx)
            )
            embed.set_image(url=f"attachment://{ctx.user.id}_{file.filename.rsplit('.', 1)[0]}.gif")

            return CommandResponse(
                embed=embed,
                file=discord_file
            )

        except Exception as e:
            print(f"Ошибка обработки изображения: {e}")
            embed = Embed(
                title="Ошибка",
                description="Произошла ошибка при обработке изображения.",
                color=DB.get_color(ctx)
            )

            return CommandResponse(
                embed=embed,
            )


def setup(bot):
    bot.add_cog(BubbleAI(bot))
