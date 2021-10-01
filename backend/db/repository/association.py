"""This file contain buisness logic for the association model"""
from operator import and_
from typing import List, Optional
from db.session import get_db
from fastapi.param_functions import Depends, Query
from pydantic.types import UUID4
from sqlalchemy.orm import Session
import sys




from db.schemas.association import AssociationCreate
from db.models.device import Device
from db.models.groupdevice import DeviceGroups, association



def create_association(group_id:int, owner_id:int, db:Session, device_id:Optional[List[int]]=Query(None)):
    group = db.query(DeviceGroups).filter(DeviceGroups.group_id == group_id).first()
    device = db.query(Device).filter(Device.device_id == device_id).first()
    statement = association.insert().values(group_id=group.group_id, device_id=device.device_id, owner_id=owner_id)
    sys.setrecursionlimit(2000)
    db.execute(statement)
    db.commit()
    return "Successfully Created"




def delete_association_by_group(group_id:int, db:Session, owner_id:int):
    group = db.query(DeviceGroups).filter(DeviceGroups.group_id == group_id).first()


    statement = association.delete().where(association.c.group_id == group.group_id)
    sys.setrecursionlimit(2000)
    db.execute(statement)
    db.commit()
    return statement


def delete_association_by_device(device_id:int, db:Session, owner_id:int):
    device = db.query(Device).filter(Device.device_id == device_id).first()


    statement = association.delete().where(association.c.device_id == device.device_id)
    sys.setrecursionlimit(2000)
    db.execute(statement)
    db.commit()
    return statement


def delete_association(group_id:int, device_id:int, owner_id:int, db:Session):
    group = db.query(DeviceGroups).filter(DeviceGroups.group_id == group_id).first()
    device = db.query(Device).filter(Device.device_id == device_id).first()


    statement = association.delete().where(association.c.group_id == group.group_id, association.c.device_id == device.device_id)
    sys.setrecursionlimit(2000)
    db.execute(statement)
    db.commit()
    return statement


