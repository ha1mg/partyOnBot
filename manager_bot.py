from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import manager_markups
from ManagerState import ManagerState
from config import MANAGER_TOKEN, ADMIN_ID
from messages import MANAGER_MESSAGES
import manager_markups as nav
import time
import location
from db import managers, posts

bot = Bot(token=MANAGER_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message, state: FSMContext):
    await state.finish()
    if message.from_user.id in managers.fetch_id() or message.from_user.id in ADMIN_ID:
        await message.answer(
            MANAGER_MESSAGES['start'].format(message.from_user),
            reply_markup=nav.mainMenu
        )
    else:
        await message.answer(
            'Я тебя не знаю'
        )


@dp.message_handler(state='*', text='Новый пост')
async def bot_message(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(MANAGER_MESSAGES['organization'], reply_markup=manager_markups.cancel)
    await ManagerState.organization.set()


@dp.message_handler(state='*', text="Отмена")
async def bot_message(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Действие отменено', reply_markup=nav.mainMenu)


@dp.message_handler(state=ManagerState.organization)
async def get_organization(message: types.Message, state: FSMContext):
    await state.update_data(organization=message.text)
    await message.answer(MANAGER_MESSAGES['date'])
    await ManagerState.date.set()


@dp.message_handler(state=ManagerState.date)
async def get_date(message: types.Message, state: FSMContext):
    try:
        time.strptime(message.text, '%d.%m.%Y')
        await state.update_data(date=message.text)
        await message.answer(MANAGER_MESSAGES['description'])
        await ManagerState.description.set()
    except ValueError:
        await message.answer(MANAGER_MESSAGES['date_error'])


@dp.message_handler(state=ManagerState.description)
async def get_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(MANAGER_MESSAGES['address'])
    await ManagerState.address.set()


@dp.message_handler(state=ManagerState.address)
async def get_address(message: types.Message, state: FSMContext):
    try:
        await state.update_data(location=location.get_coords_from_address(message.text))
        await state.update_data(address=message.text)
        await message.answer(MANAGER_MESSAGES['media'])
        await ManagerState.media.set()
    except Exception as e:
        print(f"Error occurred: {e}")
        await message.answer(MANAGER_MESSAGES['address_error'])


@dp.message_handler(state=ManagerState.media, content_types='photo')
async def get_photo(message: types.Message, state: FSMContext):
    await state.update_data(media=message.photo[-1])
    data = await state.get_data()
    await message.answer_photo(data['media'].file_id,
                               caption='*{0}*\n_{1}_\n\n{2}\n\n_{3}_'.format(
                                   data['organization'], data['date'], data['description'], data['address']),
                               parse_mode="Markdown")
    await message.answer_location(data['location'].split()[1], data['location'].split()[0], reply_markup=nav.post)


@dp.message_handler(state=ManagerState.media, content_types='any')
async def get_photo_error(message: types.Message):
    await message.answer(MANAGER_MESSAGES['media_error'])


@dp.callback_query_handler(state=ManagerState.media, text='save')
async def process_callback_save(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        row_id = posts.insert(data['organization'], data['date'], data['description'], data['address'],
                              float(data['location'].split()[1]), float(data['location'].split()[0]))
        photo_path = f'media/pics/{row_id}.jpg'
        await data['media'].download(destination_file=photo_path)
        await callback_query.message.answer('Пост записан', reply_markup=nav.mainMenu)
        await state.finish()
    except Exception as e:
        print(f"Error occurred: {e}")
        await callback_query.answer('Не удалось записать данные')


@dp.callback_query_handler(state=ManagerState.media, text='edit')
async def process_callback_edit(callback_query: types.CallbackQuery,  state: FSMContext):
    await ManagerState.edit_organization.set()
    data = await state.get_data()
    await callback_query.message.answer(f'{MANAGER_MESSAGES["organization"]}\n\n{data["organization"]}',
                                        reply_markup=nav.nextField)


@dp.callback_query_handler(state=ManagerState.edit_organization, text='next')
async def process_callback_edit_organization(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback_query.message.answer(f'{MANAGER_MESSAGES["date"]}\n\n{data["date"]}', reply_markup=nav.nextField)
    await ManagerState.edit_date.set()


@dp.message_handler(state=ManagerState.edit_organization)
async def edit_organization(message: types.Message, state: FSMContext):
    await state.update_data(organization=message.text)
    data = await state.get_data()
    await message.answer(f'{MANAGER_MESSAGES["date"]}\n\n{data["date"]}', reply_markup=nav.nextField)
    await ManagerState.edit_date.set()


@dp.callback_query_handler(state=ManagerState.edit_date, text='next')
async def process_callback_edit_date(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback_query.message.answer(f'{MANAGER_MESSAGES["description"]}\n\n{data["description"]}',
                                        reply_markup=nav.nextField)
    await ManagerState.edit_description.set()


@dp.message_handler(state=ManagerState.edit_date)
async def edit_date(message: types.Message, state: FSMContext):
    try:
        time.strptime(message.text, '%d.%m.%Y')
        await state.update_data(date=message.text)
        data = await state.get_data()
        await message.answer(f'{MANAGER_MESSAGES["description"]}\n\n{data["description"]}', reply_markup=nav.nextField)
        await ManagerState.edit_description.set()
    except ValueError:
        await message.answer(MANAGER_MESSAGES['date_error'])


@dp.callback_query_handler(state=ManagerState.edit_description, text='next')
async def process_callback_edit_description(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback_query.message.answer(f'{MANAGER_MESSAGES["address"]}\n\n{data["address"]}',
                                        reply_markup=nav.nextField)
    await ManagerState.edit_address.set()


@dp.message_handler(state=ManagerState.edit_description)
async def edit_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    await message.answer(f'{MANAGER_MESSAGES["address"]}\n\n{data["address"]}', reply_markup=nav.nextField)
    await ManagerState.edit_address.set()


@dp.callback_query_handler(state=ManagerState.edit_address, text='next')
async def process_callback_edit_address(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback_query.message.answer(MANAGER_MESSAGES["media"])
    await callback_query.message.answer_photo(data['media'].file_id, reply_markup=nav.nextField)
    await ManagerState.edit_media.set()


@dp.message_handler(state=ManagerState.edit_address)
async def edit_address(message: types.Message, state: FSMContext):
    try:
        await state.update_data(location=location.get_coords_from_address(message.text))
        await state.update_data(address=message.text)
        data = await state.get_data()
        await message.answer(MANAGER_MESSAGES["media"], reply_markup=nav.nextField)
        await message.answer_photo(data['media'].file_id)
        await ManagerState.edit_media.set()
    except Exception as e:
        print(f"Error occurred: {e}")
        await message.answer(MANAGER_MESSAGES['address_error'])


@dp.callback_query_handler(state=ManagerState.edit_media, text='next')
async def process_callback_edit_photo(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback_query.message.answer_photo(data['media'].file_id,
                                              caption='*{0}*\n_{1}_\n\n{2}\n\n_{3}_'.format(
                                                  data['organization'], data['date'],
                                                  data['description'], data['address']),
                                              parse_mode="Markdown")
    await callback_query.message.answer_location(data['location'].split()[1], data['location'].split()[0],
                                                 reply_markup=nav.post)


@dp.message_handler(state=ManagerState.edit_media, content_types='photo')
async def edit_photo(message: types.Message, state: FSMContext):
    await state.update_data(media=message.photo[-1])
    data = await state.get_data()
    await message.answer_photo(data['media'].file_id,
                               caption='*{0}*\n_{1}_\n\n{2}\n\n_{3}_'.format(
                                   data['organization'], data['date'], data['description'], data['address']),
                               parse_mode="Markdown")
    await message.answer_location(data['location'].split()[1], data['location'].split()[0], reply_markup=nav.post)


@dp.message_handler(state=ManagerState.edit_media, content_types='any')
async def edit_photo_error(message: types.Message):
    await message.answer(MANAGER_MESSAGES['media_error'])


@dp.callback_query_handler(state=ManagerState.edit_media, text='save')
async def process_callback_save(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        row_id = posts.insert(data['organization'], data['date'], data['description'], data['address'],
                              float(data['location'].split()[1]), float(data['location'].split()[0]))
        photo_path = f'media/pics/{row_id}.jpg'
        await data['media'].download(destination_file=photo_path)
        await callback_query.message.answer('Пост записан', reply_markup=nav.mainMenu)
        await state.finish()
    except Exception as e:
        print(f"Error occurred: {e}")
        await callback_query.answer('Не удалось записать данные')


@dp.callback_query_handler(state=ManagerState.edit_media, text='edit')
async def process_callback_edit(callback_query: types.CallbackQuery,  state: FSMContext):
    await ManagerState.edit_organization.set()
    data = await state.get_data()
    await callback_query.message.answer(f'{MANAGER_MESSAGES["organization"]}\n\n{data["organization"]}',
                                        reply_markup=nav.nextField)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
