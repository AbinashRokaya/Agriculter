from pydantic import BaseModel,Field,condecimal,validator
from typing import Annotated,Optional,List
from uuid import UUID,uuid4
from schemas.user_schema import UserResponse
from schemas.product_schema import ProductPaganationResponse,ProductResponse


#####---------------------- Cart --------------------####
class CartIteamRequest(BaseModel):
   
    product_id:Annotated[UUID,Field(...,description="product if for cart item")]
    stock_quantaty:Annotated[int,Field(1,ge=1,description="Quantity of the product (default 1)")]

class CartReqest(BaseModel):
    product_items:List[CartIteamRequest]

class CartProductResponse(BaseModel):
    id:Optional[UUID]
    name:Optional[str]
    price:Optional[float]
    description:Optional[str]
    discount:Optional[int]
    category_name:Optional[str]
    image:Optional[str]=None
    coverimage:Optional[List[str]]=None



class CartResponse(BaseModel):
    cart_items_id:Optional[UUID]=None
    user_id:Optional[UUID]=None
    cart_id:Optional[UUID]=None
    product:Optional[CartProductResponse]=None
    stock_quantaty:Optional[int]=None

class CartPaganitionResponse(BaseModel):
    cart_list:Optional[List[CartResponse]]=None
    next_cursor:Optional[UUID]=None

# class CartUpdateRequest(BaseModel):
#     quantaty









#####---------------------- Cart Item --------------------####

class CartIteamResponse(BaseModel):
    cart_iteams_id:Optional[UUID]=None
    cart_id:Optional[UUID]=None
    product:Optional[ProductPaganationResponse]=None
    stock_quanty:Optional[int]=None
    