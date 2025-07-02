from enum import Enum

class Role(str,Enum):
    User="User"
    SuperAdmin="SuperAdmin"
    Admin="Admin"