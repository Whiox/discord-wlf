import os

from discord import Bot, Intents
from dotenv import load_dotenv

from settings import DB


def main():
    DB()

    bot = Bot(intents=Intents.default())

    for folderName in os.listdir('./Cogs'):
        for fileName in os.listdir(f'./Cogs/{folderName}'):
            if fileName.endswith('.py') and not fileName in ['util.py', 'error.py']:
                bot.load_extension(f'Cogs.{folderName}.{fileName[:-3]}')
                print(f" - Cogs.{folderName}.{fileName[:-3]} loaded")

    load_dotenv()
    bot.run(os.getenv('TOKEN'))


if __name__ == '__main__':
    main()
