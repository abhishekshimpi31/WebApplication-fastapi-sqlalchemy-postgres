from typing import List
from db.repository.userrole import get_role
import re
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from db.schemas.groupdevice import GroupCreate, GroupUpdate, ShowGroup
from db.repository.groupdevice import create_group, delete_group, devices_present_in_group, list_groups, retrived_group, update_group
from db.session import get_db
from db.models.user import Users
from apis.version1.route_login import get_current_user_from_token
from db.repository.association import delete_association, delete_association_by_group
from core.config import settings

router = APIRouter()


@router.post("/group", response_model=ShowGroup)
def create_new_group(group: GroupCreate, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    owner_id = current_user.user_id
    userrole = get_role(user_id=owner_id, db=db)
    if userrole.role_id == settings.ADMIN or userrole.role_id == settings.MANAGER:
        group = create_group(group=group, db=db, owner_id=owner_id)
        return group
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You have not privilages to create device")


@router.get("/{group_id}", response_model=ShowGroup)
def retrived_group_by_name(group_id: int, db: Session = Depends(get_db)):
    group = retrived_group(group_id=group_id, db=db)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Group with {group_id} not found")
    return group



@router.put("/{group_id}")
def update_group_by_name(group_id: int, group: GroupUpdate, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    owner_id = current_user.user_id
    groups = retrived_group(group_id=group_id, db=db)
    if groups is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Device with id {group_id} not found")
    if groups.group_owner_id == current_user.user_id:
        message = update_group(group_id=group_id, db=db, group=group, owner_id=owner_id)
        if not message:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Device with id {group_id} not found")
        return "Successfully Updated"
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You have not privilages to update this device")    



@router.delete("/{group_id}")
def delete_device_by_name(group_id: int, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    owner_id = current_user.user_id
    groups = retrived_group(group_id=group_id, db=db)
    if not groups:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Group with name {group_id} not found")
    if groups.group_owner_id == current_user.user_id:
        delete_association_by_group(group_id=group_id,db=db,owner_id=owner_id)
        delete_group(group_id=group_id,owner_id=owner_id,db=db)
        return "Successfully Deleted"
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="You are not permitted")


@router.get("/{group_id}/devices")
def retrived_device_from_group(group_id: int,db: Session = Depends(get_db)):
    device = devices_present_in_group(group_id=group_id, db=db)
    if device is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Device not found")
    return device





