from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router import router
from database import connect_to_mongo, close_mongo_connection


app = FastAPI()
app.include_router(router)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_client():

    await connect_to_mongo()
    print("Connected to MongoDB")


@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()
