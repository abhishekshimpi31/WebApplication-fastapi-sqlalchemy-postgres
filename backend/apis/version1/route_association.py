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


@router.post("/create")
def create_new_association(association:AssociationCreate, 
                            current_user: Users = Depends(get_current_user_from_token),
                            db: Session = Depends(get_db)):
    owner_id = current_user.user_id
    userrole = get_role(user_id=owner_id, db=db)
    group_owner = retrived_group(group_name=association.group_name,db=db)
    device_owner = retrived_device(device_hostname=association.device_hostname,db=db)
    if not group_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{association.group_name} dose not exist")
    if not device_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{association.device_hostname} dose not exist")
    if userrole.role_id == 1 or userrole.role_id == 2: 
        if owner_id == group_owner.group_owner_id:
            try:
                create_association(associate=association,db=db,owner_id=owner_id)
                return "Successfully Created"
            except:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{association.device_hostname} is aleardy exist in {association.group_name}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not authorise to modify this group")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You have not privilages to make changes")



@router.delete("/delete")
def create_new_association(association:AssociationCreate, 
                            current_user: Users = Depends(get_current_user_from_token),
                            db: Session = Depends(get_db)):
    owner_id = current_user.user_id
    userrole = get_role(user_id=owner_id, db=db)
    group_owner = retrived_group(group_name=association.group_name,db=db)
    device_owner = retrived_device(device_hostname=association.device_hostname,db=db)
    if not group_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{association.group_name} dose not exist in groups")
    if not device_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{association.device_hostname} dose not exist in devices")
    if userrole.role_id == 1 or userrole.role_id == 2: 
        if owner_id == group_owner.group_owner_id:
            try:
                delete_association(associate=association, db=db, owner_id=owner_id)
                return "Successfully Deleted"
            except:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{association.device_hostname} is aleardy exist in {association.group_name}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not authorise to modify this group")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You have not privilages to make changes")