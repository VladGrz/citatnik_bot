from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.database import get_like_dislike_count


async def form_like_dislike_kb(doc_id):
    """ Creating keyboard for likes/dislikes. """

    # Getting current number of likes and dislikes to show them in buttons
    likes, dislikes = await get_like_dislike_count(doc_id)

    # In callback data we have to specify id of the citation
    # to know which citation these buttons are for
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(f'👍 {likes}',
                                     callback_data=f'like:{doc_id}'),
                InlineKeyboardButton(f'👎 {dislikes}',
                                     callback_data=f'dislike:{doc_id}')
            ]
        ]
    )
    return kb
