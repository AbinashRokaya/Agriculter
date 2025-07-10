from sqlalchemy import String,Boolean,Column,Integer,DateTime,Enum,Float,ForeignKey,Numeric
from database.database import Base
from sqlalchemy.sql import func
from uuid import uuid4
from sqlalchemy.types import UUID


class CartModel(Base):
    __tablename__="cart"
    cart_id=Column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    user_id=Column(UUID(as_uuid=True),ForeignKey("user.user_id"))
    created_at=Column(DateTime,server_default=func.now())
    update_at=Column(DateTime,server_default=func.now(),onupdate=func.now())


class CarItemModel(Base):
    __tablename__="cart_items"

    order_items_id=Column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    cart_id=Column(UUID(as_uuid=True),ForeignKey("cart.cart_id"))
    product_id=Column(UUID(as_uuid=True),ForeignKey("product.product_id"))
    stock_quantaty=Column(Integer,default=1)
