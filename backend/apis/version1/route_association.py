from typing import List, Optional

from fastapi.param_functions import Query
from core.config import settings
from db.repository.device import retrived_device
from db.models.groupdevice import DeviceGroups
from db.schemas.association import AssociationCreate
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from db.schemas.association import AssociationCreate
from db.models.user import Users
from db.session import get_db
from db.repository.association import create_association, delete_association, delete_association_by_group
from apis.version1.route_login import get_current_user_from_token
from db.repository.groupdevice import retrived_group
from db.repository.userrole import get_role


router = APIRouter()


@router.post("/association")
def create_new_association(group_id:int, device_id: Optional[List[int]]=Query(None),
                            current_user: Users = Depends(get_current_user_from_token),
                            db: Session = Depends(get_db)):
    owner_id = current_user.user_id
    userrole = get_role(user_id=owner_id, db=db)
    group_owner = retrived_group(group_id=group_id,db=db)
    for n in device_id:
        device_owner = retrived_device(device_id=n,db=db)
        if not device_owner:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{n} dose not exist")
    if not group_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{group_id} dose not exist")
    if userrole.role_id == settings.ADMIN or userrole.role_id == settings.MANAGER:
        if owner_id == group_owner.group_owner_id:
            try:
                for n in device_id:
                    creation = create_association(group_id=group_id,device_id=n,db=db,owner_id=owner_id)

                return creation
            except:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{device_id} is aleardy exist in {group_id}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not authorise to modify this group")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You have not privilages to make changes")



@router.delete("/{group_id}/{device_id}")
def delete_associations(group_id:int, device_id:int,
                            current_user: Users = Depends(get_current_user_from_token),
                            db: Session = Depends(get_db)):
    owner_id = current_user.user_id
    userrole = get_role(user_id=owner_id, db=db)
    group_owner = retrived_group(group_id=group_id,db=db)
    device_owner = retrived_device(device_id=device_id,db=db)
    if not group_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{group_id} dose not exist in groups")
    if not device_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{device_id} dose not exist in devices")
    if userrole.role_id == settings.ADMIN or userrole.role_id == settings.MANAGER:
        if owner_id == group_owner.group_owner_id:
            try:
                delete_association(group_id=group_id, device_id=device_id,  db=db, owner_id=owner_id)
                return "Successfully Deleted"
            except:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{device_id} is not exist in {group_id}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not authorise to modify this association")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You have not privilages to make changes")


