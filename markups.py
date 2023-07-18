from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import config
# inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
# inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)

# --- Main Menu ---
btnNearest = KeyboardButton('🔍')
btnTop = KeyboardButton('🔝')
btnFavourite = KeyboardButton('⭐')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnNearest, btnTop, btnFavourite)

# --- Return ---
btnReturn = KeyboardButton('🏠')
back = ReplyKeyboardMarkup(resize_keyboard=True).add(btnReturn)

# --- Location ---
btnLocation = KeyboardButton('🌍', request_location=True)
location = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnLocation, btnReturn)

# --- Posts ---
btnNext = InlineKeyboardButton('➡', callback_data='next')
btnLike = InlineKeyboardButton('🧡', callback_data='favorite')
btnEventLocation = InlineKeyboardButton('🌍', callback_data='location')
btnReturnPost = InlineKeyboardButton('🏠', callback_data='back')
posts = InlineKeyboardMarkup().add(btnNext, btnLike, btnEventLocation, btnReturnPost)


# --- Subscribes ---
btnChanel1 = InlineKeyboardButton(text='Канал #1', url=config.channel_link)
btnIsSubscribe = InlineKeyboardButton(text='Подписался!', callback_data='start')
subscribes = InlineKeyboardMarkup(row_width=1).add(btnChanel1, btnIsSubscribe)
