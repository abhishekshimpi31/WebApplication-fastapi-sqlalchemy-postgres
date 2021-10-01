from db.repository.role import create_role
from typing import Any
from pydantic.types import UUID4
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException


from db.schemas.userrole import UserRoleCreate
from db.session import get_db
from db.repository.userrole import create_userrole


router = APIRouter()


@router.post("/userrole")
def assign_user_role(user_id:int, role_id:int, db:Session = Depends(get_db), ):

    user_role = create_userrole(user_id=user_id, role_id=role_id, db=db)
    return user_role
