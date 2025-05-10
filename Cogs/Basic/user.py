import discord
from settings import Setting
from discord import ApplicationContext
from discord.ext import commands


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='user',
        description='Информация о пользователе',
        integration_types=Setting.integration_types,
        contexts=Setting.contexts,
        guild_ids=Setting.guilds_ids
    )
    @Setting.measure_execution_time()
    async def user(
        self,
        ctx: ApplicationContext,
        user: discord.Option(discord.User, name="пользователь")
    ):
        embed = Setting.Basic.User.get_embed()

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
            value=f"Первое использование: <t:{int(Setting.get_first_command(ctx))}:F>",
            inline=False
        )


        avatar_url = user.avatar.url if user.avatar \
            else f"https://cdn.discordapp.com/embed/avatars/{int(user.id) % 5}.png"
        fetched_user = await self.bot.fetch_user(user.id)

        if fetched_user.banner:
            embed.set_image(url=fetched_user.banner.url)

        embed.set_thumbnail(url=avatar_url)
        embed.color = discord.Color(Setting.get_color(ctx))

        return [2, embed]


def setup(bot):
    bot.add_cog(User(bot))