from sqlalchemy import (String,Boolean,Column,
                        Integer,DateTime,Enum,
                        Float,ForeignKey,Numeric)
from database.database import Base
from sqlalchemy.sql import func
from uuid import uuid4
from sqlalchemy.types import UUID
from schemas.order_schema import OrderStatus
from sqlalchemy.orm import relationship


class OrderModel(Base):
    __tablename__="order"
    order_id=Column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    user_id=Column(UUID(as_uuid=True),ForeignKey("user.user_id"),nullable=False)
    # shipping_address_id=Column(UUID(as_uuid=True))
    total_amount=Column(Numeric(10,2),nullable=False)
    status=Column(Enum(OrderStatus),default=OrderStatus.Pending)
    created_at=Column(DateTime,server_default=func.now())
    update_at=Column(DateTime,server_default=func.now(),onupdate=func.now())


    order_item=relationship("OrderItemsModel",back_populates="order")
    user=relationship("UserModel",back_populates="order")


class OrderItemsModel(Base):
    __tablename__="order_items"
    order_items_id=Column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    order_id=Column(UUID(as_uuid=True),ForeignKey("order.order_id"),nullable=False)
    product_it=Column(UUID(as_uuid=True),ForeignKey("product.product_id"),nullable=False)
    stock_quantaty=Column(Integer,default=1,nullable=False)
    price=Column(Numeric(10,2),nullable=False)
    product=relationship("ProductModel",back_populates="order_item")
    order=relationship("OrderModel",back_populates="order_item")