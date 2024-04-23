from pydantic import BaseModel, EmailStr
from typing import Optional
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str

# Temporary storage for registered users
registered_users = {}

def hash_password(password: str):
    return pwd_context.hash(password)