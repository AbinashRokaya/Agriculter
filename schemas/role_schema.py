from enum import Enum
from typing import Literal
from uuid import UUID
from pydantic import BaseModel


class Role(str,Enum):
    User="User"
    SuperAdmin="SuperAdmin"
    Admin="Admin"

Action=Literal["view","edit","write","delete","role_assign"]

ROLE_PERMISSIONS: dict[Role, set[Action]] = {
    Role.User: {"view"},
    Role.Admin: {"view", "edit"},
    Role.SuperAdmin: {"view", "edit", "write","delete","role_assign"},
}

class AssignRoleRequest(BaseModel):
    user_id: UUID
    new_role: Role