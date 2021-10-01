from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from db.base_class import Base


class Role(Base):
    role_id = Column(Integer,primary_key=True,index=True)
    name = Column(String, nullable=False, unique=True)
    rights = Column(String, nullable=False, unique=True)

    userrole = relationship("UserRole", back_populates="role", uselist=False)
