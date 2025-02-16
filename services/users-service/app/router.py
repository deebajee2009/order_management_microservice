from fastapi import APIRouter, HTTPException

from schemas import *
from config import config
from database import get_db


router = APIRouter(
    prefix='/users',
    tags = ['users']
)

collection = config.MONGO_COLLECTION_USERS
db = get_db()

# FastAPI Endpoints
@router.post("/", response_model=User, status_code=201)
async def create_user(user_in: UserCreate):
    user_dict = user_in.dict()
    result = await db[collecion].insert_one(user_dict)
    created_user = await db[collection].find_one({"_id": result.inserted_id})
    return User(**created_user)

@router.get("/{phone_number}", response_model=User)
async def get_user(user_id: str):
    user = await db[collection].find_one({"phone_number": phone_number})
    if user:
        return User(**user)
    else:
        raise HTTPException(status_code=404, detail="User not found")
