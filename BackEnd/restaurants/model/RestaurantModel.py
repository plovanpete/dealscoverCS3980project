from pydantic import BaseModel
from uuid import UUID, uuid4

class Restaurant(BaseModel):
    _id: UUID = uuid4()  # Assign a UUID when creating a new instance
    name: str
    address: str
    zipcode: str


class RestaurantRequest(BaseModel):
    name: str 
    address: str 
    zipcode: str 

