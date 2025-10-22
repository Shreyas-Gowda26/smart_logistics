from pydantic import BaseModel,EmailStr,Field
from typing import Optional

class UserBase(BaseModel):
    name : str
    email :EmailStr
    phone : Optional[str] = None
    role : str = "customer"

class UserCreate(UserBase):
    password : str = Field(...,min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password :str

class UserResponse(UserBase):
    id :str

    class Config:
        orm_mode = True