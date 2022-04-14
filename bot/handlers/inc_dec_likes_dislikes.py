from aiogram.types import CallbackQuery, InlineKeyboardButton, \
    InlineKeyboardMarkup

from loader import bot, dp

from data.database import user_reaction, change_likes_count, \
    change_dislikes_count

from bot.keyboards.like_dislike_kb import form_like_dislike_kb


@dp.callback_query_handler(text_startswith="like:", state='*')
async def set_like(call: CallbackQuery):
    await call.answer()
    doc_id = call.data.split(":")[1]
    reaction = await user_reaction(message=call, doc_id=doc_id)
    if reaction == 'like':
        await change_likes_count(call.from_user.id, doc_id, -1)
    elif reaction == 'dislike':
        await change_likes_count(call.from_user.id, doc_id, 1)
        await change_dislikes_count(call.from_user.id, doc_id, -1)
    else:
        await change_likes_count(call.from_user.id, doc_id, 1)
    try:
        await call.message.edit_reply_markup(
            await form_like_dislike_kb(doc_id))
    except AttributeError:
        await bot.edit_message_reply_markup(
            inline_message_id=call.inline_message_id,
            reply_markup=await form_like_dislike_kb(doc_id))


@dp.callback_query_handler(text_startswith="dislike:", state='*')
async def set_dislike(call: CallbackQuery):
    await call.answer()
    doc_id = call.data.split(":")[1]
    print(call)
    reaction = await user_reaction(message=call, doc_id=doc_id)
    if reaction == 'like':
        await change_likes_count(call.from_user.id, doc_id, -1)
        await change_dislikes_count(call.from_user.id, doc_id, 1)
    elif reaction == 'dislike':
        await change_dislikes_count(call.from_user.id, doc_id, -1)
    else:
        await change_dislikes_count(call.from_user.id, doc_id, 1)
    try:
        await call.message.edit_reply_markup(
            await form_like_dislike_kb(doc_id))
    except AttributeError:
        await bot.edit_message_reply_markup(
            inline_message_id=call.inline_message_id,
            reply_markup=await form_like_dislike_kb(doc_id))
