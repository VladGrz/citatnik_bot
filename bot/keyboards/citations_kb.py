from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.database import get_user_sort

# кнопки вибору цитати
""" 
кнопки вибору сторінки цитат
базово на 1 сторінці відображається вьсого 5 цитат, тому ці кнопки 
    будуть перемикати між набором цитат
"""


# def form_num_from_emojis(num):
#     res = ''
#     for i in str(num):
#         res += num_emojis[int(i)]
#     return res
#
#
# def form_page_buttons_text(list_len):
#     buttons_count = list_len // 6 if list_len % 6 == 0 else list_len // 6 + 1
#     buttons_names = []
#     num = 1
#     for i in range(0, buttons_count):
#         buttons_names.append(f"{num}-{num + 5}")
#         num += 6
#     return buttons_names
#
#
# async def form_message_text_and_buttons(start_mes, citat_list, kb, start, end):
#     names_list = list(citat_list.keys())[start:end]
#     for i, key in enumerate(names_list, start=start):
#         start_mes += f"{i + 1}. {key};\n"
#         button_text = form_num_from_emojis(i + 1)
#         calldata = f'citat:{citat_list[key]}'
#         kb[0].append(InlineKeyboardButton(text=f'{button_text}',
#                                           callback_data=calldata))
#     return start_mes
#
#
# async def form_page_buttons(citat_list, kb, list_type, user_id, start, end):
#     button_texts = form_page_buttons_text(len(citat_list))
#     page_line_end = 2  # this will point in which line to add page buttons
#     for i, page_num_text in enumerate(button_texts):
#         f, t = page_num_text.split("-")
#         if start + 1 == int(f) and end == int(t):
#             page_num_text += '✅'
#         callpagesdata = f'page:{page_num_text}:{list_type}:{user_id}'
#         kb[page_line_end - 1].append(InlineKeyboardButton(text=page_num_text,
#                                                           callback_data=callpagesdata))
#         # basicaly telegram can show only 8 buttons in a row
#         # so if we reached the limit we shoud add one more row of buttons
#         # and add new buttons to the new row
#         if i % 8 == 0 and i != 0:
#             kb.insert(page_line_end, [])
#             page_line_end += 1
#
#
# async def form_citation_list_kb(citat_list, list_type, user_id, start=None,
#                                 end=None):
#     # deciding page range (how many sitations will be displayed on a single page)
#     start = 0 if start is None else start - 1
#     end = start + 6 if end is None else end + 1
#
#     # forming list of user citations titles and list of citations titles
#     # for concrete page and basic keyboard
#     keys_list = list(citat_list.keys())
#     kb = [i.copy() for i in basic_structure]
#
#     # forming texts for page buttons (ex. 1-6, 7-12)
#     button_texts = form_page_buttons_text(len(keys_list))
#     msg_text = "Яку цитату бажаєте відправити?\n"
#
#     # forming message_text with first line buttons,
#     # which will point out user`s citation choice
#     msg_text = await form_message_text_and_buttons(msg_text, citat_list, kb, start, end)
#
#     # forming page buttons
#     await form_page_buttons(citat_list, kb, list_type, user_id, start, end)
#
#     keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
#     return msg_text, keyboard


class CitationKeyboard:
    basic_structure = [
        [],
        [],
        [
            InlineKeyboardButton("Назад↩️",
                                 callback_data="back_to:user_list_choice")
        ],
    ]
    num_emojis = {1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣', 5: '5️⃣', 6: '6️⃣',
                  7: '7️⃣', 8: '8️⃣', 9: '9️⃣', 0: '0️⃣'}
    sort_names = {'data': 'датою додання',
                  'usage_count': 'кількістю використань',
                  'likes': 'лайками',
                  'dislikes': 'дизлайками'}
    send_citation = "📨 Яку цитату бажаєте відправити?\n\n"
    delete_citation = "🗑 Яку цитату бажаєте видалити?\n\n"

    def __init__(self, citat_list, list_type, user_id, sort_type,
                 purpose='send', start=None, end=None):
        self.citations_keyboard = [i.copy() for i in self.basic_structure]
        self.start = 0 if start is None else start - 1
        self.end = self.start + 6 if end is None else end + 1
        self.full_citat_list = citat_list
        self.citat_list = self.full_citat_list[self.start:self.end]
        self.sort_by = self.sort_names[sort_type]
        self.button_texts = self.form_page_buttons_text()
        if purpose == 'send':
            self.message_text = self.send_citation
            self.callback_purpose = 'send_citation'
        else:
            self.message_text = self.delete_citation
            self.callback_purpose = 'delete_citation'
            self.citations_keyboard[2].pop(0)
        self.message_text += f'📊 Відсортовано за {self.sort_by}\n\n'
        if len(citat_list) == 0:
            self.message_text += 'Упс, здається в цьому списку немає цитат. ' \
                                 'Напишіть /new щоб додати цитату'
        else:
            self.citations_keyboard.insert(2, [InlineKeyboardButton(
                text=f'Змінити сортування 🔀',
                callback_data=f'sort_by:{sort_type}:{user_id}')])
        self.list_type = list_type
        self.user_id = user_id
        self.form_page_buttons()
        self.form_message_text_and_buttons()

    def form_page_buttons_text(self):
        list_len = len(self.full_citat_list)
        buttons_count = list_len // 6 if list_len % 6 == 0 else list_len // 6 + 1
        buttons_names = []
        num = 1
        for i in range(0, buttons_count):
            buttons_names.append(f"{num}-{num + 5}")
            num += 6
        return buttons_names

    def form_num_from_emojis(self, num):
        res = ''
        for i in str(num):
            res += self.num_emojis[int(i)]
        return res

    def form_citation(self, citation):
        cit_name = citation['file_name']
        likes = citation['likes']
        dislikes = citation['dislikes']
        usage_count = citation['usage_count']
        mes = f'{cit_name};\n    👍{likes}     👎{dislikes}     👁‍🗨{usage_count}\n'
        return mes

    def form_message_text_and_buttons(self):
        for i, citation in enumerate(self.citat_list, start=self.start):
            self.message_text += f"{i + 1}. {self.form_citation(citation)}"
            button_text = self.form_num_from_emojis(i + 1)
            calldata = f'{self.callback_purpose}:{citation["_id"]}:{self.user_id}'
            self.citations_keyboard[0].append(
                InlineKeyboardButton(text=f'{button_text}',
                                     callback_data=calldata))
        return

    def form_page_buttons(self):
        page_line_end = 2  # this will point in which line to add page buttons
        for i, page_num_text in enumerate(self.button_texts):
            f, t = page_num_text.split("-")
            if self.start + 1 == int(f) and self.end == int(t):
                page_num_text += '✅'
            callpagesdata = f'page:{page_num_text}:{self.list_type}:{self.user_id}'
            self.citations_keyboard[page_line_end - 1].append(
                InlineKeyboardButton(text=page_num_text,
                                     callback_data=callpagesdata))
            # basicaly telegram can show only 8 buttons in a row
            # so if we reached the limit we shoud add one more row of buttons
            # and add new buttons to the new row
            if i % 3 == 0 and i != 0:
                self.citations_keyboard.insert(page_line_end, [])
                page_line_end += 1
        return
