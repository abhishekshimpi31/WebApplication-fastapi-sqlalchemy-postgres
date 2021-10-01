from pydantic.networks import EmailStr
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.functions import user
from db.models.userrole import UserRole
from db.models.role import Role
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import sys

from sqlalchemy.sql import roles

from db.models.user import Users
from db.schemas.user import UserCreate
from core.hashing import Hasher


def create_user(user: UserCreate, db: Session):
    user = Users(full_name=user.full_name,
                 email=user.email,
                 contact_number=user.contact_number,
                 hashed_password=Hasher.get_passwd_hash(user.password),
                 location=user.location,
                 created_by=user.created_by,
                 created_on=user.created_on,
                 updated_by=user.updated_by,
                 updated_on=user.updated_on,
                 is_active=True,
                 is_superuser=False)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user



def list_users(db: Session):
    user = db.query(Users).filter(Users.is_active == True).all()
    return user


def retrived_user(user_id:int, db: Session):
    user =  db.query(Users).filter(user_id == Users.user_id).first()
    return user


def delete_user(user_id:int, owner_id: int, db: Session):
    existing_user = db.query(Users).filter(Users.user_id == user_id)
    if not existing_user.first():
        return 0
    existing_user.delete(synchronize_session=False)
    db.commit()
    return 1
