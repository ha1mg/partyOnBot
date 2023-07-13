from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
# inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)

# --- Main Menu ---
btnNearest = KeyboardButton('Ближайшая тусовка')
btnTop = KeyboardButton('Топ')
btnFavourite = KeyboardButton('Избранное')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnNearest, btnTop, btnFavourite)

# --- Return ---
btnReturn = KeyboardButton('Меню')
back = ReplyKeyboardMarkup(resize_keyboard=True).add(btnReturn)

# --- Location ---
btnLocation = KeyboardButton('Отправить локацию', request_location=True)
location = ReplyKeyboardMarkup(resize_keyboard=True).add(btnLocation, btnReturn)

# --- Posts ---
btnNext = InlineKeyboardButton('Другая', callback_data='next')
btnLike = InlineKeyboardButton('В любимое', callback_data='favorite')
btnEventLocation = InlineKeyboardButton('где это??', callback_data='location')
btnReturnPost = InlineKeyboardButton('Меню', callback_data='back')
posts = InlineKeyboardMarkup().add(btnNext, btnLike, btnEventLocation, btnReturnPost)


