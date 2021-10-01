from db.session import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session



from db.repository.role import create_role
from db.schemas.role import RoleBase


router = APIRouter()


@router.post("/role")
def create_new_role(role:RoleBase, db: Session=Depends(get_db)):
    role = create_role(role=role, db=db)
    return role
