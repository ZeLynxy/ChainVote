from fastapi import APIRouter, BackgroundTasks, Depends

from bson.objectid import ObjectId
import bcrypt
from fastapi import Request
from config.config import DB
from .utils import *
import datetime
from utils import *
from utils.jwt_authorization import  create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm

import main

users_router = APIRouter()
users = DB.users




@users_router.post("/register")
async def add_user_data(data: dict, background_tasks: BackgroundTasks):

    username = data.get("username")
    email = data.get("email", "")
    phone = data.get("phone")
    firstname =  data.get("firstname")
    lastname = data.get("lastname")
    gender = data.get('gender')
    national_id = data.get("national_id")
    password = bcrypt.hashpw(data.get("password").encode('utf-8'), bcrypt.gensalt())


    user_exists = await users.find_one({
                                            "$or" : [
                                                        {'username' : username},
                                                        {'email' : email},
                                                        {'national_id': national_id}
                                                    ]
                                            
                                            }
                                        )
    if not user_exists:
        if is_valid_email(email):
            result_user = await users.insert_one({
                    "username": username,
                    "email" : email,
                    "phone": phone,
                    "firstname": firstname,
                    "lastname": lastname,
                    "gender": gender,
                    "national_id": national_id,
                    "password": password,
                    "created_on": datetime.datetime.now(),
                    "updated_on": datetime.datetime.now(),
                    "role": UserRole.voter,
                    "account_status": UserAccountStatus.registered,
                })

            if result_user.inserted_id:

                return {
                        "status_code": 2000,
                        "detail": "User created. Account awaiting validation by admin"
                }

            else:
                return {
                    "status_code": 1000,
                    "detail": "An error occurred - User not created"
                }
        else:
            return {
                "status_code": 1001,
                "detail": "Invalid email address"
            }

    else:
        return {
                "status_code": 1002,
                "detail": "Username / email/ national_id  already exists"
        }


@users_router.post("/login")
async def login(request: Request, data: OAuth2PasswordRequestForm = Depends()):
    
    login_user = None
    username_or_email = data.username
    password = data.password
    if username_or_email and password:
        login_user = await users.find_one({
                                            "$or" : [
                                                        {'username' : username_or_email},
                                                        {'email' : username_or_email}
                                                    ]
                                            
                                            }
                                        )
        if login_user:
            if bcrypt.hashpw(password.encode('utf-8'), login_user['password']) == login_user['password']:
                user_is_admin = login_user.get("role") == UserRole.admin
                if user_is_admin or login_user.get("account_status", None) == UserAccountStatus.validated:
                    #TODO: Check with smart contract if user has already voted. If so, prevent them to log in

                    user_id = str(login_user.get("_id"))
                    token = await create_access_token (
                        data = {
                            "user_id": user_id
                        },
                        admin = user_is_admin
                    )

                    info_user = api_user(login_user)
                    info_user.update({"token": token, "token_type": "bearer"})
                    return {
                        "status_code": 2000,
                        "detail": info_user
                    }
                
                return {
                    "status_code": 1001,
                    "detail": "Authentication refused. Account awaiting validation by admin"
                }

        return {
            "status_code": 1002,
            "detail": "Authentication refused. Invalid username/email and password combination"
        }

    return {
            "status_code": 1000,
            "detail": "Authentication refused. Username/email and/or password missing"
    }


@users_router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user.get("_id"))
    try:
        await delete_key_from_cache(user_id)
        return {
            "status_code": 2000,
            "detail": "User Authorization deleted"
        }
    except:
        return {
            "status_code": 1000,
            "detail": "An error occurred while removing the authorization token from cache"
        }



@users_router.get("/admin-get-users")
async def get_registered_users_data( current_user: dict = Depends(get_current_user)):
    if await current_user_is_admin(current_user.get("user_id") ):

        list_users = await users.find({  "_id": { "$ne": ObjectId(current_user.get("user_id"))  }}).to_list(length=100)
        *list_users, = map(api_user, list_users)

        return {
            "status_code": 2000,
            "detail": list_users
        }
            
    else:
        return {
            "status_code": 1000,
            "detail": "Not authorized, you don't have required permission"
        }



@users_router.put("/admin-validate-users-accounts")
async def validate_users_accounts(data: dict, background_tasks: BackgroundTasks, current_user: dict = Depends(get_current_user)):
    if await current_user_is_admin(current_user.get("user_id")):
        if("user_to_validate_id" in data):
            user_to_validate_id = ObjectId(data["user_to_validate_id"])
            user = await users.find_one({"_id": user_to_validate_id})
            if  not user.get("account_status") == UserAccountStatus.validated:
                user_to_validate = await users.find_one_and_update(
                    {"_id" : user_to_validate_id }, 
                    {
                        "$set" : {
                            "account_status" : UserAccountStatus.validated, 
                            "updated_on": datetime.datetime.now()
                        }
                    },
                    new=True
                )

                if user_to_validate:
                    voter_id = generate_ID()
                    national_id = user_to_validate.get("national_id")
                    firstname =  user_to_validate.get("firstname")
                    lastname =  user_to_validate.get("lastname")
                    gender =  user_to_validate.get("gender")
                    email = user_to_validate.get("email")
                    print(f"{voter_id=}")
                    receipt = main.chainvote_contract_bridge.add_voter(voter_id, national_id, firstname, lastname, gender)
                    if(receipt.transactionHash):
                        background_tasks.add_task(send_post_account_activation_email, [email], voter_id)
                        return {
                            "status_code": 2000,
                            "detail": "Account has been activated"
                        }
                    return {
                            "status_code": 1001,
                            "detail": "An error occured while adding voter to the block chain"
                    }
                else:
                    return {
                                "status_code": 1000,
                                "detail": "An error occured during account activation"
                    }
            else:
                return {
                    "status_code": 1004,
                    "detail": "Error ! Account already activated"
                }
            
        return {
            "status_code": 1002,
            "detail": "Incorrect request. Missing 'user_to_validate_id' key in body"
        }
    else:
        return {
            "status_code": 1003,
            "detail": "Not authorized, you don't have required permission to activate the users accounts"
        }

