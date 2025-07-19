from pydantic import BaseModel,Field, ConfigDict
from typing import Annotated
from uuid import UUID
from typing import Optional
from schemas.role_schema import Role
from domain.common import ErrorCode,StatusMessage,BaseResponse

class Token(BaseModel):
    access_token:Optional[Annotated[str,Field(...,description="Jwt token")]]=None
    token_type:Optional[Annotated[str,Field(...,description="token type")]]=None




class IdTokenPayload(BaseModel):
    id_token: str = Field(..., description="Google ID token")

class UserAuthResponse(BaseModel):
    token:Optional[str]=None
    user_id:Optional[UUID]=None
    user_name:Optional[str]=None
    user_role:Optional[Role]=None
    user_email:Optional[str]=None

class TokenResponse(BaseResponse):
    user:Optional[UserAuthResponse]=None
    model_config = ConfigDict(use_enum_values=True)
 
    

