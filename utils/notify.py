import logging
from data.config import ADMINS
from aiogram import Dispatcher

#Оповещение админов о запуске бота
async def on_startup_notify(dp: Dispatcher):
    await dp.bot.delete_my_commands()
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Бот Запущен")
            logging.info("The bot was launched successfully.")
        except Exception as err:
            logging.exception(err)