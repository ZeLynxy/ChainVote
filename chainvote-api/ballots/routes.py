from fastapi import APIRouter, BackgroundTasks, Depends

from bson.objectid import ObjectId
import bcrypt
from fastapi import Request
from config.config import DB
import datetime
from .utils import *
from utils import *
from utils.jwt_authorization import  create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm


ballots_router = APIRouter()
ballots = DB.ballots


@ballots_router.post("/create")
async def create_ballot(data: dict, current_user: dict = Depends(get_current_user)):
    if await current_user_is_admin(current_user.get("user_id") ):

        title = data.get("title")
        result = await ballots.insert_one({
            "title": title,
            "candidates": []
        })
        if result.inserted_id:
            return {
                    "status_code": 2000,
                    "detail": "Ballot created."
            }

        else:
            return {
                "status_code": 1001,
                "detail": "An error occurred - Ballot not created"
            }
    else:
        return {
            "status_code": 1000,
            "detail": "Not authorized, you don't have required permission"
        }

@ballots_router.post("/add-candidate")
async def add_candidate(data: dict, current_user: dict = Depends(get_current_user)):
    if await current_user_is_admin(current_user.get("user_id") ):

        candidate_firstname = data.get("candidate_firstname")
        candidate_lastname = data.get("candidate_lastname")
        candidate_political_party = data.get("candidate_political_party")
        ballot_id = data.get("ballot_id")
        
        ballot = await ballots.find_one({"_id": ObjectId(ballot_id)})
        if ballot:
            candidate_id = ObjectId()
            candidate = {
                "_id": candidate_id,
                "candidate_firstname": candidate_firstname,
                "candidate_lastname": candidate_lastname,
                "candidate_political_party": candidate_political_party

            }

            result = await ballots.update_one(
                {
                    "_id": ObjectId(ballot_id),
                },
                
                {
                    "$push": {
                        "candidates": candidate
                    }
                }            
            )
            if result.modified_count > 0:
                return {
                        "status_code": 2000,
                        "detail": "Candidate added."
                }

            else:
                return {
                    "status_code": 1001,
                    "detail": "An error occurred - Candidate not added"
                }
        else:
            return {
                    "status_code": 1002,
                    "detail": "An error occurred - Ballot doesn't exist."
            }

    else:
        return {
            "status_code": 1000,
            "detail": "Not authorized, you don't have required permission"
        }


@ballots_router.get("/get-ballots")
async def get_ballots( current_user: dict = Depends(get_current_user)):
    list_ballots = await ballots.find({}).to_list(length=100)
    *list_ballots, = map(api_ballot, list_ballots)

    return {
        "status_code": 2000,
        "detail": list_ballots
    }
