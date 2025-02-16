from pydantic import BaseModel, Field
from bson.objectid import ObjectId


# Pydantic Models
class UserCreate(BaseModel):
    name: str = Field(..., description="User's full name")
    email: str = Field(..., description="User's email address")
    phone_number: str = Field(..., description="User's phone number")

class User(UserCreate):
    id: str = Field(..., alias="_id", description="User's unique ID")

    class Config:
        population_by_field_name = True
        json_encoders = {ObjectId: str} # to serialize ObjectId to string
