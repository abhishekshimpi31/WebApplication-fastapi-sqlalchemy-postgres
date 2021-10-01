from db.base_class import Base
from typing import Optional
from pydantic import BaseModel, IPvAnyAddress
from datetime import date, datetime


class DeviceBase(BaseModel):
    device_ip: str = None
    device_hostname: str = None
    device_location: str = None
    created_by: str = None
    created_on: Optional[date]
    updated_by: str = None
    updated_on: Optional[date]


class DeviceCreate(BaseModel):
    device_ip: str
    device_hostname: str
    device_location: str
    created_by: str
    updated_by: str
    created_on: date = datetime.now().date()
    updated_on: date = datetime.now().date()


class DeviceUpdate(BaseModel):
    device_ip: str
    device_hostname: str
    device_location: str
    updated_by: str
    updated_on: date = datetime.now().date()


class ShowDevice(BaseModel):
    device_ip: str
    device_hostname: str
    device_location: str
    updated_by: str
    created_on: date
    updated_on: date

    class Config():
        orm_mode = True
