"""This file contain buisness logic for the device model"""

import sys
from pydantic.typing import resolve_annotations
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from fastapi import HTTPException, status


from db.schemas.device import DeviceCreate, DeviceUpdate
from db.models.device import Device
from db.models.groupdevice import association, DeviceGroups



def create_device(device: DeviceCreate, db: Session, owner_id: int):
    """This function take few parameters and create the new device in database"""
    device = Device(device_ip=device.device_ip,
                    device_hostname=device.device_hostname,
                    device_location=device.device_location,
                    created_by=device.created_by,
                    updated_by=device.updated_by,
                    created_on=device.created_on,
                    updated_on=device.updated_on,
                    device_owner_id=owner_id)

    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def retrived_device(device_id:int, db: Session):
    """This function take device hostname and gives the device information"""
    device =  db.query(Device).filter(Device.device_id == device_id).first()
    return device


# def list_devices(db: Session):
#     device = db.query(Device).filter(Device.is_active == True).all()
#     return device


def update_device(device_id: int, db: Session, device: DeviceUpdate, owner_id: int):
    """This function take device hostname and update the device with new parameter"""
    existing_device = db.query(Device).filter(Device.device_id == device_id)
    if not existing_device.first():
        return 0
    #job.__dict__.update(owner_id=owner_id)
    existing_device.update(device.__dict__)
    db.commit()
    return 1


def delete_device(device_id: int, owner_id: int, db: Session):
    """This function take device hostname and delete it from database"""
    existing_job = db.query(Device).filter(Device.device_id == device_id)
    if not existing_job.first():
        return 0
    existing_job.delete(synchronize_session=False)
    db.commit()
    return 1


def groups_to_which_device_allocate(device_id: int, db:Session):
    """This function take device hostname and gives groups name in which it is present"""
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if device is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Device not found")
    sys.setrecursionlimit(2000)
    group_list = association.join(DeviceGroups, association.c.group_id == DeviceGroups.group_id)
    group_to_which_device_assign = select([DeviceGroups.group_name]).filter(association.c.device_id==device.device_id).select_from(group_list)
    result = db.execute(group_to_which_device_assign)
    return result.fetchall()
