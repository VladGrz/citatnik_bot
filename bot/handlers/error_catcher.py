import asyncio
from loader import bot, dp

from aiogram.types import Message, CallbackQuery, Update


async def is_reply(message):
    if message.reply_to_message is not None:
        return True
    else:
        return False


@dp.errors_handler()
async def send_error_to_owner(update, exception):
    owner_id = 559346363
    if update.message:
        mes = update.message
    else:
        mes = update.callback_query.message
    await bot.send_message(chat_id=owner_id,
                           text='🆘Error occured🆘',
                           parse_mode='html')
    if await is_reply(mes):
        await bot.forward_message(chat_id=owner_id,
                                  from_chat_id=mes.chat.id,
                                  message_id=mes.reply_to_message.message_id)
    await bot.forward_message(chat_id=owner_id,
                              from_chat_id=mes.chat.id,
                              message_id=mes.message_id)

    error_message = f"<code>Update:</code> {update}\n\n<code>Exception:</code> {exception}"
    mess = await bot.send_message(chat_id=owner_id,
                                  text=error_message,
                                  parse_mode='html')