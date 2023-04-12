from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton




# --- Main Menu ---
btnNearest = KeyboardButton('Ближайшая тусовка')
btnTop = KeyboardButton('Топ')
btnFavourite = KeyboardButton('Избранное')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnNearest, btnTop, btnFavourite)

# --- Return Inline ---
btnReturn = KeyboardButton('Назад')
back = ReplyKeyboardMarkup(resize_keyboard=True).add(btnReturn)


