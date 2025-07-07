from pydantic import BaseModel,Field,EmailStr,field_validator
from fastapi import HTTPException
from typing import Annotated,Optional,List
import re
from uuid import uuid4,UUID
# from model.user_model import User

class UserRequest(BaseModel):
    name:Annotated[str,Field(...,max_length=30,description="Name of the user")]
    email:Annotated[EmailStr,Field(...,description="Email of the user")]
    password:Annotated[str,Field(...,description="User password ")]


    @field_validator('password')
    @classmethod
    def check_password_validotor(cls,v:str)->str:

        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.islower() for c in v):
            raise ValueError("Password must include at least one lowercase letter")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must include at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must include at least one digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("Password must include at least one special character")
        if re.search(r'\s', v):
            raise ValueError("Password must not contain spaces")
        return v


class User(BaseModel):
    user_id:UUID
    name:Optional[Annotated[str,Field(...,max_length=30,description="Name of the user")]]=None
    email:Optional[Annotated[EmailStr,Field(...,description="Email of the user")]]=None
    role:Optional[str]=None

class UserResponse(BaseModel):

    name:Optional[Annotated[str,Field(...,max_length=30,description="Name of the user")]]=None
    email:Optional[Annotated[EmailStr,Field(...,description="Email of the user")]]=None


class GetUserRequest(BaseModel):
    user_id:uuid4

class GetUserResponse(BaseModel):
    name:Optional[Annotated[str,Field(...,max_length=30,description="Name of the user")]]=None
    email:Optional[Annotated[EmailStr,Field(...,description="Email of the user")]]=None


class ListUserRequest(BaseModel):
    skip:Optional[int]=0
    limit:Optional[int]=10

class ListUserResponse(BaseModel):
    users:Optional[List[User]]=None

class UpdateUserRequest(BaseModel):
    name:Optional[Annotated[str,Field(...,max_length=30,description="Name of the user")]]=None
    email:Optional[Annotated[EmailStr,Field(...,description="Email of the user")]]=None

class UpdateUserResponse(BaseModel):
    name:Optional[Annotated[str,Field(...,max_length=30,description="Name of the user")]]=None
    email:Optional[Annotated[EmailStr,Field(...,description="Email of the user")]]=None
