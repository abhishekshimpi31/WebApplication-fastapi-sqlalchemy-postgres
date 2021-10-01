from sqlalchemy.orm import relationship
from sqlalchemy import String, Boolean, Date, Integer, Column


from db.base_class import Base


class Users(Base):
    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    contact_number = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    location = Column(String, nullable=False)
    created_on = Column(Date)
    created_by = Column(String, nullable=False)
    updated_on = Column(Date)
    updated_by = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    device = relationship('Device', back_populates='user')
    group = relationship('DeviceGroups', back_populates='user')
    user_role = relationship("UserRole", back_populates="user", uselist=False)
