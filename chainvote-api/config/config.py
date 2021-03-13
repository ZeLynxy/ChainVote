from motor.motor_asyncio import AsyncIOMotorClient
from fastapi_mail import ConnectionConfig
from .constants import CONFIG_FILE
import yaml
from aioredis import create_redis_pool



def load_config() -> dict:
    with open(CONFIG_FILE) as yaml_file:
        conf = yaml.load(yaml_file.read(), Loader=yaml.SafeLoader)
    return conf


CONF = load_config()


############### MONGO DATABASE ####################

DB_CLIENT = AsyncIOMotorClient(
    host=CONF.get("databases")["default"]["HOST"],
    port=int(CONF.get("databases")["default"]["PORT"]),
    username=CONF.get("databases")["default"]["USER"],
    password=CONF.get("databases")["default"]["PASSWORD"],
)

DB = DB_CLIENT[CONF.get("databases")["default"]["NAME"]]

def close_db_client():
    DB_CLIENT.close()




############### CACHE DATABASE ####################
class RedisCache:
    def __init__(self):
        self.cache = None

    async def init_cache(self):
        host = CONF.get("databases")["cache"]["HOST"]
        port = int(CONF.get("databases")["cache"]["PORT"])
        self.cache =  await create_redis_pool(f"redis://{host}:{port}/0?encoding=utf-8")
        
    async def close_cache(self):
        self.cache.close()
        await self.cache.wait_closed()

CACHE_DB = RedisCache()           


############# Email conf ##################
EMAIL_CONF = ConnectionConfig(
        MAIL_USERNAME = CONF.get("mail")["MAIL_USERNAME"],
        MAIL_PASSWORD = CONF.get("mail")["MAIL_PASSWORD"],
        MAIL_FROM = CONF.get("mail")["MAIL_FROM"],
        MAIL_FROM_NAME = CONF.get("mail")["MAIL_FROM_NAME"],
        MAIL_PORT = CONF.get("mail")["MAIL_PORT"],
        MAIL_SERVER = CONF.get("mail")["MAIL_SERVER"],
        MAIL_TLS = CONF.get("mail")["MAIL_TLS"] ,
        MAIL_SSL = CONF.get("mail")["MAIL_SSL"]
)


##########JWT TOKENS#################
JWT = {
    "SECRET_KEY" : CONF.get("jwt")["SECRET_KEY"],
    "ALGORITHM" : CONF.get("jwt")["ALGORITHM"],
    "ACCESS_TOKEN_EXPIRE_SECONDES" : CONF.get("jwt")["ACCESS_TOKEN_EXPIRE_SECONDES"],
    "ACCESS_TOKEN_EXPIRE_SECONDES_ADMIN" : CONF.get("jwt")["ACCESS_TOKEN_EXPIRE_SECONDES_ADMIN"]
}