from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.database import get_user_private_setting


async def user_pivacy_kb(user_id):
    user_privacy = '✅' if await get_user_private_setting(user_id) else '❌'
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"Приватність: {user_privacy}",
                                     callback_data=f'change_pivacy:{user_id}')
            ]
        ]
    )
    return kb
