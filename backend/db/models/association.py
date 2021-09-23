# from sqlalchemy.orm import relationship
# from sqlalchemy import String, Integer, Column
# from sqlalchemy.sql.elements import BooleanClauseList
# from sqlalchemy.sql.expression import null
# from sqlalchemy.sql.schema import ForeignKey



# from db.base_class import Base
# from db.models.groupdevice import GroupDevice
# from db.models.device import Device 


# class Association(Base):
#     gpdevice_id = Column(Integer,ForeignKey(GroupDevice.gpdevice_id), primary_key=True, nullable=False)
#     device_id = Column(Integer,ForeignKey(Device.device_id), primary_key=True, nullable=False)
#     owner_id = Column(Integer, ForeignKey('users.user_id'))


#     user = relationship('Users', back_populates='association')

    