from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

btnList = KeyboardButton('Список постов')
btnNew = KeyboardButton('Новый пост')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnList, btnNew)

btnSave = InlineKeyboardButton('Сохранить', callback_data='save')
btnEdit = InlineKeyboardButton('Изменить', callback_data='edit')
post = InlineKeyboardMarkup().add(btnSave, btnEdit)

btnCancel = KeyboardButton('Отмена')
cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(btnCancel)

btnNext = KeyboardButton('Далее')
nextField = ReplyKeyboardMarkup(resize_keyboard=True).add(btnNext)
