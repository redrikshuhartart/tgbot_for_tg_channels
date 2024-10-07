import logging
from aiogram.dispatcher import FSMContext
from aiogram import Bot, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Command
from db import Database
from loader import dp, bot
import random
from data import config
from keyboards.keyboards import keyboard_admin_menu, remove_keyboard


VIDEO_FILE = "./content/videos/video_file.mp4"
AUDIO_FILE = "./content/audios/audio_file.ogg"
PHOTO_FILE = "./content/photos/photo_file.png"
CAPTION_TEXT = "Прими участие в розыгрыше"
INLINE_KEYBOARD_CAPTION = "Участвовать в розыгрыше"
SWITCH = "VIDEO"
DB_NAME = "raffle.db"

#--------------------------------------------
class ButtonState(StatesGroup):
    postCaptionButton = State()
    inlinePostButton = State()

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    logging.info(f"User {message.from_user.id} clicked START")
    remove_keyboard
    if str(message.from_user.id) in config.ADMINS:
        await message.reply("Добро пожаловать. Выберите действие.", reply_markup=keyboard_admin_menu, parse_mode='HTML') #
    else:
        await message.reply("Шла Саша по шоссе и сосала сушку...")

# Обработчик команды /random_user
@dp.message_handler(commands=['random_user'])
async def send_random_user(message: types.Message):
    logging.info(f"User {message.from_user.id} clicked RANDOM_USER")
    remove_keyboard
    if str(message.from_user.id) in config.ADMINS:
        random_user = random.choice(Database(DB_NAME).selectAll())
        await message.reply(f"Рандомный подписчик: id - {random_user[0]} username - {random_user[1]}",
                            reply_markup=keyboard_admin_menu,  parse_mode='HTML')

# Обработчик команды !Отправить сообщение
@dp.message_handler(regexp=r'!Отправить сообщение')
async def send_message_to_channel(message: types.Message):
    if str(message.from_user.id) in config.ADMINS:        
        logging.info(f"User {message.from_user.id} clicked !SEND_MESSAGE")
        # Создаем кнопку "Участвовать в розыгрыше"
        button = types.InlineKeyboardButton(text=INLINE_KEYBOARD_CAPTION, callback_data="participate")
        # Создаем объект клавиатуры и добавляем кнопку
        keyboard = types.InlineKeyboardMarkup().add(button)
        # Отправляем сообщение от имени канала с кнопкой
        if SWITCH == "PHOTO":
            logging.info(f"SWITCH = PHOTO")
            with open(PHOTO_FILE, 'rb') as photo:  
                await bot.send_photo(config.TARGET_CHANNEl, photo=photo, caption=CAPTION_TEXT, reply_markup=keyboard, parse_mode='HTML') 
        if SWITCH == "VIDEO":
            logging.info(f"SWItCH = VIDEO")
            with open(VIDEO_FILE, 'rb') as video:
                await bot.send_video(config.TARGET_CHANNEl, video=video, caption=CAPTION_TEXT, reply_markup=keyboard, parse_mode='HTML')
        if SWITCH == "AUDIO":
            logging.info(f"SWITCH = AUDIO")
            with open (AUDIO_FILE, 'rb') as audio:
                await bot.send_audio(config.TARGET_CHANNEl, audio=audio, caption=CAPTION_TEXT, reply_markup=keyboard, parse_mode='HTML')

# Обработчик команды !Отправить тест сообщение
@dp.message_handler(regexp=r'!Отправить тест сообщение')
async def send_message_to_channel(message: types.Message):
    if str(message.from_user.id) in config.ADMINS:
        logging.info(f"User {message.from_user.id} clicked SEND_TEST_MESSAGE")
        # Создаем кнопку "Участвовать в розыгрыше"
        button = types.InlineKeyboardButton(text=INLINE_KEYBOARD_CAPTION, callback_data="participate")
        # Создаем объект клавиатуры и добавляем кнопку
        keyboard = types.InlineKeyboardMarkup().add(button)
        # Отправляем сообщение от имени канала с кнопкой
        if SWITCH == "PHOTO":
            logging.info(f"SWITCH = PHOTO")
            with open(PHOTO_FILE, 'rb') as photo:  
                await bot.send_photo(config.TEST_CHANNEL, photo=photo, caption=CAPTION_TEXT, reply_markup=keyboard, parse_mode='HTML') 
        if SWITCH == "VIDEO":
            logging.info(f"SWITCH = VIDEO")
            with open(VIDEO_FILE, 'rb') as video:
                await bot.send_video(config.TEST_CHANNEL, video=video, caption=CAPTION_TEXT, reply_markup=keyboard, parse_mode='HTML')
        if SWITCH == "AUDIO":
            logging.info(f"SWITCH = AUDIO")
            with open (AUDIO_FILE, 'rb') as audio:
                await bot.send_audio(config.TEST_CHANNEL, audio=audio, caption=CAPTION_TEXT, reply_markup=keyboard, parse_mode='HTML')


