from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserSchema(BaseModel):
    name: str
    surname: Optional[str] = None
    username: str
    email: EmailStr
    password: str
    phone_number: str
    birthday: Optional[str] = None
    city: Optional[str] = None
    reg_date: datetime


class UserRead(BaseModel):
    status: int
    message: bool
