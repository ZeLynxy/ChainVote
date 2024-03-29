from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import config 
from users.routes import users_router
from ballots.routes import ballots_router
from web3 import Web3
from utils.contract import ChainVoteContractBridge


w3 = Web3(Web3.HTTPProvider("http://172.17.0.1:7545"))
w3.eth.defaultAccount = w3.eth.accounts[0]

chainvote_contract_bridge = ChainVoteContractBridge(w3)

app = FastAPI()

origins = [
    "http://0.0.0.0"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    users_router,
    prefix="/chainvote-api/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    ballots_router,
    prefix="/chainvote-api/ballots",
    tags=["ballots"],
    responses={404: {"description": "Not found"}},
)

@app.on_event("startup")
async def app_startup():
    """
    Do tasks related to app initialization.
    """
    #config.load_config()
    await config.CACHE_DB.init_cache()
    
    print("App has started......................................................................")


@app.on_event("shutdown")
async def app_shutdown():
    """
    Do tasks related to app termination.
    """
    print( "App termination ...")
    
