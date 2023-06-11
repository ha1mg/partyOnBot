from aiogram import Bot, Dispatcher, executor, types

import markups as nav
import location as lc
from bd import db_posts, db_users, db_favourite, db_top

TOKEN = '6164789985:AAERnbMba1dfJj20SJR4LWzfJFtlArE2uFw'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

lon = 0.0
lat = 0.0
near_loc = []

@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    db_users.edit_state('start', db_users.fetch_state(message.from_user.id))
    await bot.send_message(
        message.from_user.id,
        'Привет {0.first_name}\nЯ бот PartyOn и я помогу тебе провести эти выходные ахуенно'.format(message.from_user),
        reply_markup=nav.mainMenu
    )
    if db_users.isExist(message.from_user.id) == False:
        db_users.insert(message.from_user.id, str(message.from_user.first_name))

@dp.message_handler(content_types=['location'])
async def handle_location(message:types.Message):
    global near_loc
    if db_users.fetch_state(message.from_user.id) == 'nearest':
        lat = message.location.latitude
        lon = message.location.longitude
        coords = f"{lon},{lat}"
        address = lc.get_address_from_coords(coords)
        await message.answer(address)
        near_loc = db_posts.nearest(lon, lat)

        db_users.reset_iter(message.from_user.id)

        await bot.send_message(
            message.from_user.id,
            db_posts.fetch(near_loc[db_users.fetch_iter(message.from_user.id)][0])[1],
            reply_markup=nav.posts
        )



@dp.message_handler()
async def bot_message(message: types.Message):
    if db_users.fetch_state(message.from_user.id) == 'start':
        if message.text == 'Ближайшая тусовка':
            db_users.edit_state('nearest', message.from_user.id)
            await message.answer(
                'Кинь мне местоположение и я подскажу тебе, что есть рядом',
                reply_markup=nav.location
            )
        elif message.text == 'Топ':
            db_users.edit_state('top', message.from_user.id)
            data = db_top.fetch()
            for post_id in data:
                await bot.send_message(
                    message.from_user.id,
                    db_posts.fetch(post_id[0])[1],
                    reply_markup=nav.back
                )
        elif message.text == 'Избранное':
            db_users.edit_state('favoirite', message.from_user.id)
            await bot.send_message(
                message.from_user.id,
                '1. Тусы у Глебовича.\n',
                reply_markup=nav.back
            )
    elif db_users.fetch_state(message.from_user.id) == 'nearest':
        global near_loc
        if message.text == 'Другая':
            db_users.increment_iter(message.from_user.id)
            if db_users.fetch_iter(message.from_user.id) >= db_posts.size():
                db_users.reset_iter(message.from_user.id)
            await bot.send_message(
                message.from_user.id,
                db_posts.fetch(near_loc[db_users.fetch_iter(message.from_user.id)][0])[1],
                reply_markup=nav.posts
            )
        elif message.text == 'Назад':
            db_users.edit_state('start', message.from_user.id)
            await bot.send_message(
                message.from_user.id,
                'Выбери дальнейшее действие',
                reply_markup=nav.mainMenu
            )
    elif db_users.fetch_state(message.from_user.id) == 'top' or db_users.fetch_state(message.from_user.id) == 'favoirite':
        if message.text == 'Назад':
            db_users.edit_state('start', message.from_user.id)
            await bot.send_message(
                message.from_user.id,
                'Выбери дальнейшее действие',
                reply_markup=nav.mainMenu
            )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

