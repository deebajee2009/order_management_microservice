from fastapi import APIRouter, HTTPException
from typing import List
import asyncio

from schemas import *
from config import config
from database import get_db

router = APIRouter(
    prefix='/orders',
    tags = ['orders']
)

collection = config.MONGO_COLLECTION_ORDERS
db = get_db()

# FastAPI Endpoints
@router.post("/", response_model=Order, status_code=201)
async def create_order(order_in: OrderCreate):

    user_id = await get_user_id_from_users_service(order_in.phone_number)
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid phone_number: User's ID not found")

    order_dict = order_in.dict()
    order_dict["user_id"] = user_id

    del order_dict["phone_number"] # remove username field before saving

    result = await db[collecion].insert_one(order_dict)
    created_order = await  db[collecion].find_one({"_id": result.inserted_id})
    return Order(**created_order)


@router.get("/{phone_number}", response_model=List[Order])
async def get_orders_by_user(phone_number: str):
    user_id = await get_user_id_from_users_service(order_in.phone_number)
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid phone_number: User's ID not found")
    orders = await db[collection].find({"user_id": user_id})
    return [Order(**order) for order in list(orders)]
