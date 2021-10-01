from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime


class GroupBase(BaseModel):
    group_name: str = None
    group_description: str = None
    created_by: str = None
    created_on: Optional[date]
    updated_by: str = None
    updated_on: Optional[date]


class GroupCreate(BaseModel):
    group_name: str
    group_description: str
    created_by: str
    updated_by: str
    created_on: date = datetime.now().date()
    updated_on: date = datetime.now().date()


class GroupUpdate(BaseModel):
    group_name: str
    group_description: str
    updated_by: str
    updated_on: date = datetime.now().date()


class ShowGroup(BaseModel):
    group_name: str
    group_description: str
    created_by: str
    updated_by: str
    created_on: date
    updated_on: date

    class Config():
        orm_mode = True
