
import logging

from discord.ext import commands

from Cogs.Basic.help import Help


logger = logging.getLogger(__name__)


class OnReadyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(Help.get_view())  # Добавляем view
        logger.info(f'We have logged in as {self.bot.user}')
        print(f'We have logged in as {self.bot.user}')

def setup(bot):
    bot.add_cog(OnReadyCog(bot))
