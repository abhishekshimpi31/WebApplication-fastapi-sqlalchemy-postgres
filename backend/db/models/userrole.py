from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, Column
from sqlalchemy.sql.elements import BooleanClauseList
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import ForeignKey



from db.base_class import Base
from db.models.user import Users
from db.models.role import Role 


class UserRole(Base):
    user_id = Column(Integer,ForeignKey(Users.user_id), primary_key=True, nullable=False)
    role_id = Column(Integer,ForeignKey(Role.role_id), primary_key=True, nullable=False)

    role = relationship("Role")
    user = relationship("Users", back_populates="user_role", uselist=False)