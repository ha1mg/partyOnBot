from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from main import bot, dp
import config
import markups


class IsSubscriber(BoundFilter):
    async def check_sub(self, message:types.Message):
        sub = await bot.get_chat_member(chat_id=config.partyOnChanelTest_id, user_id=message.from_user.id)
        if sub.status != types.ChatMemberStatus:
            return True
        else:
            await dp.bot.send_message(chat_id=message.from_user.id,
                                      text=f'Сначала подпишись на канал, а потом повтори попытку)',
                                      reply_markup=markups.subscrKB)
            return False
