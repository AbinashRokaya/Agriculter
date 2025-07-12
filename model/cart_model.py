from sqlalchemy import (String,Boolean,Column,Integer,DateTime,Enum,Float,ForeignKey,Numeric)
from database.database import Base
from sqlalchemy.sql import func
from uuid import uuid4
from sqlalchemy.types import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship



class CarItemModel(Base):
    __tablename__="cart_items"

    order_items_id=Column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    cart_id=Column(UUID(as_uuid=True),ForeignKey("cart.cart_id"))
    product_id=Column(UUID(as_uuid=True),ForeignKey("product.product_id"))
    stock_quantaty=Column(Integer,default=1)

    cart=relationship("CartModel",back_populates="cart_item")
    product=relationship("ProductModel",back_populates="cart")


class CartModel(Base):
    __tablename__="cart"
    cart_id=Column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    user_id=Column(UUID(as_uuid=True),ForeignKey("user.user_id"))
    created_at=Column(DateTime,server_default=func.now())
    update_at=Column(DateTime,server_default=func.now(),onupdate=func.now())

    user=relationship("UserModel",back_populates="cart_value")
    cart_item=relationship("CarItemModel",back_populates="cart")

