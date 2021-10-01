from starlette import status
from db.models.device import Device
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
import sys
from fastapi import HTTPException


from db.schemas.groupdevice import GroupCreate, GroupUpdate
from db.models.groupdevice import DeviceGroups, association


def create_group(group: GroupCreate, db: Session, owner_id: int):
    gpdevice = DeviceGroups(group_name=group.group_name,
                    group_description=group.group_description,
                    created_by=group.created_by,
                    updated_by=group.updated_by,
                    created_on=group.created_on,
                    updated_on=group.updated_on,
                    group_owner_id=owner_id,
                    )

    db.add(gpdevice)
    db.commit()
    db.refresh(gpdevice)
    return gpdevice


def retrived_group(group_id:int, db: Session):
    group =  db.query(DeviceGroups).filter(group_id == DeviceGroups.group_id).first()
    return group


def list_groups(db: Session):
    group = db.query(DeviceGroups).filter(DeviceGroups.is_active == True).all()
    return group


def update_group(group_id: int, db: Session, group: GroupUpdate, owner_id: int):
    existing_group = db.query(DeviceGroups).filter(DeviceGroups.group_id == group_id)
    if not existing_group.first():
        return 0
    existing_group.update(group.__dict__)
    db.commit()
    return 1


def delete_group(group_id: int, owner_id: int, db: Session):
    existing_group = db.query(DeviceGroups).filter(DeviceGroups.group_id == group_id)
    if not existing_group.first():
        return 0
    existing_group.delete(synchronize_session=False)
    db.commit()
    return 1


def devices_present_in_group(group_id: int, db:Session):
    group = db.query(DeviceGroups).filter(DeviceGroups.group_id == group_id).first()
    if group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Group not found")
    sys.setrecursionlimit(2000)
    device_list = association.join(Device, association.c.device_id == Device.device_id)
    device_in_group = select([Device.device_hostname]).filter(association.c.group_id==group.group_id).select_from(device_list)
    result = db.execute(device_in_group)
    return result.fetchall()
