from aiogram import Bot, Dispatcher, executor, types

import markups as nav
import location as lc
from bd import db_posts, db_users, db_favourite, db_top

TOKEN = '6164789985:AAERnbMba1dfJj20SJR4LWzfJFtlArE2uFw'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

state = ''
lon = 0.0
lat = 0.0
near_loc = []
i = 0

@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    global state
    state = 'start'
    await bot.send_message(
        message.from_user.id,
        'Привет {0.first_name}\nЯ бот PartyOn и я помогу тебе провести эти выходные ахуенно'.format(message.from_user),
        reply_markup=nav.mainMenu
    )
    if db_users.isExist(message.from_user.id) == False:
        db_users.insert(message.from_user.id, str(message.from_user.first_name))

@dp.message_handler(content_types=['location'])
async def handle_location(message:types.Message):
    global state
    if state == 'nearest':
        lat = message.location.latitude
        lon = message.location.longitude
        coords = f"{lon},{lat}"
        address = lc.get_address_from_coords(coords)
        await message.answer(address)
        near_loc = db_posts.nearest(lon, lat)

        await bot.send_message(
            message.from_user.id,
            db_posts.fetch(near_loc[i])[1],
            reply_markup=nav.posts
        )



@dp.message_handler()
async def bot_message(message: types.Message):
    global state
    if state == 'start':
        if message.text == 'Ближайшая тусовка':
            state = 'nearest'
            await message.answer(
                'Кинь мне местоположение и я подскажу тебе, что есть рядом',
                reply_markup=nav.location
            )
        elif message.text == 'Топ':
            state = 'top'
            data = db_top.fetch()
            for post_id in data:
                await bot.send_message(
                    message.from_user.id,
                    db_posts.fetch(post_id)[1],
                    reply_markup=nav.back
                )
        elif message.text == 'Избранное':
            state = 'favoirite'
            await bot.send_message(
                message.from_user.id,
                '1. Тусы у Глебовича.\n',
                reply_markup=nav.back
            )
    elif state == 'nearest':
        global i
        global near_loc
        if message.text == 'Другая':
            i+=1
            await bot.send_message(
                message.from_user.id,
                db_posts.fetch(near_loc[i])[1],
                reply_markup=nav.posts
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

