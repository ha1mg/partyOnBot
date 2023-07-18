from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
import markups as nav
from db import posts, users, favourite, top
from messages import MESSAGES

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.callback_query_handler(text='next')
async def process_callback_next(callback_query: types.CallbackQuery):
    if users.fetch_state(callback_query.from_user.id) == 'nearest':
        near_loc_str = users.fetch_sorted_dist(callback_query.from_user.id)
        near_loc = [int(x) for x in near_loc_str.split(",")]
        users.increment_iter(callback_query.from_user.id)
        if users.fetch_iter(callback_query.from_user.id) >= posts.size():
            users.reset_iter(callback_query.from_user.id)
        data = posts.fetch(near_loc[users.fetch_iter(callback_query.from_user.id)])
        photo = open(f'media/pics/{data[0]}.jpg', 'rb')
        await callback_query.message.answer('Еще вариант:', reply_markup=types.ReplyKeyboardRemove())
        await callback_query.message.answer_photo(
            photo, caption='*{0}*\n_{1}_\n\n{2}\n\n_{3}_'.format(data[1], data[2], data[3], data[4]),
            reply_markup=nav.posts, parse_mode="Markdown")

@dp.callback_query_handler(text='favorite')
async def process_callback_favorite(callback_query: types.CallbackQuery):
    if users.fetch_state(callback_query.from_user.id) == 'nearest':
        near_loc_str = users.fetch_sorted_dist(callback_query.from_user.id)
        near_loc = [int(x) for x in near_loc_str.split(",")]
        if favourite.is_exist(posts.fetch(near_loc[users.fetch_iter(callback_query.from_user.id)])[1],
                                callback_query.from_user.id) == False:
            favourite.insert(posts.fetch(near_loc[users.fetch_iter(callback_query.from_user.id)])[1],
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
    users.edit_state('start', message.from_user.id)
    await bot.send_message(
        message.from_user.id,
        MESSAGES['start'].format(message.from_user),
        reply_markup=nav.mainMenu
    )
    if users.is_exist(message.from_user.id) == False:
        users.insert(message.from_user.id, str(message.from_user.first_name))


@dp.callback_query_handler(text='location')
async def process_callback_event_location(callback_query: types.CallbackQuery):
    near_loc_str = users.fetch_sorted_dist(callback_query.from_user.id)
    near_loc = [int(x) for x in near_loc_str.split(",")]
    data = posts.fetch(near_loc[users.fetch_iter(callback_query.from_user.id)])
    await callback_query.message.answer_location(data[5], data[6])


@dp.callback_query_handler(text='back')
async def process_callback_menu(callback_query: types.CallbackQuery):
    users.edit_state('start', callback_query.from_user.id)
    await bot.send_message(
        callback_query.from_user.id,
        MESSAGES['menu'],
        reply_markup=nav.mainMenu
    )


@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    if users.fetch_state(message.from_user.id) == 'nearest':
        lat = message.location.latitude
        lon = message.location.longitude
        users.recording_coords(lon, lat, message.from_user.id)
        near_loc_str = users.fetch_sorted_dist(message.from_user.id)
        near_loc = [int(x) for x in near_loc_str.split(",")]
        users.reset_iter(message.from_user.id)
        data = posts.fetch(near_loc[users.fetch_iter(message.from_user.id)])
        photo = open(f'media/pics/{data[0]}.jpg', 'rb')
        await message.answer('Почти у дома:', reply_markup=types.ReplyKeyboardRemove())
        await message.answer_photo(
            photo, caption='*{0}*\n_{1}_\n\n{2}\n\n_{3}_'.format(data[1], data[2], data[3], data[4]),
            reply_markup=nav.posts, parse_mode="Markdown")

@dp.message_handler()
async def bot_message(message: types.Message):
    if users.fetch_state(message.from_user.id) == 'start':
        if message.text == '🔍':
            users.edit_state('nearest', message.from_user.id)
            await message.answer(
                MESSAGES['location'],
                reply_markup=nav.location,
                parse_mode="Markdown"
            )
        elif message.text == '🔝':
            users.edit_state('top', message.from_user.id)
            data = top.fetch()
            for post_id in data:
                await bot.send_message(
                    message.from_user.id,
                    '{0}\n\n{1}'.format(posts.fetch(post_id[0])[1], posts.fetch(post_id[0])[2]),
                    reply_markup=nav.back
                )
        elif message.text == '⭐':
            users.edit_state('favoirite', message.from_user.id)
            data = favourite.fetch(message.from_user.id)
            if data:
                for organization in data:
                    post = posts.fetch_by_organization(organization[0])
                    photo = open(f'media/pics/{post[0]}.jpg', 'rb')
                    await message.answer_photo(
                        photo, caption='*{0}*\n_{1}_\n\n{2}\n\n_{3}_'.format(post[1], post[2], post[3], post[4]),
                        reply_markup=nav.back, parse_mode="Markdown")
            else:
                await bot.send_message(
                    message.from_user.id,
                    MESSAGES['favourite_null'],
                    reply_markup=nav.back
                )
    elif users.fetch_state(message.from_user.id) == 'top' or users.fetch_state(message.from_user.id) == 'favoirite' or users.fetch_state(message.from_user.id) == 'nearest':
        if message.text == '🏠':
            users.edit_state('start', message.from_user.id)
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

