from pydantic import BaseModel, UUID4
from typing import Optional




class AssociationCreate(BaseModel):
    group_name: Optional[str]
    device_hostname: Optional[str]