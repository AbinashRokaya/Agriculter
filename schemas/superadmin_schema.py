from pydantic import BaseModel
from typing import Optional,List
from uuid import UUID
from schemas.role_schema import Role

class Admin(BaseModel):
    user_id:UUID
    name:Optional[str]=None
    email:Optional[str]=None
    role:Optional[str]=None

class AdminListRequest(BaseModel):
    skip:Optional[int]=0
    limit:Optional[int]=10

class AdminListResponse(BaseModel):
    admin:Optional[List[Admin]]=None


# class UpdateRequest(BaseModel):
#     user_id=UUID
#     roll=Role