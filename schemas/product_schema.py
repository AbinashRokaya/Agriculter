from pydantic import BaseModel,Field,condecimal,computed_field,conlist,validator
from typing import Annotated,Optional,List
from uuid import UUID,uuid4
from fastapi import UploadFile,File
import re



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
    
    

class ProductCreatewithImage(ProductCreate):
    # @computed_field
    # @property
    # def discount_price(self)->float:
    #     return round(self.price-(self.price*(self.discount/100)),2)
    image: UploadFile = File(...),
    coverimage: List[UploadFile] = File(...)


    @validator('image')
    def validate_image_path(cls, v):
        if not re.match(r"^/static/.+\.(jpg|jpeg|png|gif)$", v, re.IGNORECASE):
            raise ValueError("Image must be a valid static image path (jpg, png, gif)")
        return v

    @validator('coverimage')
    def validate_cover_images(cls, v):
        if len(v) < 3:
            raise ValueError("At least 3 cover images are required.")
        for url in v:
            if not re.match(r"^/static/.+\.(jpg|jpeg|png|gif)$", url, re.IGNORECASE):
                raise ValueError(f"Invalid image path: {url}")
        return v
    

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
    image:Optional[str]=None
    coverimage:Optional[List[str]]=None
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
    image:Optional[Annotated[str,Field(...,description="main image of product")]]=None
    coverimage:Optional[Annotated[List[str],Field(...,description="covers image of produuct")]]=None
