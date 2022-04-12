from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from data.database import get_global_citat_list, get_user_citat_list, \
    change_user_sort
from loader import dp

from bot.filters.filters import AccessFilter
from bot.keyboards.citations_kb import CitationKeyboard


@dp.callback_query_handler(text_startswith='sort_by', access=True)
async def change_sort_type(call:CallbackQuery):
    sort_by = await change_user_sort(call.from_user.id)
    if not sort_by:
        await call.answer("Упс, щось я вас не впізнаю, напишіть /start "
                          "щоб ми познайомились😉", show_alert=True)
        return
    page_callback_data = (
        call.message.reply_markup.inline_keyboard[1][0]['callback_data'])
    list_type = page_callback_data.split(':')[2]
    if list_type == 'global_list':
        citat_list = await get_global_citat_list(call.from_user.id)
    else:
        citat_list = await get_user_citat_list(call.from_user.id)
    purpose = (
        call.message.reply_markup.inline_keyboard[0][0]['callback_data'].split(
            ':')[0])
    keyboard = CitationKeyboard(citat_list,
                                list_type,
                                sort_type=sort_by,
                                purpose=purpose.split("_")[0],
                                user_id=call.from_user.id)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard.citations_keyboard)
    await call.message.edit_text(keyboard.message_text,
                                 reply_markup=markup)
