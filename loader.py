from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from data import config
# Создаем объект бота
bot = Bot(config.BOT_TOKEN)

# Создаем объект диспетчера
dp = Dispatcher(bot, storage=MemoryStorage())