from pydantic import BaseModel, UUID4
from typing import Optional

from db.models.role import Role

class RoleBase(BaseModel):
    name: Optional[str]
    rights: Optional[str]
