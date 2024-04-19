from pydantic import BaseModel

class Coupon(BaseModel):
    id: int
    title: str
    description: str

class CouponRequest(BaseModel):
    title: str
    description: str