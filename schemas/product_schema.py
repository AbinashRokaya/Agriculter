from pydantic import BaseModel,Field,condecimal,computed_field
from typing import Annotated,Optional,List
from uuid import UUID



class ProductCreate(BaseModel):
    name:Annotated[str,Field(...,max_length=255,description="Name of the product")]
    price: Annotated[
        condecimal(max_digits=10, decimal_places=2),
        Field(..., description="Price with 2 decimal places")
    ]
    stock_quantity:Annotated[int,Field(...,ge=0,description="Available quantity in stock")]
    description:Annotated[str,Field(...,max_length=500,description="product description")]
    discount:Annotated[int,Field(...,ge=0,le=100,description="Discount of product")]
    category_id:Annotated[UUID,Field(...,description="Reference to category ID")]



    # @computed_field
    # @property
    # def discount_price(self)->float:
    #     return round(self.price-(self.price*(self.discount/100)),2)
    

class ProductResponse(BaseModel):
    id:Optional[Annotated[UUID,Field(...,description="Product id")]]=None
    name:Optional[Annotated[str,Field(...,max_lengh=255,description="Name of the product")]]=None
    price: Optional[Annotated[
        condecimal(max_digits=10, decimal_places=2),
        Field(..., description="Price with 2 decimal places")
    ]]=None
    stock_quantity:Optional[Annotated[int,Field(...,ge=0,description="Available quantity in stock")]]=None
    description:Optional[Annotated[str,Field(...,max_length=500,description="product description")]]=None
    discount:Optional[Annotated[int,Field(...,ge=0,le=100,description="Discount of product")]]=None
    category_id:Optional[Annotated[UUID,Field(...,description="Reference to category ID")]]=None
    # discount_price:Optional[Annotated[float,Field(...,description="discount price of product")]]=None
class ProductListResponse(BaseModel):
    product_list:Optional[List[ProductResponse]]=None
    
class ProductListRequest(BaseModel):
    skip:Optional[int]=0
    limit:Optional[int]=10

class ProductUpdate(BaseModel):
    name:Optional[Annotated[str,Field(...,max_lengh=255,description="Name of the product")]]=None
    price: Optional[Annotated[
        condecimal(max_digits=10, decimal_places=2),
        Field(..., description="Price with 2 decimal places")
    ]]=None
    stock_quantity:Optional[Annotated[int,Field(...,ge=0,description="Available quantity in stock")]]=None
    description:Optional[Annotated[str,Field(...,max_length=500,description="product description")]]=None
    discount:Optional[Annotated[int,Field(...,ge=0,le=100,description="Discount of product")]]=None
    category_id:Optional[Annotated[UUID,Field(...,description="Reference to category ID")]]=None
