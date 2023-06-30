from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import manager_markups
from ManagerState import ManagerState
from config import MANAGER_TOKEN
from messages import MANAGER_MESSAGES
import manager_markups as nav
import time
import location
from db import db_posts

bot = Bot(token=MANAGER_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# @dp.message_handler(state=ManagerState.media, content_types=['video', 'video_note'])
# async def get_video(message: types.Message, state: FSMContext):
#     await state.update_data(info=[message.effective_attachment.file_id])
#     await message.answer('Еще?')

# @dp.callback_query_handler(Text('edit'))
# async def process_callback_edit(callback_query: types.CallbackQuery):


@dp.message_handler(commands=['start'], state='*')
async def command_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        MANAGER_MESSAGES['start'].format(message.from_user),
        reply_markup=nav.mainMenu
    )


@dp.message_handler()
async def bot_message(message: types.Message):
    if message.text == 'Новый пост':
        await message.answer(MANAGER_MESSAGES['organization'], reply_markup=manager_markups.cancel)
        await ManagerState.organization.set()


@dp.message_handler(state='*', text="Отмена")
async def bot_message(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Действие отменено', reply_markup=nav.mainMenu)


@dp.callback_query_handler(Text('save'), state=ManagerState.media)
async def process_callback_save(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        row_id = db_posts.insert(data['organization'], data['date'], data['description'], data['address'],
                                 float(data['location'].split()[1]), float(data['location'].split()[0]))
        print(row_id)
        photo_path = f'media/pics/{row_id}.jpg'
        await data['media'].download(destination_file=photo_path)
        await callback_query.answer('Пост записан')
    except Exception as e:
        print(f"Error occurred: {e}")
        await callback_query.answer('Не удалось записать данные')


@dp.message_handler(state=ManagerState.media, content_types='photo')
async def get_photo(message: types.Message, state: FSMContext):
    await state.update_data(media=message.photo[-1])
    data = await state.get_data()
    await message.answer_photo(data['media'].file_id,
                               caption='*{0}*\n_{1}_\n\n{2}\n\n_{3}_'.format(
                                   data['organization'], data['date'], data['description'], data['address']),
                               parse_mode="Markdown")
    await message.answer_location(data['location'].split()[1], data['location'].split()[0], reply_markup=nav.post)


@dp.message_handler(state=ManagerState.media)
async def get_photo_error(message: types.Message):
    await message.answer(MANAGER_MESSAGES['media_error'])


@dp.message_handler(state=ManagerState.address)
async def get_address(message: types.Message, state: FSMContext):
    try:
        await state.update_data(location=location.get_coords_from_address(message.text))
        print(location.get_coords_from_address(message.text))
        await state.update_data(address=message.text)
        await message.answer(MANAGER_MESSAGES['media'])
        await ManagerState.media.set()
    except Exception as e:
        print(f"Error occurred: {e}")
        await message.answer(MANAGER_MESSAGES['address_error'])


@dp.message_handler(state=ManagerState.description)
async def get_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(MANAGER_MESSAGES['address'])
    await ManagerState.address.set()


@dp.message_handler(state=ManagerState.date)
async def get_date(message: types.Message, state: FSMContext):
    try:
        time.strptime(message.text, '%d.%m.%Y')
        await state.update_data(date=message.text)
        await message.answer(MANAGER_MESSAGES['description'])
        await ManagerState.description.set()
    except ValueError:
        await message.answer(MANAGER_MESSAGES['date_error'])


@dp.message_handler(state=ManagerState.organization)
async def get_organization(message: types.Message, state: FSMContext):
    await state.update_data(organization=message.text)
    await message.answer(MANAGER_MESSAGES['date'])
    await ManagerState.date.set()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
