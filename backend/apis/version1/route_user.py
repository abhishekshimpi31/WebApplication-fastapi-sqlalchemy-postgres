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


router = APIRouter()


@router.post("/create", response_model=ShowUser)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_user(user, db)
    return user


@router.get("/list-of-users", response_model=List[ShowUser])
def list_of_all_devices(db: Session = Depends(get_db)):
    users = list_users(db=db)
    return users


@router.get("/{email}", response_model=ShowUser)
def retrived_user_by_fullname(email:EmailStr, db: Session = Depends(get_db)):
    user = retrived_user(email=email, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Group with {email} not found")
    return user


@router.delete("/{email}/delete")
def delete_user_by_user_name(email:EmailStr, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_from_token)):
    owner_id = current_user.user_id
    user = retrived_user(email=email,db=db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Group with {email} not found")
    if user.user_id == owner_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Login user cannot be deleted")
    userrole = get_role(user_id=owner_id, db=db)
    if userrole.role_id == 1:
        try:
            delete_user_role(user_name=user.full_name,owner_id=owner_id,db=db)
            delete_user(email=email,owner_id=owner_id,db=db)
            return "Successfully Deleted"
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"First delete all devices and groups associated with {email}")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not permitted to delete the user")





                        