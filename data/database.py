"""
There are functions for working with MongoDB`s database.
"""

import re

import motor.motor_asyncio

from bson import ObjectId, Regex

from data.config import MONGO_CLIENT
from bot.extract_info import extract_file_info, extract_user_info

# Creating client through which app will connect to MongoDB server
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_CLIENT)

# Creating two points through which we will connect to collections
user_list = client.user_list['user_list']
citat_list = client.users_citation["all_citations"]


async def collection_exists(coll):
    return bool(await coll.count_documents({}))


async def user_exists(user_id, coll=user_list):
    """ Check if user is already registered in db. """

    return await coll.find_one({'user_id': user_id})


async def reg_user(message, private=True):
    """ Register user in db. """

    # Extracting info about user
    info = extract_user_info(message=message)

    if not await user_exists(user_id=info['user_id']):
        # Making JSON-format document to write into collection
        credentials = {
            'user_id': info['user_id'],
            'first_name': info['first_name'],
            'last_name': info['last_name'],
            'user_tag': info['username'],
            'user_liked': [],
            'user_disliked': [],
            'private': private,
            'sort_key': 'data'
        }
        # Inserting new document into collection
        await user_list.insert_one(credentials)
        return user_list
    else:
        return False


async def add_citation(msg, file_name):
    """ Add citation. """

    # Extracting info about file
    chat_id, message_id, user_id, file_type, file_id, file_unique_id = extract_file_info(
        message=msg)

    # Getting user privacy setting to make new citation`s privacy setting
    # the same as user`s one
    privacy = await get_user_private_setting(user_id)

    # If no privacy setting was found so the user does not exist,
    # and we should register him
    if privacy is None:
        await reg_user(msg)
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
        'private': privacy
    }
    await citat_list.insert_one(credentials)


async def increase_usages(citation_id):
    """ Increase usages count if someone uses citation. """
    await citat_list.update_one({'_id': ObjectId(citation_id)},
                                {'$inc': {'usage_count': 1}})


async def get_user_sort(user_id):
    """ Get user`s sort type. """
    user = await user_list.find_one({'user_id': user_id})
    try:
        return user['sort_key']
    except KeyError:
        # If user has no sort type, we will create this field in document
        # and return basic sort type
        await user_list.update_one({'user_id': user_id},
                                   {'$set': {'sort_key': 'data'}})
        return 'data'
    except TypeError:
        return 'data'


async def change_user_sort(user_id):
    """ Change user`s sort type. """

    # Defining all possible sort types
    sort_types = ['data', 'usage_count', 'likes', 'dislikes']

    # Getting user fom BD by his id
    user = await user_list.find_one({'user_id': user_id})
    try:
        # Getting user`s current sort`s type index and increasing it by 1
        # to switch to the new sort type from the list
        next_sort = sort_types.index(user['sort_key']) + 1
    except TypeError:
        return False

    # Checking whether next index is equal to the number of sort types
    if next_sort == len(sort_types):
        # if it is then the next sort type will be the first one from the list
        next_sort = 0

    # Setting new sort type for the user
    await user_list.update_one({'user_id': user_id},
                               {'$set': {'sort_key': sort_types[next_sort]}})
    return sort_types[next_sort]


async def get_citation(user_id, citation_id):
    """ Get citation by its _id. """
    result = await citat_list.find_one({'_id': ObjectId(citation_id)})

    # Checking if citation exists
    if result is None:
        return None, None, None
    elif result['private'] and user_id != result['user_id']:
        # If requested citation is private
        # and user who requested it isn`t the owner
        # we return 'private' message to forbid the access
        return 'private', None, None

    # If all is good we will increase citation usages
    # and return necessary variables to send citation
    await increase_usages(citation_id)
    return result['file_id'], result['file_type'], result['file_name']


