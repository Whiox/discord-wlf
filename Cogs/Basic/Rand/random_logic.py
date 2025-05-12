from discord import Embed

from logic import AbstractLogic
from random import choice

from settings import Setting

from Cogs.Basic.Rand import random_text as rt


class RandomLogic():
    def get_title(self, result):
        if result:
            return choice(rt.good_titles)
        return choice(rt.bad_titles)

    def get_description(self, result):
        if result:
            return choice(rt.good_descriptions)
        return choice(rt.bad_description)

    def get_image(self, result):
        if result:
            return choice(rt.good_images)
        return choice(rt.bad_images)

    def get_embed(self, ctx):
        result = choice([True, False])

        return Embed(
            title=self.get_title(result),
            description=self.get_description(result),
            image=self.get_image(result),
            color=Setting.get_color(ctx)
        )
