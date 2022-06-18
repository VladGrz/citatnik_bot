from aiogram.types import Message, InlineQuery, \
    InlineQueryResultCachedDocument, InlineQueryResultCachedVoice, \
    InlineQueryResultCachedVideo, ChosenInlineResult

from loader import dp

from data.database import get_user_citat_list, get_global_citat_list, \
    increase_usages

from bot.keyboards.like_dislike_kb import form_like_dislike_kb


async def get_fake_results(start_num, citations_list, size=50):
    if start_num >= len(citations_list):
        return []
    elif start_num + size >= len(citations_list):
        return citations_list[start_num: len(citations_list)]
    else:
        return citations_list[start_num: start_num+size]


@dp.inline_handler()
async def search_result(query: InlineQuery):
    """ Catches inline request from user. """

    # If user specifies '-global' parameter after bot`s tag we have to show
    # global citations list
    # Variable 'search' will keep user`s name of citation
    # If he would like to search specific citation
    if query.query.startswith('-global'):
        try:
            search = query.query.lower()[7:].lstrip()
        except IndexError:
            # if there is no search for specific citation so search is ''
            search = ''
        citations = await get_global_citat_list(query.from_user.id, search)
    else:
        search = query.query.lower()
        citations = await get_user_citat_list(query.from_user.id, search)

    # There will be all results saved to show in query result
    audio_result = []
    query_offset = int(query.offset) if query.offset else 1
    for citation in await get_fake_results(query_offset, citations):

        # Creating id for specific result
        hashed_id: str = str(citation['_id'])

        # Like/dislike keyboard for citation which will be pinned to message
        markup = await form_like_dislike_kb(citation['_id'])

        # Checking file type to form special result
        # caption variable is the text which will be displayed in the message
        if citation['file_type'] == 'audio/ogg':
            # Forming voice result
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
            # Forming audio result
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
            # Forming video result
            audio_result.append(
                InlineQueryResultCachedVideo(
                    id=hashed_id,
                    video_file_id=citation['file_id'],
                    caption=citation['file_name'],
                    title=citation['file_name'],
                    reply_markup=markup
                )
            )
    # Forming menu which will be displayed on top of the input box
    # after typing a teg of the bot
    # cache time variable says how long after using bot it will remember the result
    # in our case it`s better to set it as 1, to form new list every time
    # when user request this menu

    # Switch parameter and text defines text of the inline button
    # and command which will be transferred to bot
    if len(audio_result) < 50:
        # If length of result is less than 50 we have no more results to show
        # and next_offset will be empty
        await query.answer(audio_result,
                           cache_time=1,
                           is_personal=True,
                           next_offset="",
                           switch_pm_text="Додати цитату",
                           switch_pm_parameter='add')
    else:
        # If length is bigger than 50 we have to set next_offset to show them
        await query.answer(audio_result,
                           cache_time=1,
                           is_personal=True,
                           next_offset=str(query_offset+50),
                           switch_pm_text="Додати цитату",
                           switch_pm_parameter='add')

@dp.chosen_inline_handler()
async def chosen_inline_result(chosen_result: ChosenInlineResult):
    # Increasing usages if citation was used in inline mode
    await increase_usages(chosen_result.result_id)
