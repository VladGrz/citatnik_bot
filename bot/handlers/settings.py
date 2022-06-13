from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

from loader import dp
from bot.keyboards.settings_kb import user_pivacy_kb
from data.database import change_user_private_setting, reg_user

privat = {
    True: "приватні",
    False: "не приватні"
}


@dp.message_handler(commands='settings', state='*')
async def settings(message: Message):
    """ Catches `/settings` command. """

    # Sending settings message with keyboard to change privacy type
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
    """ Catches pressing a button which changes privacy. """

    # Getting the id of user from the callback to check if user that pressed
    # the button is the same that requested settings message
    user = int(call.data.split(':')[1])
    if user == call.from_user.id:
        privacy = await change_user_private_setting(call.from_user.id)
        if privacy is None:
            # If no privacy setting was found it means user uses bot for the
            # first time, and we should register him
            await reg_user(call)
            privacy = True
        try:
            # Trying to change keyboard
            await call.message.edit_reply_markup(
                await user_pivacy_kb(call.from_user.id)
            )
        except MessageNotModified:
            # If message was not modified we do nothing
            pass
        finally:
            # Finally, we show user a warning with current privacy
            await call.answer(f'Ваші цитати {privat[privacy]}.')
    else:
        # We show an alert that only user that called settings can change them
        await call.answer(f'Ці налаштування не для вас🤪. Напишіть /settings '
                          'і я надішлю вам ваші налаштування.',
                          show_alert=True)

