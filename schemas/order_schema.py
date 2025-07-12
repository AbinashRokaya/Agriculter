from pydantic import BaseModel,Field,condecimal,validator
from typing import Annotated,Optional,List
from uuid import UUID,uuid4
from enum import Enum
from schemas.user_schema import UserResponse
from schemas.product_schema import ProductPaganationResponse

class OrderStatus(str,Enum):
    Pending="Pending"
    Processing="processing"
    Shipped="shipped"
    Delivered="delivered"
    Cancelled="cancelled"



###------------------- order ---------------------####
class OrderRequest(BaseModel):
    user_id:Annotated[UUID,Field(...,description="user id for creating cart id")]
    total_amount: Annotated[
        condecimal(max_digits=10, decimal_places=2),
        Field(...,ge=0, description="Price with 2 decimal places")
    ]
    status:Annotated[OrderStatus,Field(...,description="Order status")]
class OrderIteamRequest(BaseModel):
    
    product_id:Annotated[UUID,Field(...,description="product if for order item")]
    stock_quantaty:Annotated[int,Field(1,ge=1,description="Quantity of the product (default 1)")]
    price: Annotated[
        condecimal(max_digits=10, decimal_places=2),
        Field(...,ge=0, description="Price with 2 decimal places")
    ]
class OrderResponse(BaseModel):
    order_id:Optional[UUID]=None
    user_id:Optional[UserResponse]=None
    total_amount:Optional[float]=None
    status:Optional[OrderStatus]=None
    product_item=Optional[List[OrderIteamRequest]]=None










###---------------------------- order items -------------------#####


class OrderIteamResponse(BaseModel):
    order_item_id:Optional[UUID]=None
    order_id=Optional[UUID]=None
    product=Optional[ProductPaganationResponse]=None
    stock_quanty=Optional[int]=None
    price:Optional[float]=None
