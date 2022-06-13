from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup

from loader import dp

from data.database import get_citation, get_user_citat_list, \
    get_global_citat_list, get_user_sort

from bot.keyboards.like_dislike_kb import form_like_dislike_kb
from bot.keyboards.users_choice_kb import users_choice_kb
from bot.keyboards.citations_kb import CitationKeyboard

from bot.filters.filters import AccessFilter


@dp.callback_query_handler(text_startswith='back_to:', state="*")
async def users_choice_citats_list(call: CallbackQuery):
    """ Catching pressed button 'Back_to: '"""
    await call.answer()

    # Editing text and keyboard for choosing citation list message
    await call.message.edit_text("Цитату з якого списку бажаєте відправити?",
                                 reply_markup=users_choice_kb)


@dp.message_handler(commands='citation', state='*')
async def users_choice_citats_list(message: Message):
    """ Catching `/citation` command to show message with chosement of citation list to show. """
    await message.reply("Цитату з якого списку бажаєте відправити?",
                        reply_markup=users_choice_kb)


@dp.callback_query_handler(text_startswith="choice:", state='*')
async def form_citation_list(call: CallbackQuery):
    """Catching user's choice of citation list. """

    list_type = call.data.split(":")[1]
    if list_type == 'global_list':
        # getting global citations list
        citat_list = await get_global_citat_list(call.from_user.id)
    else:
        # getting personal citations list
        citat_list = await get_user_citat_list(call.from_user.id)
    sort_by = await get_user_sort(call.from_user.id)
    keyboard = CitationKeyboard(citat_list,
                                list_type,
                                sort_type=sort_by,
                                user_id=call.from_user.id)

    # forming keyboard to be pinned to a message
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard.citations_keyboard)

    # Editing message text and keyboard
    await call.message.edit_text(keyboard.message_text,
                                 reply_markup=markup)
    await call.answer()


@dp.callback_query_handler(text_startswith='page:', access=True, state='*')
async def change_page(call: CallbackQuery):
    """ Catching pressing a page button. """

    await call.answer()

    # splitting callback data to get user_id, purpose, current page data, and type of list
    calldata = call.data.split(":")
    purpose = (
        call.message.reply_markup.inline_keyboard[0][0]['callback_data'].split(
            ':')[0])
    user_id = int(calldata[3])
    list_type = calldata[2]
    page_start, page_end = calldata[1].split("-")

    if list_type == 'global_list':
        citat_list = await get_global_citat_list(call.from_user.id)
    else:
        citat_list = await get_user_citat_list(user_id)

    sort_by = await get_user_sort(user_id)
    keyboard = CitationKeyboard(citat_list,
                                list_type,
                                sort_type=sort_by,
                                purpose=purpose.split("_")[0],
                                user_id=user_id,
                                start=int(page_start))
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard.citations_keyboard)
    await call.message.edit_text(keyboard.message_text,
                                 reply_markup=markup)


@dp.callback_query_handler(text_contains='send_citation', access=True,
                           state='*')
async def send_citation(call: CallbackQuery):
    """ Catching user`s desire to send citation. """

    # Splitting callback data to get citation id
    doc_id = call.data.split(":")[1]
    file_id, file_type, file_name = await get_citation(call.from_user.id,
                                                       doc_id)
    if file_id is None:
        await call.answer(text="Не вдалось знайти цитату             🔍❌\n"
                               "Можливо користувач її видалив ✉️➡️🗑",
                          show_alert=True)
    else:
        first_name = call.from_user.first_name
        last_name = call.from_user.last_name

        # Joining first and lastname of user
        sent_by = (('' if first_name is None else first_name)
                   + ' '
                   + '' if last_name is None else last_name)

        likes_kb = await form_like_dislike_kb(doc_id)

        # Checking whether file is in audio or voice format to send it in
        # appropriate format
        if 'mpeg' in file_type:
            await call.message.answer_audio(file_id,
                                            caption=f"{file_name}\nSent by {sent_by}",
                                            reply_markup=likes_kb)
        elif 'ogg' in file_type:
            await call.message.answer_voice(file_id,
                                            caption=f"{file_name}\nSent by {sent_by}",
                                            reply_markup=likes_kb)
        await call.answer(text="Цитату надіслано")
