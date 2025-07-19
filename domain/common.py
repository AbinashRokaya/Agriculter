from pydantic import BaseModel
from typing import Optional
from enum import Enum

class ErrorCode(Enum):
    UNKNOWN = 0
    OK=200
    INVALID_REQUEST = 400
    NOT_FOUND = 404
    INTERNAL_ERROR = 500
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    BAD_REQUEST = 400
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    SERVICE_UNAVAILABLE = 503
    RATE_LIMIT_EXCEEDED = 429
    TOO_MANY_REQUESTS = 429
    GATEWAY_TIMEOUT = 504

class StatusMessage(str, Enum):
    SUCCESSFULLY = "Success"
    FAILED = "Fail"

class BaseResponse(BaseModel):
    status: StatusMessage = StatusMessage.SUCCESSFULLY
    error: Optional[bool] = False
    status_code: Optional[ErrorCode] = None
    msg: Optional[str] = None

class Debug(BaseModel):
    debug_id: Optional[str] = None
    trace_id: Optional[str] = None
    request_id: Optional[str] = None

class BaseRequest(BaseModel):
    authorization: Optional[str] = None
    debug: Optional[Debug] = None

class PublicRequest(BaseModel):
    pass
