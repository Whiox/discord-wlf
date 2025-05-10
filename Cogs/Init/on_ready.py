from discord.ext import commands
from settings import Setting


class OnReadyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(Setting.Basic.Help.get_view())  # Добавляем view
        print(f'We have logged in as {self.bot.user}')

def setup(bot):
    bot.add_cog(OnReadyCog(bot))
