from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
# inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)

# --- Main Menu ---
btnNearest = KeyboardButton('Ближайшая тусовка')
btnTop = KeyboardButton('Топ')
btnFavourite = KeyboardButton('Избранное')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnNearest, btnTop, btnFavourite)

# --- Return ---
btnReturn = InlineKeyboardButton('Меню', callback_data='back')
back = InlineKeyboardMarkup().add(btnReturn)

# --- Location ---
btnLocation = KeyboardButton('Отправить локацию', request_location=True)
location = ReplyKeyboardMarkup(resize_keyboard=True).add(btnLocation)

# --- Posts ---
btnNext = InlineKeyboardButton('Другая', callback_data='next')
btnLike = InlineKeyboardButton('В любимое', callback_data='favorite')
posts = InlineKeyboardMarkup().add(btnNext, btnLike, btnReturn)
