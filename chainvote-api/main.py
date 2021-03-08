from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import config 
from users.routes import users_router


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
    
