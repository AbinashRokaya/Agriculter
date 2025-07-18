from pydantic import BaseModel,Field
from typing import Annotated
from uuid import UUID
from typing import Optional
from schemas.role_schema import Role

class Token(BaseModel):
    access_token:Optional[Annotated[str,Field(...,description="Jwt token")]]=None
    token_type:Optional[Annotated[str,Field(...,description="token type")]]=None




class IdTokenPayload(BaseModel):
    id_token: str = Field(..., description="Google ID token")

class UserAuthResponse(BaseModel):
    user_id:Optional[UUID]=None
    user_name:Optional[str]=None
    user_role:Optional[Role]=None
    user_email:Optional[str]=None

class TokenResponse(BaseModel):
   token:Optional[Token]=None
   user:Optional[UserAuthResponse]=None
   message:Optional[str]=None
    

