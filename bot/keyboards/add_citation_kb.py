from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

add_or_cancel_adding_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Додати ще цитату", callback_data='continue'),
        ]
    ]
)