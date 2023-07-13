from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

from config import TOKEN
import markups as nav
from db import posts, users, favourite, top
from messages import MESSAGES

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.callback_query_handler(Text('next'))
async def process_callback_next(callback_query: types.CallbackQuery):
    if db_users.fetch_state(callback_query.from_user.id) == 'nearest':
        near_loc_str = db_users.fetch_sorted_dist(callback_query.from_user.id)
        near_loc = [int(x) for x in near_loc_str.split(",")]
        db_users.increment_iter(callback_query.from_user.id)
        if db_users.fetch_iter(callback_query.from_user.id) >= db_posts.size():
            db_users.reset_iter(callback_query.from_user.id)
        data = db_posts.fetch(near_loc[db_users.fetch_iter(callback_query.from_user.id)])
        photo = open(f'media/pics/{data[0]}.jpg', 'rb')
        await callback_query.message.answer_photo(
            photo, caption='*{0}*\n_{1}_\n\n{2}\n\n_{3}_'.format(data[1], data[2], data[3], data[4]),
            reply_markup=nav.back, parse_mode="Markdown")
        await bot.send_location(callback_query.from_user.id, data[5], data[6], reply_markup=nav.posts)

@dp.callback_query_handler(Text('favorite'))
async def process_callback_favorite(callback_query: types.CallbackQuery):
    if db_users.fetch_state(callback_query.from_user.id) == 'nearest':
        near_loc_str = db_users.fetch_sorted_dist(callback_query.from_user.id)
        near_loc = [int(x) for x in near_loc_str.split(",")]
        if db_favourite.isExist(db_posts.fetch(near_loc[db_users.fetch_iter(callback_query.from_user.id)])[1],
                                callback_query.from_user.id) == False:
            db_favourite.insert(db_posts.fetch(near_loc[db_users.fetch_iter(callback_query.from_user.id)])[1],
                                callback_query.from_user.id)
            await callback_query.message.answer(
                MESSAGES['favourite']
            )
        else:
            await callback_query.message.answer(
                MESSAGES['favourite_exist']
            )

@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    db_users.edit_state('start', message.from_user.id)
    await bot.send_message(
        message.from_user.id,
        MESSAGES['start'].format(message.from_user),
        reply_markup=nav.mainMenu
    )
    if db_users.isExist(message.from_user.id) == False:
        db_users.insert(message.from_user.id, str(message.from_user.first_name))

@dp.message_handler(content_types=['location'])
async def handle_location(message:types.Message):
    if db_users.fetch_state(message.from_user.id) == 'nearest':
        lat = message.location.latitude
        lon = message.location.longitude
        db_users.recording_coords(lon, lat, message.from_user.id)
        near_loc_str = db_users.fetch_sorted_dist(message.from_user.id)
        near_loc = [int(x) for x in near_loc_str.split(",")]
        db_users.reset_iter(message.from_user.id)
        data = db_posts.fetch(near_loc[db_users.fetch_iter(message.from_user.id)])
        photo = open(f'media/pics/{data[0]}.jpg', 'rb')
        await message.answer_photo(
                photo, caption='*{0}*\n_{1}_\n\n{2}\n\n_{3}_'.format(data[1], data[2], data[3], data[4]),
                reply_markup=nav.back, parse_mode="Markdown")
        await bot.send_location(message.from_user.id, data[5], data[6], reply_markup=nav.posts)

@dp.message_handler()
async def bot_message(message: types.Message):
    if db_users.fetch_state(message.from_user.id) == 'start':
        if message.text == 'Ближайшая тусовка':
            db_users.edit_state('nearest', message.from_user.id)
            await message.answer(
                MESSAGES['location'],
                reply_markup=nav.location,
                parse_mode="Markdown"
            )
        elif message.text == 'Топ':
            db_users.edit_state('top', message.from_user.id)
            data = db_top.fetch()
            for post_id in data:
                await bot.send_message(
                    message.from_user.id,
                    '{0}\n\n{1}'.format(db_posts.fetch(post_id[0])[1], db_posts.fetch(post_id[0])[2]),
                    reply_markup=nav.back
                )
        elif message.text == 'Избранное':
            db_users.edit_state('favoirite', message.from_user.id)
            data = db_favourite.fetch(message.from_user.id)
            if data:
                for i in data:
                    await bot.send_message(
                        message.from_user.id,
                        '{0}\n\n{1}'.format(db_posts.fetch_by_organization(i[0])[1], db_posts.fetch_by_organization(i[0])[2]),
                        reply_markup=nav.back
                )
            else:
                await bot.send_message(
                    message.from_user.id,
                    MESSAGES['favourite_null'],
                    reply_markup=nav.back
                )
    elif db_users.fetch_state(message.from_user.id) == 'top' or db_users.fetch_state(message.from_user.id) == 'favoirite' or db_users.fetch_state(message.from_user.id) == 'nearest':
        if message.text == 'Меню':
            db_users.edit_state('start', message.from_user.id)
            await bot.send_message(
                message.from_user.id,
                MESSAGES['menu'],
                reply_markup=nav.mainMenu
            )

@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

