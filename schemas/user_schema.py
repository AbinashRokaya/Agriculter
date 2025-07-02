from pydantic import BaseModel,Field,EmailStr,field_validator
from domain.common import BaseRequest,BaseResponse
from fastapi import HTTPException
from typing import Annotated,Optional
import re
# from model.user_model import User

class UserRequest(BaseRequest):
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
    name:Optional[str]=None
    email:Optional[str]=None


class UserResponse(BaseResponse):

    user:Optional[User]=None

