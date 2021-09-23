#from db.repository.userrole import retrived_userrole
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


