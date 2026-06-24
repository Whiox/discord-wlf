
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class HelpCommand:
    name: str
    description: str


@dataclass(frozen=True, slots=True)
class HelpSection:
    name: str
    description: str
    commands: tuple[HelpCommand, ...]

    def command_list(self) -> str:
        return ", ".join(f"`{command.name}`" for command in self.commands)

    def full_description(self) -> str:
        return "\n\n".join(f"`{command.name}`\n{command.description}" for command in self.commands)


HELP_SECTIONS = {
    "basic": HelpSection(
        name="Basic",
        description="Получить информацию о базовых функциях",
        commands=(
            HelpCommand(
                name="help",
                description="Выводит сообщение с выпадающим списком команд.",
            ),
            HelpCommand(
                name="user",
                description=(
                    "Выводит информацию о пользователе: аватар, баннер, "
                    "ID и дату регистрации."
                ),
            ),
            HelpCommand(
                name="ping",
                description=(
                    "Проверяет работоспособность бота и соединение "
                    "с базой данных."
                ),
            ),
            HelpCommand(
                name="color",
                description=(
                    "Изменяет цвет Embed-сообщений. Можно выбрать готовый "
                    "цвет или указать собственный HEX-код."
                ),
            ),
            HelpCommand(
                name="mode",
                description=(
                    "Изменяет настройки приватности ответов бота."
                ),
            ),
        ),
    ),

    "converter": HelpSection(
        name="Converter",
        description="Получить информацию о функциях конвертации",
        commands=(
            HelpCommand(
                name="gif",
                description=(
                    "Конвертирует из PNG, JPEG, WebP GIF."
                    "в GIF-файл."
                ),
            ),
            HelpCommand(
                name="png",
                description=(
                    "Конвертирует из PNG, JPEG, WebP GIF."
                    "в PNG-изображение."
                ),
            ),
            HelpCommand(
                name="bubble",
                description=(
                    "Создаёт bubble GIF из PNG, JPEG, WebP GIF."
                ),
            ),
            HelpCommand(
                name="bubble AI™",
                description=(
                    "Создаёт bubble AI™ GIF из PNG, JPEG, WebP GIF при помощи нейросети."
                ),
            ),
        ),
    ),

    "helper": HelpSection(
        name="Helper",
        description="Получить информацию о вспомогательных функциях",
        commands=(
            HelpCommand(
                name="relanguage",
                description=(
                    "Поменяет раскладку текста (рус -> англ или англ -> рус)."
                ),
            ),
        ),
    ),
}
