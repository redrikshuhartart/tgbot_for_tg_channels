from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

#---1---
__button_text = KeyboardButton('!Текст подписи поста')
__button_video = KeyboardButton('!Загрузить видео')
__button_photo = KeyboardButton('!Загрузить фото')
__button_audio = KeyboardButton('!Загрузить аудио')
__button_inline_button_caption = KeyboardButton('!Текст подписи кнопки поста')
__button_test_send = KeyboardButton('!Отправить тест сообщение')
__button_send = KeyboardButton('!Отправить сообщение')
__button_random = KeyboardButton('/random_user')
keyboard_admin_menu = ReplyKeyboardMarkup(resize_keyboard=True)

remove_keyboard = ReplyKeyboardRemove()

keyboard_admin_menu.add(__button_text, 
                        __button_video,
                        __button_photo, 
                        __button_audio, 
                        __button_inline_button_caption,
                        __button_test_send, 
                        __button_random,
                        __button_send)

#---2---
__button_video_content = KeyboardButton('!Загрузить видео')
__button_audio_content = KeyboardButton('!Загрузить аудио')
__button_photo_content = KeyboardButton('!Загрузить фото')

keyboad_content_type = ReplyKeyboardMarkup(resize_keyboard=True)

keyboad_content_type.add(__button_video_content,
                         __button_audio_content,
                         __button_photo_content)