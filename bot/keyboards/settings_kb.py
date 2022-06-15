from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.database import get_user_private_setting


async def user_pivacy_kb(user_id):
    """ Create settings keyboard. """

    # Getting user's privacy setting to point in button current chose
    privacy = await get_user_private_setting(user_id)
    if privacy:
        user_privacy = '✅'
    elif privacy is None:
        user_privacy = '✅'
    else:
        user_privacy = '❌'
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"Приватність: {user_privacy}",
                                     callback_data=f'change_pivacy:{user_id}')
            ]
        ]
    )
    return kb
