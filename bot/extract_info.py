def extract_user_info(message=None):
    """ Extract info about User from message. """
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    return {'user_id': user_id,
            'first_name': first_name,
            'last_name': last_name,
            'username': username}


def extract_file_info(message=None, call=None):
    """ Extract info about file. """
    msg_id = message.message_id
    cht_id = message.chat.id
    usr_id = message.from_user.id
    file = message.audio
    if not file:
        file = message.voice
    file_id = file.file_id
    file_uniq_id = file.file_unique_id
    file_type = file.mime_type
    return cht_id, msg_id, usr_id, file_type, file_id, file_uniq_id

