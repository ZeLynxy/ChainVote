from config.config import CACHE_DB
from uuid import uuid4
from bson.objectid import ObjectId

from config.config import DB
from users.utils import *

users = DB.users


################## CACHE ################
async def key_exists_in_cache(key):
    return await CACHE_DB.cache.exists(key)

async def get_key_from_cache(key):
    return await CACHE_DB.cache.get(key)


async def set_key_in_cache(key, value, expire=0):
    await CACHE_DB.cache.set(key, value, expire=expire)

async def delete_key_from_cache(key):
    await CACHE_DB.cache.delete(key)


def generate_ID():
    return str(uuid4())



########### USERS AUTHORIZATION ####################
async def current_user_can_do_request(current_user_id, user_id_on, role=None):
    if isinstance(user_id_on, list) :
        if current_user_id in user_id_on:
            return True
    else:
        if current_user_id == user_id_on:
            return True
    
    user = await users.find_one({ "_id": ObjectId(current_user_id) })
    return user.get("role") == role or user.get("role") == UserRole.admin


async def get_role(user_id):
    user = await users.find_one({ "_id": ObjectId(user_id) })
    return user.get("role", None)


async def current_user_is_admin(current_user_id):
    return await get_role(current_user_id) == UserRole.admin



