from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

from loader import bot, dp
from bot.keyboards.settings_kb import user_pivacy_kb
from data.database import change_user_private_setting, reg_user

privat = {
    True: "приватні",
    False: "не приватні"
}


@dp.message_handler(commands='settings', state='*')
async def settings(message: Message):
    await message.reply("Тут ви можете змінити доступність ваших цитат, "
                         "для цього клацніть на кнопку.\n\n"
                         "✅ - означає, що ваші цитати приватні, "
                         "вони не будуть відображатись в глобальному списку "
                         "цитат і, під час вибору цитат в групі, "
                         "інша людина не "
                         "зможе викликати цитату з вашого списку."
                         "\n❌ - означає, що ваші цитати не приватні.",
                         reply_markup=await user_pivacy_kb(
                             message.from_user.id))


@dp.callback_query_handler(text_startswith='change_pivacy', state='*')
async def change_privacy(call: CallbackQuery):
    user = int(call.data.split(':')[1])
    if user == call.from_user.id:
        privacy = await change_user_private_setting(call.from_user.id)
        if privacy is None:
            await reg_user(call)
            privacy = True
        try:
            await call.message.edit_reply_markup(
                await user_pivacy_kb(call.from_user.id)
            )
        except MessageNotModified:
            await call.answer(f'Ваші цитати {privat[privacy]}.')
        else:
            await call.answer(f'Ваші цитати {privat[privacy]}.')
    else:
        await call.answer(f'Ці налаштування не для вас🤪. Напишіть /settings '
                          'і я надішлю вам ваші налаштування.',
                          show_alert=True)

