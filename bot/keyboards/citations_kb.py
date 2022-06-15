from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.database import get_user_sort

# кнопки вибору цитати
""" 
кнопки вибору сторінки цитат
базово на 1 сторінці відображається вьсого 5 цитат, тому ці кнопки 
    будуть перемикати між набором цитат
"""


class CitationKeyboard:
    """ Class to form message with citations list and keyboard. """

    # Basic structure of keyboard, first line will contain buttons
    # pressing which we will request the citation from the list in the message.
    # Second line will contain buttons pressing which we will change the page.
    # If there are many pages we will add more lines after the second one.
    # The last line is for "Back" button to switch to previous menu.
    basic_structure = [
        [],
        [],
        [
            InlineKeyboardButton("Назад↩️",
                                 callback_data="back_to:user_list_choice")
        ],
    ]

    # Dict to convert numbers to emojis
    num_emojis = {1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣', 5: '5️⃣', 6: '6️⃣',
                  7: '7️⃣', 8: '8️⃣', 9: '9️⃣', 0: '0️⃣'}

    # Dict to convert sort type from BD to humanreadable format
    sort_names = {'data': 'датою додання',
                  'usage_count': 'кількістю використань',
                  'likes': 'лайками',
                  'dislikes': 'дизлайками'}
    send_citation = "📨 Яку цитату бажаєте відправити?\n\n"
    delete_citation = "🗑 Яку цитату бажаєте видалити?\n\n"

    def __init__(self, citat_list, list_type, user_id, sort_type,
                 purpose='send', start=None, end=None):
        # Copying template of the keyboard
        self.citations_keyboard = [i.copy() for i in self.basic_structure]

        # Defining start number of citation(page) and end number
        self.start = 0 if start is None else start - 1
        self.end = self.start + 6 if end is None else end + 1

        # Saving full citation list use in future and slicing it to form
        # list of citations for current page
        self.full_citat_list = citat_list
        self.citat_list = self.full_citat_list[self.start:self.end]

        self.sort_by = self.sort_names[sort_type]
        self.button_texts = self.form_page_buttons_text()

        # Checking the purpose of the message to form callback purpose
        # and message's first line
        if purpose == 'send':
            self.message_text = self.send_citation
            self.callback_purpose = 'send_citation'
        else:
            self.message_text = self.delete_citation
            self.callback_purpose = 'delete_citation'
            # if user wants to delete citation there will be no 'Back' button
            self.citations_keyboard[2].pop(0)
        self.message_text += f'📊 Відсортовано за {self.sort_by}\n\n'
        if len(citat_list) == 0:
            self.message_text += 'Упс, здається в цьому списку немає цитат. ' \
                                 'Напишіть /new щоб додати цитату'
        else:
            # If there are citations new button with sort changing will be displayed
            self.citations_keyboard.insert(2, [InlineKeyboardButton(
                text=f'Змінити сортування 🔀',
                callback_data=f'sort_by:{sort_type}:{user_id}')])
        self.list_type = list_type
        self.user_id = user_id
        self.form_page_buttons()
        self.form_message_text_and_buttons()

    def form_page_buttons_text(self):
        """ Forming text for each page button. """
        list_len = len(self.full_citat_list)

        # Defining how many buttons of pages will be.
        # Bot will show 6 citations per page so page number we can get by
        # dividing overall number of citations by 6 and if remainder is doesn`t
        # equals to 0 we should add one more button
        buttons_count = list_len // 6 if list_len % 6 == 0 else list_len // 6 + 1
        buttons_names = []
        num = 1
        for i in range(0, buttons_count):
            # Forming page button text
            # in which range of citations number will be shown
            buttons_names.append(f"{num}-{num + 5}")
            num += 6
        return buttons_names

    def form_num_from_emojis(self, num):
        """ Forming number from emojis. For example 14 is 1️⃣4️⃣"""

        res = ''
        for i in str(num):
            res += self.num_emojis[int(i)]
        return res

    def form_citation(self, citation):
        """ Forming the appearance of a citation in message. """
        cit_name = citation['file_name']
        likes = citation['likes']
        dislikes = citation['dislikes']
        usage_count = citation['usage_count']
        mes = f'{cit_name};\n    👍{likes}     👎{dislikes}     👁‍🗨{usage_count}\n'
        return mes

    def form_message_text_and_buttons(self):
        """ Forming message and first line of the buttons. """

        for i, citation in enumerate(self.citat_list, start=self.start):
            self.message_text += f"{i + 1}. {self.form_citation(citation)}"
            button_text = self.form_num_from_emojis(i + 1)
            calldata = f'{self.callback_purpose}:{citation["_id"]}:{self.user_id}'
            self.citations_keyboard[0].append(
                InlineKeyboardButton(text=f'{button_text}',
                                     callback_data=calldata))
        return

    def form_page_buttons(self):
        """ Forming rows of page buttons. """

        page_line_end = 2  # this will point in which line to add page buttons
        for i, page_num_text in enumerate(self.button_texts):
            f, t = page_num_text.split("-")
            # There we are checking whether start and end citation number
            # equals to the current page. If it is so this page will be marked
            # as current by '✅' emoji at the end.
            if self.start + 1 == int(f) and self.end == int(t):
                page_num_text += '✅'
            callpagesdata = f'page:{page_num_text}:{self.list_type}:{self.user_id}'

            # We are adding our button to the page row
            self.citations_keyboard[page_line_end - 1].append(
                InlineKeyboardButton(text=page_num_text,
                                     callback_data=callpagesdata))

            # basically telegram can show only 8 buttons in a row
            # so if we reached the limit we should add one more row of buttons
            # and add new buttons to the new row
            if i % 3 == 0 and i != 0:
                self.citations_keyboard.insert(page_line_end, [])
                page_line_end += 1
        return
