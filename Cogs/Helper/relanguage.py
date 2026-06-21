
from discord import ApplicationContext, Embed, Attachment, Option, File, Message
from discord.ext import commands

from settings import Setting, DB


class ReLanguage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.EN_TO_RU = {
            "`": "ё", "~": "Ё",
            "q": "й", "w": "ц", "e": "у", "r": "к", "t": "е", "y": "н", "u": "г", "i": "ш", "o": "щ", "p": "з",
            "[": "х", "]": "ъ",
            "a": "ф", "s": "ы", "d": "в", "f": "а", "g": "п", "h": "р", "j": "о", "k": "л", "l": "д", ";": "ж",
            "'": "э",
            "z": "я", "x": "ч", "c": "с", "v": "м", "b": "и", "n": "т", "m": "ь", ",": "б", ".": "ю", "/": ".",
        }

        self.EN_TO_RU.update({k.upper(): v.upper() for k, v in self.EN_TO_RU.items()})

        self.RU_TO_EN = {v: k for k, v in self.EN_TO_RU.items()}

    def convert(self, text: str, mapping: dict) -> str:
        return ''.join(mapping.get(ch, ch) for ch in text)

    @commands.slash_command(
        name='relanguage',
        description='Поменяйте раскладку символов',
        integration_types=Setting.integration_types,
        contexts=Setting.contexts
    )
    @Setting.measure_execution_time()
    async def relanguage(
            self,
            ctx: ApplicationContext,
            text: str,
    ):
        private = DB.get_private(ctx)
        if not ctx.response.is_done():
            await ctx.defer(ephemeral=private)
        embed = Embed()
        embed.colour = DB.get_color(ctx)

        if any('а' <= ch <= 'я' or 'А' <= ch <= 'Я' or ch in "ёЁ" for ch in text):
            result = self.convert(text, self.RU_TO_EN)
        else:
            result = self.convert(text, self.EN_TO_RU)

        embed.title = result

        return [2, embed]



    @commands.message_command(
        name="Поменять раскладку",
        integration_types=Setting.integration_types,
        contexts=Setting.contexts
    )
    async def rel(self, ctx: ApplicationContext, message: Message):
        private = DB.get_private(ctx)
        if not ctx.response.is_done():
            await ctx.defer(ephemeral=private)
        embed = Embed()
        embed.colour = DB.get_color(ctx)

        text = message.content

        if any('а' <= ch <= 'я' or 'А' <= ch <= 'Я' or ch in "ёЁ" for ch in text):
            result = self.convert(text, self.RU_TO_EN)
        else:
            result = self.convert(text, self.EN_TO_RU)

        embed.title = result

        await ctx.followup.send(embed=embed, ephemeral=private)


def setup(bot):
    bot.add_cog(ReLanguage(bot))
