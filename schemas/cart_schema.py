from pydantic import BaseModel,Field,condecimal,validator
from typing import Annotated,Optional,List
from uuid import UUID,uuid4
from schemas.user_schema import UserResponse
from schemas.product_schema import ProductPaganationResponse


#####---------------------- Cart --------------------####
class CartIteamRequest(BaseModel):
   
    product_id:Annotated[UUID,Field(...,description="product if for cart item")]
    stock_quantaty:Annotated[int,Field(1,ge=1,description="Quantity of the product (default 1)")]

class CartReqest(BaseModel):
    product_items:List[CartIteamRequest]

class CartResponse(BaseModel):
    user_id:Optional[UUID]=None
    cart_id:Optional[UserResponse]=None










#####---------------------- Cart Item --------------------####

class CartIteamResponse(BaseModel):
    cart_iteams_id:Optional[UUID]=None
    cart_id:Optional[UUID]=None
    product:Optional[ProductPaganationResponse]=None
    stock_quanty:Optional[int]=None
    