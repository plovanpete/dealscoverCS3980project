from pydantic import BaseModel, Field, validator
from bson import ObjectId

class Coupon(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    title: str
    description: str
    restaurant_id: str

    @validator('id', 'restaurant_id', pre=True, always=True)
    def validate_ids(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return str(ObjectId(v))

class CouponRequest(BaseModel):
    title: str
    description: str
    restaurant_id: str

    @validator('restaurant_id', pre=True, always=True)
    def validate_restaurant_id(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return str(ObjectId(v))



