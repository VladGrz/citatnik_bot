from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup

from loader import dp

from data.database import get_citation, get_user_citat_list, \
    delete_user_citation, get_user_sort

from bot.keyboards.citations_kb import CitationKeyboard
from bot.filters.filters import AccessFilter


@dp.message_handler(commands='delete_citation', state='*')
async def form_citation_list(message: Message):
    """
    Catching user`s desire to delete citation and forming citations list.
    """

    citat_list = await get_user_citat_list(message.from_user.id)
    sort_by = await get_user_sort(message.from_user.id)
    keyboard = CitationKeyboard(citat_list,
                                sort_type=sort_by,
                                list_type='private_list',
                                purpose='delete',
                                user_id=message.from_user.id)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard.citations_keyboard)
    await message.reply(keyboard.message_text,
                        reply_markup=markup)


@dp.callback_query_handler(text_startswith='delete_citation', access=True, state="*")
async def delete_citation(call: CallbackQuery):
    """ Catching citations which user wants to delete. """

    # Splitting callback data to get citation id
    doc_id = call.data.split(":")[1]
    file_id, file_type, file_name = await get_citation(call.from_user.id,
                                                       doc_id)
    pages = call.message.reply_markup.inline_keyboard[1]
    citats = call.message.reply_markup.inline_keyboard[0]
    start = int(pages[0]['text'].split("-")[0])
    user_id = int(pages[0]['callback_data'].split(":")[3])

    # Defining current page and start point for the new citation list after deletion
    for i in pages:
        if '✅' in i['text'] and len(pages) != 1 and len(citats) > 1:
            start = int(i['text'].split("-")[0])
            print(i, start)

    await delete_user_citation(doc_id)

    # Warning user that his citation was deleted
    await call.answer(f'Вашу цитату: "{file_name}", видалено.',
                      show_alert=True)

    # Forming new message without that citation
    citat_list = await get_user_citat_list(user_id)
    sort_by = await get_user_sort(call.from_user.id)
    keyboard = CitationKeyboard(citat_list,
                                sort_type=sort_by,
                                list_type='private_list',
                                purpose='delete',
                                user_id=user_id,
                                start=start)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard.citations_keyboard)
    await call.message.edit_text(keyboard.message_text, reply_markup=markup)
