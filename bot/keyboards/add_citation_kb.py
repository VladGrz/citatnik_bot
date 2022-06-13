from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


""" Keyboard to ask user whether he wants to add one more citation. """
add_or_cancel_adding_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Додати ще цитату", callback_data='continue'),
        ]
    ]
)