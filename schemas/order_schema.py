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

class OrderProductResponse(BaseModel):
    id:Optional[UUID]
    name:Optional[str]
    
    description:Optional[str]
    discount:Optional[int]
    category_name:Optional[str]
    image:Optional[str]=None
    coverimage:Optional[List[str]]=None

class OrderResponse(BaseModel):
    order_id:Optional[UUID]=None
    total_amount:Optional[float]=None
    status:Optional[OrderStatus]=None



class UserResponse(BaseModel):
    user_id:Optional[UUID]=None
    name:Optional[str]=None


class OrderItemsResponse(BaseModel):
    order_item_id:Optional[UUID]=None
    product:Optional[OrderProductResponse]=None
    price:Optional[float]=None
    stock_quantaty:Optional[int]=None

    
class AllOrderItemsResponse(BaseModel):
    order_items:Optional[List[OrderItemsResponse]]=None
    user:Optional[UserResponse]=None
    order:Optional[OrderResponse]=None
   

class OrderPaganitionResponse(BaseModel):
    order_list:Optional[List[AllOrderItemsResponse]]=None
    next_cursor:Optional[UUID]=None


class OrderIteamRequest(BaseModel):
    
    product_id:Annotated[UUID,Field(...,description="product if for order item")]
    stock_quantaty:Annotated[int,Field(1,ge=1,description="Quantity of the product (default 1)")]

class OrderItemsListRequest(BaseModel):
    order_items:List[OrderIteamRequest]
# class OrderResponse(BaseModel):
#     order_items_id=Optional[UUID]=None
#     order_id:Optional[UUID]=None
#     user_id:Optional[UserResponse]=None
#     total_amount:Optional[float]=None
#     status:Optional[OrderStatus]=None
#     product_item:Optional[List[OrderIteamRequest]]=None










###---------------------------- order items -------------------#####


# class OrderIteamResponse(BaseModel):
#     order_item_id:Optional[UUID]=None
#     order_id:Optional[UUID]=None
#     product:Optional[ProductPaganationResponse]=None
#     stock_quanty:Optional[int]=None
#     price:Optional[float]=None
