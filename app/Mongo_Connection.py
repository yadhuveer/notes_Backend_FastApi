
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()


MONGO_URL = os.getenv("DATABASE_URL")

client = None
db = None

async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(MONGO_URL)
    db = client.get_default_database()
    print("Sucessfully Connected to MongoDB")

async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("Mongo connection closed sucessfully")

def get_database():
    return db
