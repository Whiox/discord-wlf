
from discord import Embed

from src.settings import CommandResponse


VALID_FORMATS = ['png', 'jpeg', 'jpg', 'webp', 'gif']


class BaseConverter:
    def check_file_format(self, file) -> bool | CommandResponse:
        file_format = file.filename.lower().split('.')[-1]
        if file_format not in VALID_FORMATS:
            embed = Embed(
                title="Ошибка",
                description="Неверный формат файла. Допустимые форматы: png, jpeg, webp, gif.",
            )

            return CommandResponse(
                embed=embed,
            )

        return True
