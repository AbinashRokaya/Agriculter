from pydantic import BaseModel,Field,condecimal
from typing import Annotated,Optional,List
from uuid import UUID

class CategoryRequest(BaseModel):
    name:Annotated[str,Field(...,max_length=255,description="Name of the Cateogry")]
    description:Annotated[str,Field(...,max_length=500,description="Category description")]


class CategoryResponse(BaseModel):
    id:Optional[UUID]=None
    name:Optional[str]=None
    description:Optional[str]=None

class CategoryListResponse(BaseModel):
    Category_list:Optional[List[CategoryResponse]]=None

class CategoryUpdate(BaseModel):
    name:Annotated[str,Field(...,max_length=255,description="Name of the Cateogry")]
    description:Annotated[str,Field(...,max_length=500,description="Category description")]


