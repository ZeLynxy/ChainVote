from fastapi import APIRouter, BackgroundTasks, Depends

from bson.objectid import ObjectId
import bcrypt
from fastapi import Request
from config.config import DB
from .utils import *
from utils import *
from utils.jwt_authorization import get_current_user
import main

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
                receipt = main.chainvote_contract_bridge.add_candidate(str(candidate_id), candidate_firstname, candidate_lastname, candidate_political_party )
                print(receipt)
                if(receipt.transactionHash):
                    return {
                        "status_code": 2000,
                        "detail": "Candidate added."
                    }
                else:
                    return {
                        "status_code": 1003,
                        "detail": "An error occurred - Candidate not added to the blockchain"
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


@ballots_router.get("/get-candidates")
async def get_candidates( current_user: dict = Depends(get_current_user)):
    result = main.chainvote_contract_bridge.get_candidates()

    return {
        "status_code": 2000,
        "detail": result
    }

@ballots_router.post("/vote")
async def get_candidates( data: dict, current_user: dict = Depends(get_current_user)):
    voter_id = data.get("voter_ID")
    candidate_id = data.get("candidate_id")
    result = main.chainvote_contract_bridge.vote(voter_id, candidate_id)
    print(result) 
    if(result.get("canVote")):
        if(result.get("hasVoted")):
            return {
                "status_code": 2000,
                "detail": "Your vote has been actually casted"
            }
        else:
            return {
                "status_code": 1000,
                "detail": "An error occured. Your vote has not been cast. Potential issue with your voter ID"
            }
    else:
        return {
                "status_code": 1001,
                "detail": "You have already voted!"
        }

