from db.repository.association import delete_association_by_device
from db.repository.userrole import get_role
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List


from db.schemas.device import DeviceCreate, ShowDevice, DeviceUpdate
from db.repository.device import create_device, delete_device, groups_to_which_device_allocate, retrived_device, update_device
from db.session import get_db
from db.models.user import Users
from apis.version1.route_login import get_current_user_from_token
from core.config import settings

router = APIRouter()


@router.post("/device", response_model=ShowDevice)
def create_new_device(device: DeviceCreate, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    owner_id = current_user.user_id
    userrole = get_role(user_id=owner_id, db=db)
    if userrole is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User is not assign to any role")
    if userrole.role_id == settings.ADMIN or userrole.role_id == settings.MANAGER:
        try:
            device = create_device(device=device, db=db, owner_id=owner_id)
            return device
        except:
            raise HTTPException(status_code=status.HTTP_201_CREATED,detail="Device is already created")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You have not privilages to create device")



@router.get("/{device_id}", response_model=ShowDevice)
def retrived_device_by_device_id(device_id: int, db: Session = Depends(get_db)):
    device = retrived_device(device_id=device_id, db=db)
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Device with device id {device_id} not found")
    return device


@router.put("/{device_id}")
def update_devices_by_device_id(device_id: int, device: DeviceUpdate, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    owner_id = current_user.user_id
    devices = retrived_device(device_id=device_id, db=db)
    if devices is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Device with id {device_id} not found")
    if devices.device_owner_id == current_user.user_id:
        message = update_device(device_id=device_id, db=db, device=device, owner_id=owner_id)
        if not message:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Device with id {device_id} not found")
        return "Succesfully Updated"
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You have not privilages to update this device")



@router.delete("/{device_id}")
def delete_device_by_device_id(device_id: int, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    owner_id = current_user.user_id
    devices = retrived_device(device_id=device_id, db=db)
    if not devices:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Device with id {device_id} not found")
    if devices.device_owner_id == current_user.user_id:
        delete_association_by_device(device_id=device_id,db=db,owner_id=owner_id)
        delete_device(device_id=device_id,owner_id=owner_id,db=db)
        return "Successfully Deleted"
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="You are not permitted")



@router.get("/{device_id}/groups")
def retrived_device_from_group(device_id: int,db: Session = Depends(get_db)):
    group = groups_to_which_device_allocate(device_id=device_id,db=db)
    if group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Group not found")
    return group






