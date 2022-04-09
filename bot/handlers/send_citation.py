from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, \
    InlineKeyboardMarkup

from loader import bot, dp

from data.database import get_citation, get_user_citat_list, \
    get_global_citat_list

from bot.keyboards.like_dislike_kb import form_like_dislike_kb
from bot.keyboards.users_choice_kb import users_choice_kb
from bot.keyboards.citations_kb import form_citation_list_kb

# from bot.states.add_citation import AddingCitation

num_emojis = {1: '1️⃣',
              2: '2️⃣',
              3: '3️⃣',
              4: '4️⃣',
              5: '5️⃣',
              6: '6️⃣',
              7: '7️⃣',
              8: '8️⃣',
              9: '9️⃣',
              10: '🔟'}


@dp.callback_query_handler(text_startswith='back_to:', state="*")
async def users_choice_citats_list(call: CallbackQuery):
    await call.message.edit_text("Цитату з якого списку бажаєте відправити?",
                                 reply_markup=users_choice_kb)


@dp.message_handler(commands='citata', state='*')
async def users_choice_citats_list(message: Message):
    await message.reply("Цитату з якого списку бажаєте відправити?",
                        reply_markup=users_choice_kb)


@dp.callback_query_handler(text_startswith="choice:", state='*')
async def form_citation_list(call: CallbackQuery):
    user_choice = call.data.split(":")[1]
    if user_choice == 'global_list':
        citat_list = await get_global_citat_list()
    else:
        citat_list = await get_user_citat_list(call.from_user.id)
    msg_text, keyboard = await form_citation_list_kb(citat_list,
                                                     user_choice,
                                                     user_id=call.from_user.id)
    await call.message.edit_text(msg_text, reply_markup=keyboard)


@dp.callback_query_handler(text_startswith='page:', state='*')
async def change_page(call: CallbackQuery):
    calldata = call.data.split(":")
    user_id = int(calldata[3])
    list_type = calldata[2]
    page_start, page_end = calldata[1].split("-")
    if list_type == 'global_list':
        citat_list = await get_global_citat_list()
    else:
        citat_list = await get_user_citat_list(user_id)
    msg_text, keyboard = await form_citation_list_kb(citat_list,
                                                     list_type,
                                                     user_id=user_id,
                                                     start=int(page_start))
    await call.message.edit_text(msg_text, reply_markup=keyboard)


@dp.callback_query_handler(text_contains='citat', state='*')
async def send_citation(call: CallbackQuery):
    doc_id = call.data.split(":")[1]
    file_id, file_type, file_name = await get_citation(call.from_user.id,
                                                       doc_id)

    if file_id == 'private':
        await call.answer(text="Власник заборонив доступ до своїх цитат",
                          show_alert=True)
    elif file_id is None:
        await call.answer(text="Не вдалось знайти цитату", show_alert=True)
    else:
        likes_kb = await form_like_dislike_kb(doc_id)
        if 'mpeg' in file_type:
            await call.message.answer_audio(file_id,
                                            reply_markup=likes_kb)
        elif 'ogg' in file_type:
            await call.message.answer_voice(file_id,
                                            reply_markup=likes_kb)
        await call.answer(text="Цитату надіслано")
