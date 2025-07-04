from enum import Enum
from typing import Literal



class Role(str,Enum):
    User="User"
    SuperAdmin="SuperAdmin"
    Admin="Admin"

Action=Literal["view","edit","write","delete"]

ROLE_PERMISSIONS: dict[Role, set[Action]] = {
    Role.User: {"view"},
    Role.Admin: {"view", "edit"},
    Role.SuperAdmin: {"view", "edit", "write","delete","role_assign"},
}