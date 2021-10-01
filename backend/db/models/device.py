from sqlalchemy.orm import relationship
from sqlalchemy import String, Boolean, Date, ForeignKey, Integer, Column


from db.base_class import Base
from db.models.groupdevice import association


class Device(Base):
    device_id = Column(Integer, primary_key=True, index=True)
    device_ip = Column(String, nullable=False, unique=True)
    device_hostname = Column(String, nullable=False, unique=True)
    device_location = Column(String, nullable=False)
    created_on = Column(Date)
    created_by = Column(String, nullable=False)
    updated_on = Column(Date)
    updated_by = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    device_owner_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship('Users', back_populates='device')
    #groupasso = relationship("GroupDevice",secondary='AssociationTable',back_populates="deviceasso")
    subcribers = relationship("DeviceGroups",secondary=association,back_populates="subscription")

