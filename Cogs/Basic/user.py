
from discord import ApplicationContext, Embed, Option, User
from discord.ext import commands

from settings import Setting, DB, CommandResponse, measure_execution_time


class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='user_info',
        description='Информация о пользователе',
        integration_types=Setting.integration_types,
        contexts=Setting.contexts,
        guild_ids=Setting.guilds_ids
    )
    @measure_execution_time()
    async def user_info(
        self,
        ctx: ApplicationContext,
        user: Option(User, name="пользователь")
    ):
        embed = Embed()

        embed.title = f"Информация о `@{user.name}`"
        embed.description = f"Id - {user.id}"

        embed.add_field(
            name="Дата создания аккаунта", inline=False,
            value=f"Аккаунт был создан: <t:{int(user.created_at.timestamp())}:F>"
        )

        if ctx.guild:
            member = ctx.guild.get_member(user.id)
            if member and member.joined_at:
                embed.add_field(
                    name="Дата вступления на сервер",
                    value=f"Присоединился: <t:{int(member.joined_at.timestamp())}:F>",
                    inline=False
                )

        embed.add_field(
            name="Дата первого использования бота",
            value=f"Первое использование: <t:{int(DB.get_first_command(ctx))}:F>",
            inline=False
        )


        avatar_url = user.avatar.url if user.avatar \
            else f"https://cdn.discordapp.com/embed/avatars/{int(user.id) % 5}.png"
        fetched_user = await self.bot.fetch_user(user.id)

        if fetched_user.banner:
            embed.set_image(url=fetched_user.banner.url)

        embed.set_thumbnail(url=avatar_url)
        embed.colour = DB.get_color(ctx)

        return CommandResponse(
            embed=embed,
        )


def setup(bot):
    bot.add_cog(UserInfo(bot))