from aiogram.types import CallbackQuery

from loader import bot, dp

from data.database import user_reaction, change_likes_count, \
    change_dislikes_count

from bot.keyboards.like_dislike_kb import form_like_dislike_kb


@dp.callback_query_handler(text_startswith="like:", state='*')
async def set_like(call: CallbackQuery):
    """ Catching pressed `like` button"""
    await call.answer()

    # Splitting to get citation id
    doc_id = call.data.split(":")[1]
    reaction = await user_reaction(message=call, doc_id=doc_id)
    if reaction == 'like':
        # If user already liked this we will remove like
        await change_likes_count(call.from_user.id, doc_id, -1)
    elif reaction == 'dislike':
        # If user disliked citation we will remove dislike and set like on it
        await change_likes_count(call.from_user.id, doc_id, 1)
        await change_dislikes_count(call.from_user.id, doc_id, -1)
    else:
        # If user has not reacted to this citation we will set like
        await change_likes_count(call.from_user.id, doc_id, 1)
    try:
        # trying to edit keyboard by the call object
        await call.message.edit_reply_markup(
            await form_like_dislike_kb(doc_id))
    except AttributeError:
        # If citation was sent by inline mode we have to edit it by inline_message_id
        await bot.edit_message_reply_markup(
            inline_message_id=call.inline_message_id,
            reply_markup=await form_like_dislike_kb(doc_id))


@dp.callback_query_handler(text_startswith="dislike:", state='*')
async def set_dislike(call: CallbackQuery):
    """ Catching pressed `dislike` button"""
    await call.answer()

    # Splitting to get citation id
    doc_id = call.data.split(":")[1]

    reaction = await user_reaction(message=call, doc_id=doc_id)

    if reaction == 'like':
        # If user liked citation we will remove like and set dislike on it
        await change_likes_count(call.from_user.id, doc_id, -1)
        await change_dislikes_count(call.from_user.id, doc_id, 1)
    elif reaction == 'dislike':
        # If user already disliked this we will remove dislike
        await change_dislikes_count(call.from_user.id, doc_id, -1)
    else:
        # If user has not reacted to this citation we will set dislike
        await change_dislikes_count(call.from_user.id, doc_id, 1)

    try:
        # trying to edit keyboard by the call object
        await call.message.edit_reply_markup(
            await form_like_dislike_kb(doc_id))
    except AttributeError:
        # If citation was sent by inline mode we have to edit it by inline_message_id
        await bot.edit_message_reply_markup(
            inline_message_id=call.inline_message_id,
            reply_markup=await form_like_dislike_kb(doc_id))
