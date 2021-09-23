from starlette import status
from db.repository.groupdevice import retrived_group
from typing import Optional
from pydantic.networks import EmailStr
from pydantic.types import UUID4
from sqlalchemy.orm import Session
import sys
from fastapi import HTTPException



from db.models.userrole import UserRole
from db.schemas.userrole import UserRoleCreate
from db.models.role import Role
from db.models.user import Users



def create_userrole(user_role:UserRoleCreate, db:Session):
    user = db.query(Users).filter(Users.email == user_role.email).first()
    role = db.query(Role).filter(Role.name == user_role.name).first()

    
    userrole = UserRole(user_id = user.user_id,
                        role_id = role.role_id)

    
    db.add(userrole)
    db.commit()
    db.refresh(userrole)
    return userrole


def get_role(user_id:int, db:Session):
    user_role = db.query(UserRole).filter(user_id == UserRole.user_id).first()
    return user_role


def delete_user_role(user_name:str, db:Session, owner_id:int):
    user = db.query(Users).filter(Users.full_name==user_name).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Username not exist")

    existing_userrole = db.query(UserRole).filter(UserRole.user_id==user.user_id)
    if not existing_userrole.first():
        return 0

    existing_userrole.delete(synchronize_session=False)
    db.commit()
    return 1