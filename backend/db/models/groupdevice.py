from sqlalchemy.orm import relationship
from sqlalchemy import String, Boolean, Date, ForeignKey, Integer, Column, Table, Constraint


from db.base_class import Base


association = Table('association', Base.metadata,
    Column('group_id',Integer, ForeignKey('devicegroups.group_id'), primary_key=True),
    Column('device_id',Integer, ForeignKey('device.device_id'), primary_key=True),
    Column('owner_id',Integer, ForeignKey('users.user_id')))


class DeviceGroups(Base):
    group_id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String, nullable=False, unique=True)
    group_description = Column(String, nullable=False)
    created_on = Column(Date)
    created_by = Column(String, nullable=False)
    updated_on = Column(Date)
    updated_by = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    group_owner_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship('Users', back_populates='group')
    subscription = relationship("Device",secondary=association,back_populates="subcribers")

