from typing import Optional
from pydantic import EmailStr, BaseModel, ValidationError, validator
from datetime import datetime, date


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    contact_number: str
    password: str
    location: str
    created_by: str
    created_on: date = datetime.now().date()
    updated_by: str
    updated_on: date = datetime.now().date()


class UserCreate_test(BaseModel):
    email: EmailStr
    password: str





class ShowUser(BaseModel):
    full_name: str
    email: EmailStr
    contact_number: str
    location: str
    created_by: str
    created_on: date
    updated_by: str
    updated_on: date
    is_active: bool

    class Config():
        orm_mode = True
