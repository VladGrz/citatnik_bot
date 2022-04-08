from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.database import get_like_dislike_count


async def form_like_dislike_kb(doc_id):
    likes, dislikes = await get_like_dislike_count(doc_id)
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
