from sqlalchemy import String,Boolean,Column,Integer,DateTime,Enum,Float,ForeignKey,Numeric
from database.database import Base
from sqlalchemy.sql import func
from uuid import uuid4
from sqlalchemy.types import UUID
from sqlalchemy.orm import relationship

class CategoryModel(Base):
    __tablename__="category"

    category_id=Column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    name=Column(String,nullable=False)
    description=Column(String)
    created_at=Column(DateTime,server_default=func.now())
    update_at=Column(DateTime,server_default=func.now(),onupdate=func.now())

    product=relationship("ProductModel",back_populates="category")
    
