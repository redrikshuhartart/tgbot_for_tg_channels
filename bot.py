import logging
from aiogram.utils import executor
import sqlite3
from loader import dp, bot
from utils.notify import on_startup_notify

from handlers import handlers


# Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup_notify)
