from aiogram import Bot, Dispatcher, executor, types

import bd.db_posts
import markups as nav
import location as lc
from bd import db_posts, db_users, db_favourite

#555bc789-2362-40fb-bfbf-c7c01038f989 ключ яндекса
TOKEN = '6164789985:AAERnbMba1dfJj20SJR4LWzfJFtlArE2uFw'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

state = ''
lon = 0.0
lot = 0.0


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    global state
    state = 'start'
    await bot.send_message(
        message.from_user.id,
        'Привет {0.first_name}\nЯ бот PartyOn и я помогу тебе провести эти выходные ахуенно'.format(message.from_user),
        reply_markup=nav.mainMenu
    )
    # if bd_users.isExist()
    bd_users.insert(message.from_user.id, str(message.from_user.first_name))

@dp.message_handler(content_types=['location'])
async def handle_location(message:types.Message):
    global state
    if state == 'nearest':
        lat = message.location.latitude
        lon = message.location.longitude
        coords = f"{lon},{lat}"
        adress = lc.get_address_from_coords(coords)
        await message.answer(adress)

        await message.answer(bd_posts.nearest(lon, lat))
@dp.message_handler()
async def bot_message(message: types.Message):
    global state
    if state == 'start':
        if message.text == 'Ближайшая тусовка':
            state = 'nearest1'
            await message.answer(
                'Кинь мне местоположение и я подскажу тебе, что есть рядом',
                reply_markup=nav.location
            )

        elif message.text == 'Топ':
            state = 'top'
            await bot.send_message(
                message.from_user.id,
                'Топ организаций:\n1. Тусы у Глебовича.\n2.СытоПьяно\n3.(Рекламное место)',
                reply_markup=nav.back
            )
        elif message.text == 'Избранное':
            state = 'favoirite'
            await bot.send_message(
                message.from_user.id,
                '1. Тусы у Глебовича.\n',
                reply_markup=nav.back
            )
    elif state == 'nearest' or state == 'top' or state == 'favoirite':
        if message.text == 'Назад':
            state = 'start'
            await bot.send_message(
                message.from_user.id,
                'Выбери дальнейшее действие',
                reply_markup=nav.mainMenu
            )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

