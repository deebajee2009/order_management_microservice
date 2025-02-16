from pydantic import BaseModel, Field
from bson.objectid import ObjectId


# Pydantic Models
class OrderCreate(BaseModel):
    phone_number: str = Field(..., description="Username of the user placing the order")
    product_name: str = Field(..., description="Name of the product")
    price: float = Field(..., description="Price of the product")
    quantity: int = Field(..., description="Quantity of the product")

class Order(BaseModel):
    id: str = Field(..., alias="_id", description="Order's unique ID")
    user_id: str = Field(..., description="ID of the user who placed the order")
    product_name: str = Field(..., description="Name of the product")
    price: float = Field(..., description="Price of the product")
    quantity: int = Field(..., description="Quantity of the product")

    class Config:
        population_by_field_name = True
        json_encoders = {ObjectId: str} # Serialize ObjectId
