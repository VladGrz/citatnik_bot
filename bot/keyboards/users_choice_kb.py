from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

""" Keyboard to chose list of citations(private or global). """
users_choice_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Глобальний",
                                 callback_data='choice:global_list'),
            InlineKeyboardButton("Особистий",
                                 callback_data='choice:private_list')
        ]
    ]
)