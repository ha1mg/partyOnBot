from aiogram import Bot, Dispatcher, executor, types
import markups as nav

TOKEN = '6164789985:AAERnbMba1dfJj20SJR4LWzfJFtlArE2uFw'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

state = ''


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    global state
    state = 'start'
    await bot.send_message(
        message.from_user.id,
        'Привет {0.first_name}\nЯ бот PartyOn и я помогу тебе провести эти выходные ахуенно'.format(message.from_user),
        reply_markup=nav.mainMenu
    )


@dp.message_handler()
async def bot_message(message: types.Message):
    global state
    if state == 'start':
        if message.text == 'Ближайшая тусовка':
            state = 'nearest'
            await bot.send_message(
                message.from_user.id,
                'Кинь мне местоположение и я подскажу тебя, что есть рядом'
            )
            await message.answer(
                'Туса у Глебовича\nАдрес: Лыткарино\nТам будет клеавый дед, дешевое бухло и вид на Москву реку'
            )
            await message.answer_location(55.589387, 37.886200, reply_markup=nav.back)

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
