from datetime import datetime, timedelta
from config.config import JWT

import jwt
import time
from utils import set_key_in_cache, key_exists_in_cache
from fastapi import Depends, FastAPI, HTTPException
from starlette.status import HTTP_403_FORBIDDEN
from jwt import PyJWTError
from config.config import DB
from fastapi.security import OAuth2PasswordBearer
from bson.objectid import ObjectId

users = DB.users



async def create_access_token(data: dict, expires_delta: timedelta = None, admin = False):
    to_encode = data.copy()
    user_id = to_encode.get("user_id")
    if expires_delta:
        expire = time.time() + expires_delta
    else:
        expire = time.time() + JWT.get("ACCESS_TOKEN_EXPIRE_SECONDES_ADMIN" if admin else "ACCESS_TOKEN_EXPIRE_SECONDES")
    to_encode.update({"expires": expire})
    encoded_jwt = jwt.encode(to_encode, JWT.get("SECRET_KEY"), algorithm=JWT.get("ALGORITHM"))
    await set_key_in_cache(f"{user_id}", encoded_jwt, JWT.get("ACCESS_TOKEN_EXPIRE_SECONDES_ADMIN" if admin else "ACCESS_TOKEN_EXPIRE_SECONDES"))
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT.get("SECRET_KEY"), algorithms=[JWT.get("ALGORITHM")])
        return decoded_token if decoded_token and decoded_token.get("expires") >= time.time() else None
    except:
        return {}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )
    try:
        payload = decode_access_token(token)
        if not payload:
            raise credentials_exception
        user_id = payload.get("user_id", None)
        if user_id is None:
            raise credentials_exception
        else:
            if not await key_exists_in_cache(user_id):
                raise credentials_exception

    except PyJWTError:
        raise credentials_exception
    user = await users.find_one({ "_id": ObjectId(user_id) })
    if user is None:
        raise credentials_exception
    return payload