async def get_user_citat_list(user_id, starts_with=''):
    """ Get citation list of the user. """

    # Making regex pattern to find citations by their beginning
    pattern = re.compile(f'^{starts_with}', re.I)
    regex = Regex.from_native(pattern)
    regex.flags ^= re.UNICODE

    all_citats = []
    sort_by = await get_user_sort(user_id)

    # Using {'$regex': regex} as a parameter for 'file_name'
    # we say that we want to get citations,
    # names of which correspond only with our filter
    async for citation in citat_list.find({'user_id': user_id,
                                           'file_name': {
                                               '$regex': regex}
                                           },
                                          sort=[(sort_by, -1)]):
        all_citats.append(citation)
    return all_citats


async def get_global_citat_list(user_id, starts_with=''):
    """ Get global citations list. """
    # Making regex pattern to find citations by their beginning
    pattern = re.compile(f'^{starts_with}', re.I)
    regex = Regex.from_native(pattern)
    regex.flags ^= re.UNICODE

    all_citats = []
    sort_by = await get_user_sort(user_id)

    # Using {'$regex': regex} as a parameter for 'file_name'
    # we say that we want to get citations,
    # names of which correspond only with our filter
    async for citation in citat_list.find({'file_name': {'$regex': regex},
                                           'private': False},
                                          sort=[(sort_by, -1)]):
        all_citats.append(citation)
    return all_citats


async def get_like_dislike_count(doc_id):
    """ Get number of likes and dislikes of the citation. """
    result = await citat_list.find_one({'_id': ObjectId(doc_id)})
    return result['likes'], result['dislikes']


async def change_likes_count(user_id, doc_id, step):
    """ Change likes count. """

    # Increasing likes count by a step
    # It could be negative and positive, so the likes count will be increased
    # or decreased
    await citat_list.update_one({'_id': ObjectId(doc_id)},
                                {'$inc': {'likes': step}})

    # Getting list of citations that user liked
    liked_citations = (await user_list.find_one({'user_id': user_id}))[
        'user_liked']
    # If step is positive we will append id of citation which user liked
    # Else we will remove that id from the list
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
    """ Change dislikes count. """

    # Increasing dislikes count by a step
    # It could be negative and positive, so the likes count will be increased
    # or decreased
    await citat_list.update_one({'_id': ObjectId(doc_id)},
                                {'$inc': {'dislikes': step}})

    # Getting list of citations that user liked
    disliked_citations = (await user_list.find_one({'user_id': user_id}))[
        'user_disliked']

    # If step is positive we will append id of citation which user disliked
    # Else we will remove that id from the list
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
    """ Get user's reaction to the citation. """

    # Trying to register user
    new_user = await reg_user(message)
    user_id = message.from_user.id

    # if user is new so user has no reaction to that citation at all
    if new_user:
        like = False
    else:
        # Getting user from bd
        user = await user_list.find_one({'user_id': user_id})

        # Getting list of citations that user liked
        liked_citations = user['user_liked']

        # Getting list of citations that user disliked
        disliked_citations = user['user_disliked']

        # Checking if citation id is in any list
        # If id is in liked citations list so the reaction is 'like'
        # and vice versa, but if id does not exist in any list
        # it means user has not reacted to that citation
        if doc_id in liked_citations:
            like = 'like'
        elif doc_id in disliked_citations:
            like = 'dislike'
        else:
            like = False
    return like


async def get_user_private_setting(user_id):
    """ Get user's privacy setting. """
    user = await user_list.find_one({'user_id': user_id})
    try:
        return user['private']
    except KeyError:
        return None


async def change_user_private_setting(user_id):
    """ Change user's privacy setting. """

    # Getting current privacy setting
    privacy = await get_user_private_setting(user_id)
    if privacy is None:
        return None

    # Changing privacy setting for all user`s citations
    await citat_list.update_many({'user_id': user_id},
                                 {'$set': {'private': not privacy}})

    # Changing general user privacy setting
    await user_list.update_one({'user_id': user_id},
                               {'$set': {'private': not privacy}})
    return not privacy


async def delete_user_citation(citation_id):
    """ Deleting citation by its id. """
    await citat_list.delete_one({'_id': ObjectId(citation_id)})
    return