# Обработчик нажатия на кнопку "Участвовать в розыгрыше"
@dp.callback_query_handler(lambda c: c.data == 'participate')
async def participate_in_raffle(callback_query: types.CallbackQuery):
    # Отправляем сообщение пользователю о том, что он участвует в розыгрыше
    answers = []
    for channel in config.CHANNELS:
        answer = await bot.get_chat_member(chat_id=f'{channel}', user_id=f'{callback_query.from_user.id}')
        answers.append(answer.is_chat_member())
    if all(answers):
        print(Database(DB_NAME).checkUserInDatabase(callback_query.from_user.id))
        if Database(DB_NAME).checkUserInDatabase(callback_query.from_user.id):
            await bot.answer_callback_query(callback_query.id, text="Вы уже участвуете в розыгрыше!")
        else:
            Database(DB_NAME).addUserToDatabase(callback_query.from_user.id, callback_query.from_user.username)    
            await bot.answer_callback_query(callback_query.id, text="Вы участвуете в розыгрыше!")
    else:
        await bot.answer_callback_query(callback_query.id, text="Вы не являетесь подписчиком указанных каналов :-(")

#---PHOTO---
@dp.message_handler(regexp=r'!Загрузить фото')
async def waiting_photo(message: types.Message):
    if str(message.from_user.id) in config.ADMINS:
        logging.info(f"User {message.from_user.id} clicked LOAD_PHOTO")
        await message.reply("Пришли мне фотографию.")
        @dp.message_handler(content_types=["photo"])
        async def handle_photo(message):
            photo = message.photo[-1]
            file_id = photo.file_id
            file_info = await bot.get_file(message.photo[-1].file_id)
            await message.photo[-1].download(destination_file=PHOTO_FILE)
            global SWITCH
            SWITCH = "PHOTO"
            await message.answer("Фото сохранено.")

#---VIDEO---
@dp.message_handler(regexp=r'!Загрузить видео')
async def waiting_video(message: types.Message):
    if str(message.from_user.id) in config.ADMINS:
        logging.info(f"User {message.from_user.id} clicked LOAD_VIDEO")
        await message.reply("Пришли мне видеозапись.")
        @dp.message_handler(content_types=["video"])
        async def handle_video(message):
            file_id = message.video.file_id
            file = await bot.get_file(file_id)
            await message.video.download(destination_file=VIDEO_FILE)
            global SWITCH
            SWITCH = "VIDEO"
            await message.answer("Видео сохранено.")

#---AUDIO---
@dp.message_handler(regexp=r'!Загрузить аудио')
async def waiting_audio(message: types.Message):
    if str(message.from_user.id) in config.ADMINS:
        logging.info(f"User {message.from_user.id} clicked LOAD_AUDIO")
        await message.reply("Пришли мне аудиозапись.")
        @dp.message_handler(content_types=["audio"])
        async def handle_audio(message):
            file_id = message.audio.file_id
            file = await bot.get_file(file_id)
            await message.audio.download(destination_file=AUDIO_FILE)
            global SWITCH
            SWITCH = "AUDIO"
            await message.answer("Аудиозапись сохранена.")

#---TEXT-CAPTION---
@dp.message_handler(regexp=r'!Текст подписи поста')
async def waiting_text_caption(message: types.Message):
    if str(message.from_user.id) in config.ADMINS:
        logging.info(f"User {message.from_user.id} clicked LOAD_TEXT_POST")
        await message.reply("Пришли мне текст поста.")
        await ButtonState.postCaptionButton.set()

# Хэндлер для сохранения текста подписи поста в состоянии postCaptionButton
@dp.message_handler(state=ButtonState.postCaptionButton)
async def handle_text_caption(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in config.ADMINS:
        # Сохраняем текст поста в глобальную переменную
        global CAPTION_TEXT
        CAPTION_TEXT = message.text
        await message.answer("Текст сохранен.")
        # Возвращаемся в начальное состояние
        await state.finish()

#---TEXT-INLINE-BUTTON-CAPTION---
@dp.message_handler(regexp=r'!Текст подписи кнопки')
async def waiting_inline_button_caption(message: types.Message):
    if str(message.from_user.id) in config.ADMINS:
        logging.info(f"User {message.from_user.id} clicked LOAD_BUTTON_POST_TEXT")
        await message.reply("Пришли мне текст подписи кнопки под постом.")
        await ButtonState.inlinePostButton.set()

# Хэндлер для сохранения текста подписи кнопки в состоянии InlineButtonCaptionState
@dp.message_handler(state=ButtonState.inlinePostButton)
async def handle_text_inline_button_caption(message: types.Message, state: FSMContext):
    # Сохраняем текст подписи кнопки в глобальную переменную
    if str(message.from_user.id) in config.ADMINS:
        global INLINE_KEYBOARD_CAPTION
        INLINE_KEYBOARD_CAPTION = message.text
        await message.answer("Текст сохранен.")
        # Возвращаемся в начальное состояние
        await state.finish()