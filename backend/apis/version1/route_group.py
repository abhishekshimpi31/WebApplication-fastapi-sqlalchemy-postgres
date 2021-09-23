from db.repository.association import delete_association
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


router = APIRouter()


@router.post("/create")
def create_new_group(group: GroupCreate, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    owner_id = current_user.user_id
    userrole = get_role(user_id=owner_id, db=db)
    if userrole.role_id == 1 or userrole.role_id == 2:
        group = create_group(group=group, db=db, owner_id=owner_id)
        return group
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You have not privilages to create device")


@router.get("/{group_name}", response_model=ShowGroup)
def retrived_group_by_name(group_name: str, db: Session = Depends(get_db)):
    group = retrived_group(group_name=group_name, db=db)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Group with {group_name} not found")
    return group



@router.get("/list-of-groups", response_model=List[ShowGroup])
def list_of_all_groups(db: Session = Depends(get_db)):
    groups = list_groups(db=db)
    return groups


@router.put("/{group_name}/update")
def update_group_by_name(group_name: str, group: GroupUpdate, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    owner_id = current_user.user_id
    groups = retrived_group(group_name=group_name, db=db)
    if groups is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Device with id {group_name} not found")
    if groups.group_owner_id == current_user.user_id:
        message = update_group(group_name=group_name, db=db, group=group, owner_id=owner_id)
        if not message:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Device with id {group_name} not found")
        return "Successfully Updated"
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You have not privilages to update this device")    



@router.delete("/{group_name}/delete")
def delete_device_by_name(group_name: str, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    owner_id = current_user.user_id
    groups = retrived_group(group_name=group_name, db=db)
    if not groups:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Group with name {group_name} not found")
    if groups.group_owner_id == current_user.user_id:
        delete_association(name=group_name,db=db,owner_id=owner_id)
        delete_group(name=group_name,owner_id=owner_id,db=db)
        return "Successfully Deleted"
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="You are not permitted")


@router.get("/select-device-present-in-group/{group_name}")
def retrived_device_from_group(group_name: str,db: Session = Depends(get_db)):
    device = devices_present_in_group(group_name=group_name, db=db)
    if device is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Device not found")
    return device



