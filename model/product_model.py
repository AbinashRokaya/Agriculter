from sqlalchemy import (String,Boolean,Column,
                        Integer,DateTime,
                        Enum,Float,ForeignKey,
                        Numeric,JSON)
from database.database import Base
from sqlalchemy.sql import func
from uuid import uuid4
from sqlalchemy.types import UUID
from sqlalchemy.orm import relationship

class ProductModel(Base):
    __tablename__="product"

    product_id=Column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    name=Column(String,nullable=False)
    price=Column(Numeric(10,2),nullable=False)
    stock_quantity=Column(Integer,nullable=False)
    description=Column(String)
    discount=Column(Integer)
    image=Column(String)
    coverimage=Column(JSON)
    category_id=Column(UUID(as_uuid=True),ForeignKey("category.category_id"))
    created_at=Column(DateTime,server_default=func.now())
    update_at=Column(DateTime,server_default=func.now(),onupdate=func.now())

    cart=relationship("CarItemModel",back_populates="product")
    category=relationship("CategoryModel",back_populates="product")
    order_item=relationship("OrderItemsModel",back_populates="product")
