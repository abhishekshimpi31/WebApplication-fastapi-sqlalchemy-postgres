from pydantic.networks import EmailStr
from db.repository.userrole import delete_user_role, get_role
from apis.version1.route_login import get_current_user_from_token
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from db.schemas.user import UserCreate, ShowUser
from db.repository.user import create_user, delete_user, list_users, retrived_user
from db.session import get_db
from db.models.user import Users
from core.config import settings


router = APIRouter()


@router.post("/user", response_model=ShowUser)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(user, db)
        return user
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user with {user.email} or {user.contact_number} already exist")




@router.get("/users", response_model=List[ShowUser])
def list_of_all_devices(db: Session = Depends(get_db)):
    users = list_users(db=db)
    return users


@router.get("/{user_id}", response_model=ShowUser)
def retrived_user_by_user_id(user_id:int, db: Session = Depends(get_db)):
    user = retrived_user(user_id=user_id, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {user_id} not found")
    return user


@router.delete("/{user_id}")
def delete_user_by_user_name(user_id:int, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    owner_id = current_user.user_id
    user = retrived_user(user_id=user_id,db=db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Group with {user_id} not found")
    if user.user_id == owner_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Login user cannot be deleted")
    userrole = get_role(user_id=owner_id, db=db)
    if userrole.role_id == settings.ADMIN:
        try:
            delete_user_role(user_id=user.user_id,owner_id=owner_id,db=db)
            delete_user(user_id=user_id,owner_id=owner_id,db=db)
            return "Successfully Deleted"
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"First delete all devices and groups associated with {user_id}")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not permitted to delete the user")

