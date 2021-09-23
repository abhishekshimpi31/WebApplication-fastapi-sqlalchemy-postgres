from pydantic import BaseModel, UUID4
from typing import Optional

from pydantic.networks import EmailStr


class UserRoleCreate(BaseModel):
    email: Optional[EmailStr]
    name: Optional[str]





