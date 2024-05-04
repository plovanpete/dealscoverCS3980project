from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4

class Recipe(BaseModel):
    _id: UUID = uuid4()
    title: str
    description: str
    image_url: Optional[str]  # Making the image_url field optional

class RecipeRequest(BaseModel):
    title: str
    description: str
    image_url: Optional[str]  # Making the image_url field optional


