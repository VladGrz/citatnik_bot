import hashlib

from aiogram.types import Message, InlineQuery, \
    InlineQueryResultCachedDocument, InlineQueryResultCachedVoice, \
    InlineQueryResultCachedVideo

from loader import dp

from data.database import get_user_citat_list, get_global_citat_list

from bot.keyboards.like_dislike_kb import form_like_dislike_kb


@dp.inline_handler()
async def search_result(query: InlineQuery):
    if query.query.startswith('-global'):
        try:
            search = query.query.lower()[7:].lstrip()
        except IndexError:
            search = ''
        citations = await get_global_citat_list(search)
    else:
        search = query.query.lower()
        citations = await get_user_citat_list(query.from_user.id, search)
    audio_result = []
    for citation in citations:
        hashed_id: str = hashlib.md5(
            citation['file_name'].encode()).hexdigest()
        markup = await form_like_dislike_kb(citation['_id'])
        if citation['file_type'] == 'audio/ogg':
            audio_result.append(
                InlineQueryResultCachedVoice(
                    id=hashed_id,
                    voice_file_id=citation['file_id'],
                    caption=citation['file_name'],
                    title=citation['file_name'],
                    reply_markup=markup
                )
            )
        elif citation['file_type'] == 'audio/mpeg':
            audio_result.append(
                InlineQueryResultCachedDocument(
                    id=hashed_id,
                    document_file_id=citation['file_id'],
                    caption=citation['file_name'],
                    title=citation['file_name'],
                    reply_markup=markup
                )
            )
        else:
            audio_result.append(
                InlineQueryResultCachedVideo(
                    id=hashed_id,
                    video_file_id=citation['file_id'],
                    caption=citation['file_name'],
                    title=citation['file_name'],
                    reply_markup=markup
                )
            )
    print(await query.answer(audio_result,
                             cache_time=1,
                             is_personal=True, 
                             switch_pm_text="Додати цитату",
                             switch_pm_parameter='add'))
