
import os
import threading

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

logging.getLogger("tensorflow").setLevel(logging.ERROR)

from discord import Bot, Intents
from dotenv import load_dotenv

from src.settings import DB
from src.http_server import start_http_server


def setup_logging() -> None:
    if not Path("logs").exists():
        Path("logs").mkdir()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        handlers=[
            RotatingFileHandler("logs/bot.log", maxBytes=5 * 1024 * 1024, backupCount=3),
            logging.StreamHandler(),
        ]
    )


def main() -> None:
    setup_logging()
    DB()

    logger = logging.getLogger(__name__)

    for folderName in os.listdir('./Cogs'):
        for fileName in os.listdir(f'./Cogs/{folderName}'):
            if fileName.endswith('.py') and not fileName in ['util.py', 'error.py']:
                bot.load_extension(f'Cogs.{folderName}.{fileName[:-3]}')
                logger.info(f" - Cogs.{folderName}.{fileName[:-3]} loaded")

    load_dotenv()
    bot.run(os.getenv('TOKEN'))


if __name__ == '__main__':
    bot = Bot(intents=Intents.default())

    threading.Thread(
        target=start_http_server,
        kwargs={
            "port": int(os.getenv("HTTP_SERVER_PORT", "8081")),
            "bot": bot,
        },
        daemon=True,
    ).start()

    main()
