from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, \
    InlineKeyboardMarkup

from loader import bot, dp

from data.database import get_citation, get_user_citat_list


# from bot.states.add_citation import AddingCitation

num_emojis = {1: '1️⃣',
              2: '2️⃣',
              3: '3️⃣',
              4: '4️⃣',
              5: '5️⃣',
              6: '6️⃣',
              7: '7️⃣',
              8: '8️⃣',
              9: '9️⃣',
              10: '🔟'}

@dp.message_handler(commands="citata", state='*')
async def form_citation_list(message: Message):
    citat_list = await get_user_citat_list(message.from_user.id)
    print(citat_list)
    name = list(citat_list.keys())
    print(name)
    msg_text = "Яку цитату бажаєте відправити?\n"
    kb = [InlineKeyboardButton(text=f'⬅️',
                                       callback_data=f'back')]
    for i, key in enumerate(name):
        msg_text += f"{i + 1}. {key};\n"
        kb.append(InlineKeyboardButton(text=f'{num_emojis[i + 1]}',
                                       callback_data=f'citat:{citat_list[key]}'))
    kb.append(InlineKeyboardButton(text=f'➡️', callback_data=f'forward'))
    keyboard = InlineKeyboardMarkup(inline_keyboard=[kb])

    await message.reply(msg_text, reply_markup=keyboard)


@dp.callback_query_handler(text_contains='citat')
async def send_citation(call: CallbackQuery):
    await call.answer()
    file_id, file_type = await get_citation(call.from_user.id, call.data.split(":")[1])
    print(file_id, file_type)
    if 'mpeg' in file_type:
        print('trying')
        await call.message.answer_audio(file_id)
    elif 'ogg' in file_type:
        await call.message.answer_voice(file_id)
