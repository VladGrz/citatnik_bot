from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# кнопки вибору цитати
""" 
кнопки вибору сторінки цитат
базово на 1 сторінці відображається вьсого 5 цитат, тому ці кнопки 
    будуть перемикати між набором цитат
"""
basic_structure = [
    [
    ],
    [
    ],
    [
        InlineKeyboardButton("Назад↩️",
                             callback_data="back_to:user_list_choice")
    ],
]

num_emojis = {1: '1️⃣',
              2: '2️⃣',
              3: '3️⃣',
              4: '4️⃣',
              5: '5️⃣',
              6: '6️⃣',
              7: '7️⃣',
              8: '8️⃣',
              9: '9️⃣',
              0: '0️⃣'}


def form_num_from_emojis(num):
    res = ''
    for i in str(num):
        res += num_emojis[int(i)]
    return res


def form_page_buttons_text(list_len):
    buttons_count = list_len // 6 if list_len % 6 == 0 else list_len // 6 + 1
    buttons_names = []
    num = 1
    for i in range(0, buttons_count):
        buttons_names.append(f"{num}-{num + 5}")
        num += 6
    return buttons_names


async def form_citation_list_kb(citat_list, list_type, user_id, start=None, end=None):
    start = 0 if start is None else start - 1
    end = start + 6 if end is None else end + 1
    keys_list = list(citat_list.keys())
    name = keys_list[start:end]
    button_texts = form_page_buttons_text(len(keys_list))
    msg_text = "Яку цитату бажаєте відправити?\n"
    kb = [i.copy() for i in basic_structure]
    page_line_end = 2
    for i, key in enumerate(name, start=start):
        msg_text += f"{i + 1}. {key};\n"
        button_text = form_num_from_emojis(i + 1)
        calldata = f'citat:{citat_list[key]}'
        kb[0].append(InlineKeyboardButton(text=f'{button_text}',
                                          callback_data=calldata))
    for i, page_num_text in enumerate(button_texts):
        f, t = page_num_text.split("-")
        if start+1 == int(f) and end == int(t):
            page_num_text += '✅'
        callpagesdata = f'page:{page_num_text}:{list_type}:{user_id}'
        kb[page_line_end - 1].append(InlineKeyboardButton(text=page_num_text,
                                                          callback_data=callpagesdata))
        if i % 8 == 0 and i != 0:
            kb.insert(page_line_end, [])
            page_line_end += 1

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return msg_text, keyboard
