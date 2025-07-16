from pydantic import BaseModel,Field
from typing import Annotated
from uuid import UUID

class Token(BaseModel):
    access_token:Annotated[str,Field(...,description="Jwt token")]
    token_type:Annotated[str,Field(...,description="token type")]




class IdTokenPayload(BaseModel):
    id_token: str = Field(..., description="Google ID token")


class TokenResponse(BaseModel):
    access_token: Annotated[str, Field(..., description="JWT access token")]
    token_type: Annotated[str, Field(..., description="Token type")]
    user_id:UUID
    user_name:str
    user_role:str
    user_email:str

