import asyncio
import motor.motor_asyncio

from bson import ObjectId

from data.config import MONGO_CLIENT
from bot.extract_info import extract_file_info, extract_user_info

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_CLIENT)
users_citation = client.users_citation
user_list = client.user_list['user_list']


async def collection_exists(coll):
    return bool(await coll.count_documents({}))


async def user_exists(user_id, coll=user_list):
    return await coll.find_one({'user_id': user_id})


async def reg_user(message, private=True):
    info = extract_user_info(message=message)
    if not await user_exists(user_id=info['user_id']):
        credentials = {
            'user_id': info['user_id'],
            'first_name': info['first_name'],
            'last_name': info['last_name'],
            'user_tag': info['username'],
            'user_liked': [],
            'user_disliked': [],
            'private': private
        }
        await user_list.insert_one(credentials)
        return user_list
    else:
        return False


async def add_citation(msg, file_name):
    chat_id, message_id, user_id, file_type, file_id, file_unique_id = extract_file_info(
        message=msg)
    citations = users_citation["all_citations"]
    credentials = {
        'file_name': file_name,
        'file_type': file_type,
        'file_id': file_id,
        'file_unique_id': file_unique_id,
        'chat_id': chat_id,
        'user_id': user_id,
        'message_id': message_id,
        'usage_count': 0,
        'likes': 0,
        'dislikes': 0,
        'private': True
    }
    await citations.insert_one(credentials)


async def set_like(citations_list, citation_id, likes_count):
    await citations_list.update_one({'_id': ObjectId(citation_id)},
                                    {'$set': {'likes': likes_count + 1}})


async def set_dislike(citations_list, citation_id, dislikes_count):
    await citations_list.update_one({'_id': ObjectId(citation_id)},
                                    {'$set': {'dislikes': dislikes_count + 1}})


async def increase_usages(citations_list, citation_id):
    await citations_list.update_one({'_id': ObjectId(citation_id)},
                                    {'$inc': {'usage_count': 1}})


async def get_citation(user_id, citation_id):
    citation = users_citation["all_citations"]
    result = await citation.find_one({'_id': ObjectId(citation_id)})
    if result is None:
        return None, None, None
    elif result['private'] and user_id != result['user_id']:
        return 'private', None, None
    await increase_usages(citation, citation_id)
    return result['file_id'], result['file_type'], result['file_name']


async def get_user_citat_list(user_id):
    citat_list = users_citation["all_citations"]
    result = {}
    async for citation in citat_list.find({'user_id': user_id},
                                          sort=[('usage_count', -1)]):
        result.update({citation['file_name']: citation['_id']})
    return result


async def get_global_citat_list():
    citat_list = users_citation["all_citations"]
    result = {}
    async for citation in citat_list.find({'private': False},
                                          sort=[('usage_count', -1)]):
        result.update({citation['file_name']: citation['_id']})
    return result


async def update_all(user_id):
    citat_list = users_citation[str(user_id)]
    await citat_list.update_many({}, {'$set': {'uses_count': 0}})


async def get_like_dislike_count(doc_id):
    citat_list = users_citation["all_citations"]
    result = await citat_list.find_one({'_id': ObjectId(doc_id)})
    return result['likes'], result['dislikes']


async def change_likes_count(user_id, doc_id, step):
    citat_list = users_citation["all_citations"]
    await citat_list.update_one({'_id': ObjectId(doc_id)},
                                {'$inc': {'likes': step}})
    liked_citations = (await user_list.find_one({'user_id': user_id}))['user_liked']
    if step > 0:
        liked_citations.append(doc_id)
        await user_list.update_one({'user_id': user_id},
                                   {'$set': {
                                       'user_liked': liked_citations}})
    elif step < 0:
        liked_citations.remove(doc_id)
        await user_list.update_one({'user_id': user_id},
                                   {'$set': {
                                       'user_liked': liked_citations}})


async def change_dislikes_count(user_id, doc_id, step):
    citat_list = users_citation["all_citations"]
    await citat_list.update_one({'_id': ObjectId(doc_id)},
                                {'$inc': {'dislikes': step}})
    disliked_citations = (await user_list.find_one({'user_id': user_id}))[
        'user_disliked']
    if step > 0:
        disliked_citations.append(doc_id)
        await user_list.update_one({'user_id': user_id},
                                   {'$set': {
                                       'user_disliked': disliked_citations}})
    elif step < 0:
        disliked_citations.remove(doc_id)
        await user_list.update_one({'user_id': user_id},
                                   {'$set': {
                                       'user_disliked': disliked_citations}})


async def user_reaction(message, doc_id):
    new_user = await reg_user(message)
    user_id = message.from_user.id
    if new_user:
        like = False
    else:
        user = await user_list.find_one({'user_id': user_id})
        liked_citations = user['user_liked']
        disliked_citations = user['user_disliked']
        if doc_id in liked_citations:
            like = 'like'
        elif doc_id in disliked_citations:
            like = 'dislike'
        else:
            like = False
    return like


async def get_user_private_setting(user_id):
    user = await user_list.find_one({'user_id': user_id})
    return user['private']


async def change_user_private_setting(user_id):
    citat_list = users_citation["all_citations"]
    privacy = await get_user_private_setting(user_id)
    await citat_list.update_many({'user_id': user_id},
                                 {'$set': {'private': not privacy}})
    await user_list.update_one({'user_id': user_id},
                                 {'$set': {'private': not privacy}})
    return not privacy
