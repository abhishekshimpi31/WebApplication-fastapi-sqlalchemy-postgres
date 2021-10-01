from pydantic import BaseModel, UUID4
from typing import Optional

from pydantic.networks import EmailStr


class UserRoleCreate(BaseModel):
    user_id: Optional[int]
    role_id: Optional[int]

