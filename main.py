import os
import discord
from dotenv import load_dotenv


def main():
    bot = discord.Bot(intents=discord.Intents.default())

    for folderName in os.listdir('./Cogs'): # Список папок в Cogs
        for fileName in os.listdir(f'./Cogs/{folderName}'): # Список файлов в Cogs/...
            if fileName.endswith('.py') and not fileName in ['util.py', 'error.py']: # Все .py файлы в Cogs/.../.py
                bot.load_extension(f'Cogs.{folderName}.{fileName[:-3]}')
                print(f" - Cogs.{folderName}.{fileName[:-3]} loaded")

    load_dotenv()
    bot.run(os.getenv('TOKEN'))


if __name__ == '__main__':
    main()
