from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# --- Main Menu ---
btnNearest = KeyboardButton('Ближайшая тусовка')
btnTop = KeyboardButton('Топ')
btnFavourite = KeyboardButton('Избранное')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnNearest, btnTop, btnFavourite)

# --- Return Inline ---
btnReturn = KeyboardButton('Назад')
back = ReplyKeyboardMarkup(resize_keyboard=True).add(btnReturn)

# --- Location ---
btnLocation = KeyboardButton('Отправить локацию', request_location=True)
location = ReplyKeyboardMarkup(resize_keyboard=True).add(btnLocation)

# --- Top ---
btnNext = KeyboardButton('Другая', request_location=True)
btnLike = KeyboardButton('В любимое', request_location=True)
posts = ReplyKeyboardMarkup(resize_keyboard=True).add(btnNext, btnLike)
