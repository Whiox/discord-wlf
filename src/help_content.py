
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
                    "Конвертирует изображения PNG, JPEG и WebP "
                    "в GIF-файл."
                ),
            ),
            HelpCommand(
                name="png",
                description=(
                    "Конвертирует JPEG, WebP и первый кадр GIF "
                    "в PNG-изображение."
                ),
            ),
            HelpCommand(
                name="reply",
                description=(
                    "Создаёт reply-GIF из изображений PNG, JPEG, WebP "
                    "или GIF."
                ),
            ),
        ),
    ),
}
