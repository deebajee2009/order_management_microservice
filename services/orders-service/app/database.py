from pymongo import AsyncMongoClient
from config import config

MONGO_HOST = config.MONGO_HOST
MONGO_PORT = config.MONGO_PORT
MONGO_USER = config.MONGO_USER
MONGO_PASS = config.MONGO_PASS
MONGO_DATABASE = config.MONGO_DATABASE

connection_uri = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}"

client: AsyncMongoClient = None
database = None

async def connect_to_mongo():
    global client, database
    client = await AsyncMongoClient(connection_uri).aconnect()

    database = client[MONGO_DATABASE]


async def close_mongo_connection():
    if client:
        await client.close()

def get_db():
    return database
