from discord import ApplicationContext
from settings import Setting
from discord.ext import commands

import random

from logic import AbstractLogic


class RandomLogic(AbstractLogic):
    def get_title(self):
        titles = [
            "Вам пизда черти ебаные",
            "Играйте пб умнички ;3"
        ]

        return random.choice(titles)

    def get_description(self):
        descriptions = [
            "(Даже не пытайтесь дебики)",
            "(Попробуйте, хуже не будет ;3)"
        ]

        return random.choice(descriptions)

    def get_image(self):
        images = [
            'https://cdn.discordapp.com/attachments/1266472308235571261/1309271448094773299/'
            'a922aa26e575735d59359ce3d3ab6cf9.png?ex=6740f98e&is=673fa80e&hm=73d524bae14997a'
            'c28a0f5a2a673e5cce3ad7765a0365743043c20b9446914fc&',

            'https://cdn.discordapp.com/attachments/1101524758824230935/1371488190891950120/'
            'image.png?ex=68235169&is=6821ffe9&hm=0e21de457bf4c13466a6cf4129843ba8023ab2313f'
            'da5fe585e8a178cbca1ac1&'
        ]

        return random.choice(images)


class Rand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='rand',
        description='Узнайте ваш таинственный исход на пб',
        integration_types=Setting.integration_types,
        contexts=Setting.contexts,
        guild_ids=Setting.guilds_ids
    )
    @Setting.measure_execution_time()
    async def rand(
        self,
        ctx: ApplicationContext
    ):
        embed = RandomLogic().get_embed(ctx)
        return [2, embed]


def setup(bot):
    bot.add_cog(Rand(bot))
