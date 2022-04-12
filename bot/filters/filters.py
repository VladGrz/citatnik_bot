from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, CallbackQuery

from loader import bot, dp

from data.database import get_user_private_setting


class AccessFilter(BoundFilter):
    key = "access"

    def __init__(self, access):
        self.access = access

    async def check(self, call: CallbackQuery):
        callback_data = call.message.reply_markup.inline_keyboard[0][0][
            'callback_data']
        keys = callback_data.split(':')
        user_clicked = call.data.split(":")[0]
        user_id = int(keys[2])
        call_purpose = keys[0]
        owner_request = user_id == call.from_user.id
        user_private_status = await get_user_private_setting(user_id)
        print(user_clicked)
        strict_access = (
                    user_clicked != 'delete_citation' or user_clicked != 'sort_by')
        print(strict_access)
        if owner_request or (
                not user_private_status and not strict_access):
            return True
        elif user_private_status and user_clicked == 'page':
            await call.answer(
                "Ви не маєте доступу до цього повідомлення "
                "у зв'язку з налаштуваннями користувача.🤷‍♂️",
                show_alert=True)
            return False
        elif user_clicked == 'sort_by':
            await call.answer(
                "Ви не можете змінити тип сортування іншої людини 😜",
                show_alert=True)
            return False
        elif call_purpose == 'delete_citation':
            await call.answer(
                "Ви не можете видаляти чужі цитати😡",
                show_alert=True)
            return False
        else:
            await call.answer(
                "Ви не маєте доступу до цього повідомлення "
                "у зв'язку з налаштуваннями користувача.🤷‍♂️",
                show_alert=True)
            return False


dp.filters_factory.bind(AccessFilter)
