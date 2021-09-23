from operator import and_
from db.session import get_db
from fastapi.param_functions import Depends
from pydantic.types import UUID4
from sqlalchemy.orm import Session
import sys




from db.schemas.association import AssociationCreate
from db.models.device import Device
from db.models.groupdevice import DeviceGroups, association



def create_association(associate:AssociationCreate, db:Session, owner_id:int):
    group = db.query(DeviceGroups).filter(DeviceGroups.group_name == associate.group_name).first()
    device = db.query(Device).filter(Device.device_hostname == associate.device_hostname).first()


    
    statement = association.insert().values(group_id=group.group_id, device_id=device.device_id, owner_id=owner_id)
    sys.setrecursionlimit(2000)
    db.execute(statement)
    db.commit()
    return statement


def delete_association_by_group(group_name:str, db:Session, owner_id:int):
    group = db.query(DeviceGroups).filter(DeviceGroups.group_name == group_name).first()


    statement = association.delete().where(association.c.group_id == group.group_id)
    sys.setrecursionlimit(2000)
    db.execute(statement)
    db.commit()
    return statement


def delete_association_by_device(device_hostname:str, db:Session, owner_id:int):
    device = db.query(Device).filter(Device.device_hostname == device_hostname).first()


    statement = association.delete().where(association.c.device_id == device.device_id)
    sys.setrecursionlimit(2000)
    db.execute(statement)
    db.commit()
    return statement


def delete_association(associate:AssociationCreate, db:Session, owner_id:int):
    group = db.query(DeviceGroups).filter(DeviceGroups.group_name == associate.group_name).first()
    device = db.query(Device).filter(Device.device_hostname == associate.device_hostname).first()


    statement = association.delete().where(association.c.group_id == group.group_id, association.c.device_id == device.device_id)
    sys.setrecursionlimit(2000)
    db.execute(statement)
    db.commit()
    return statement




