import asyncio
import motor.motor_asyncio

from bson import ObjectId

from data.config import MONGO_CLIENT
from bot.extract_info import extract_file_info

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_CLIENT)
users_citation = client.users_citation
user_list = client.user_list


async def collection_exists(coll):
    return bool(await coll.count_documents({}))


async def user_exists(coll, user_id):
    return await coll.find_one({'user_id': user_id})


async def reg_user(user_id, first_name=None,
                   last_name=None, username=None,
                   private=True):
    us_list = user_list['user_list']
    if not await user_exists(us_list, user_id):
        credentials = {
            'user_id': user_id,
            'first_name': first_name,
            'last_name': last_name,
            'user_tag': username,
            'private': private
        }
        await us_list.insert_one(credentials)
        return us_list
    else:
        return False


async def add_citation(msg, file_name):
    chat_id, message_id, user_id, file_type, file_id, file_unique_id = extract_file_info(message=msg)
    citations = users_citation[str(user_id)]
    credentials = {
        'file_name': file_name,
        'file_type': file_type,
        'file_id': file_id,
        'file_unique_id': file_unique_id,
        'chat_id': chat_id,
        'message_id': message_id
    }
    await citations.insert_one(credentials)


async def get_citation(user_id, citation_id):
    citation = users_citation[str(user_id)]
    result = await citation.find_one({'_id': ObjectId(citation_id)})
    return result['file_id'], result['file_type']


async def get_user_citat_list(user_id):
    citat_list = users_citation[str(user_id)]
    result = {}
    async for citation in citat_list.find({}):
        result.update({citation['file_name']: citation['_id']})
    return result
