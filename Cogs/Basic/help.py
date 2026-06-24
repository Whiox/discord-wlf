
from discord import ApplicationContext, Embed, SelectOption
from discord.ui import select, View
from discord.ext import commands

from src.settings import Setting, DB, CommandResponse, process_command, process_view

from src.help_content import HELP_SECTIONS


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='help',
        description='Информация о командах бота',
        integration_types=Setting.integration_types,
        contexts=Setting.contexts,
        guild_ids=Setting.guilds_ids
    )
    @process_command()
    async def help(
        self,
        ctx: ApplicationContext
    ) -> CommandResponse:
        embed = Embed()
        embed.title = 'Чтобы узнать подробности выберите нужный вам раздел'

        for section in HELP_SECTIONS.values():
            embed.add_field(name=section.name, value=section.command_list(), inline=False)

        embed.colour = DB.get_color(ctx)

        return CommandResponse(
            embed=embed,
            view=Help.get_view(),
        )


    @staticmethod
    def get_view() -> View:
        options = [
            SelectOption(
                label=section.name,
                value=section_id,
                description=section.description,
            )
            for section_id, section in HELP_SECTIONS.items()
        ]


        class HelpView(View):
            def __init__(self):
                super().__init__(timeout=None)

            @select(
                placeholder="Выберите нужный раздел",
                custom_id="select-help",
                options=options
            )
            @process_view()
            async def select_callback(self, select_menu, interaction) -> CommandResponse:
                section_id = select_menu.values[0]
                section = HELP_SECTIONS[section_id]

                embed = Embed(
                    title=section.name,
                    description=section.full_description(),
                    color=DB.get_color(interaction))

                return CommandResponse(
                    embed=embed,
                )

        return HelpView()


def setup(bot):
    bot.add_cog(Help(bot))