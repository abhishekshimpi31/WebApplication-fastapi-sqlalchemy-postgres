from pydantic import BaseModel, UUID4
from typing import List, Optional




class AssociationCreate(BaseModel):
    group_id: int
    device_id: int
