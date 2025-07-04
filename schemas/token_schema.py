from pydantic import BaseModel,Field
from typing import Annotated

class Token(BaseModel):
    access_token:Annotated[str,Field(...,description="Jwt token")]
    token_type:Annotated[str,Field(...,description="token type")]