from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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



@app.on_event("startup")
async def app_startup():
    """
    Do tasks related to app initialization.
    """
    print("App has started")


@app.on_event("shutdown")
async def app_shutdown():
    """
    Do tasks related to app termination.
    """
    print("App termination ...")
    
