import random
from abc import ABC, abstractmethod

from settings import Setting

from discord import Embed


class AbstractLogic(ABC):
    def get_title(self) -> str:
        return ""

    def get_description(self):
        return ""

    def get_image(self):
        return ""

    @abstractmethod
    def get_embed(self, ctx):
        return Embed(
            title=self.get_title(),
            description=self.get_description(),
            image=self.get_image(),
            color=Setting.get_color(ctx)
        )
