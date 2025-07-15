from database.database import Base
from sqlalchemy import String,Boolean,Column,Integer,DateTime,Enum
from sqlalchemy.sql import func
from uuid import uuid4
from sqlalchemy.types import UUID
from schemas.role_schema import Role
from sqlalchemy.orm import relationship



class UserModel(Base):
    __tablename__="user"

    user_id=Column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    name=Column(String,nullable=False)
    email=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=True)
    role=Column(Enum(Role),default=Role.User)
    is_google_auth=Column(Boolean,default=False)
    created_at=Column(DateTime,server_default=func.now())
    update_at=Column(DateTime,server_default=func.now(),onupdate=func.now())

    cart_value=relationship("CartModel",back_populates="user")
    order=relationship("OrderModel",back_populates="user")
    
