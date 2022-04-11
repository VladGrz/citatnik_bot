from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup

from loader import bot, dp

from data.database import get_citation, get_user_citat_list, \
    get_global_citat_list

from bot.keyboards.like_dislike_kb import form_like_dislike_kb
from bot.keyboards.users_choice_kb import users_choice_kb
from bot.keyboards.citations_kb import CitationKeyboard

from bot.filters.filters import AccessFilter


@dp.callback_query_handler(text_startswith='back_to:', state="*")
async def users_choice_citats_list(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text("Цитату з якого списку бажаєте відправити?",
                                 reply_markup=users_choice_kb)


@dp.message_handler(commands='citation', state='*')
async def users_choice_citats_list(message: Message):
    await message.reply("Цитату з якого списку бажаєте відправити?",
                        reply_markup=users_choice_kb)


@dp.callback_query_handler(text_startswith="choice:", state='*')
async def form_citation_list(call: CallbackQuery):
    list_type = call.data.split(":")[1]
    if list_type == 'global_list':
        citat_list = await get_global_citat_list()
    else:
        citat_list = await get_user_citat_list(call.from_user.id)
    keyboard = CitationKeyboard(citat_list,
                                list_type,
                                user_id=call.from_user.id)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard.citations_keyboard)
    await call.message.edit_text(keyboard.message_text,
                                 reply_markup=markup)
    await call.answer()


@dp.callback_query_handler(text_startswith='page:', access=True, state='*')
async def change_page(call: CallbackQuery):
    await call.answer()
    calldata = call.data.split(":")
    purpose = \
    call.message.reply_markup.inline_keyboard[0][0]['callback_data'].split(
        ':')[0]
    user_id = int(calldata[3])
    list_type = calldata[2]
    page_start, page_end = calldata[1].split("-")
    if list_type == 'global_list':
        citat_list = await get_global_citat_list()
    else:
        citat_list = await get_user_citat_list(user_id)
    keyboard = CitationKeyboard(citat_list,
                                list_type,
                                purpose=purpose.split("_")[0],
                                user_id=user_id,
                                start=int(page_start))
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard.citations_keyboard)
    await call.message.edit_text(keyboard.message_text,
                                 reply_markup=markup)


@dp.callback_query_handler(text_contains='send_citation', access=True,
                           state='*')
async def send_citation(call: CallbackQuery):
    doc_id = call.data.split(":")[1]
    file_id, file_type, file_name = await get_citation(call.from_user.id,
                                                       doc_id)
    if file_id is None:
        await call.answer(text="Не вдалось знайти цитату             🔍❌\n"
                               "Можливо користувач її видалив ✉️➡️🗑",
                          show_alert=True)
    else:
        likes_kb = await form_like_dislike_kb(doc_id)
        if 'mpeg' in file_type:
            await call.message.answer_audio(file_id,
                                            caption=file_name,
                                            reply_markup=likes_kb)
        elif 'ogg' in file_type:
            await call.message.answer_voice(file_id,
                                            caption=file_name,
                                            reply_markup=likes_kb)
        await call.answer(text="Цитату надіслано")
