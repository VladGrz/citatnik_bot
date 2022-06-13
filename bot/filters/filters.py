from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, CallbackQuery

from loader import bot, dp

from data.database import get_user_private_setting


class AccessFilter(BoundFilter):
    """ Filter for access check. """

    # Defining key which we should use in handler
    key = "access"

    def __init__(self, access):
        self.access = access

    async def check(self, call: CallbackQuery):
        """ Checking whether user has access to the message. """

        # Extracting callback data from the call
        callback_data = call.message.reply_markup.inline_keyboard[0][0][
            'callback_data']

        # Splitting by ":" to get keys
        keys = callback_data.split(':')

        # Saving what button user clicked,
        # user_id from the call (not the user id who clicked the button,
        # but the user who owns this message)
        user_clicked = call.data.split(":")[0]
        user_id = int(keys[2])
        call_purpose = keys[0]

        # checking whether user's id who clicked the button equals
        # to the id of owner of the message
        owner_request = user_id == call.from_user.id

        # Getting owner privacy setting
        user_private_status = await get_user_private_setting(user_id)

        # Defining strict access, because only owners can delete their citation
        # and change sort type
        strict_access = (
                    user_clicked == 'delete_citation' or user_clicked == 'sort_by')

        # If request is from owner, or owners privacy setting allows other user
        # access to the citation and access is not strict, so we allow request
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
