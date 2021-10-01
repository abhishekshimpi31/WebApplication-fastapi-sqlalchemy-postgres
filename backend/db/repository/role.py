"""This file contain buisness logic for the role model"""


from sqlalchemy.orm import Session


from db.models.role import Role
from db.schemas.role import RoleBase


def create_role(role:RoleBase, db:Session):
    role = Role(name = role.name,
    rights = role.rights)

    db.add(role)
    db.commit()
    db.refresh(role)
    return role


