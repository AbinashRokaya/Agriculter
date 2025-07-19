from schemas.user_schema import UserRequest, UserResponse
from fastapi import APIRouter, HTTPException, status
from database.database import get_db
from model.user_model import UserModel
from auth.hasing import get_password_hashed
from sqlalchemy import and_,or_
from auth.jwt import create_access_token
from schemas.token_schema import Token,TokenResponse,UserAuthResponse
from domain.common import ErrorCode,StatusMessage,BaseResponse
from fastapi.responses import JSONResponse
from starlette.status import HTTP_409_CONFLICT

route = APIRouter(
    prefix="/api/v1",
    tags=["Register"]
)

@route.post("/register")
def register(user: UserRequest):
    try:
        with get_db() as db:

            existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()

            if existing_user:
               return JSONResponse(
                status_code=409,
                content=TokenResponse(
                    error=True,
                    msg="Email already exists",
                    status_code=ErrorCode.CONFLICT.value,  
                    status=StatusMessage.FAILED.value     
                ).model_dump()
            )

            
            existing_user = db.query(UserModel).filter(UserModel.email == user.name).first()
            if existing_user:
                                
                return JSONResponse(
                    status_code=HTTP_409_CONFLICT,
                    content=TokenResponse(
                        error=True,
                        msg="User already exists",
                        status_code=ErrorCode.CONFLICT,
                        status=StatusMessage.FAILED
                    ).model_dump()
                )
            hased_password=get_password_hashed(user.password)
            new_user = UserModel(
                name=user.name,
                email=user.email,
                password=hased_password
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            access_token=create_access_token({"email":new_user.email,"role":new_user.role,"user_id":str(new_user.user_id)})
            return JSONResponse(
                status_code=200,
                content=TokenResponse(
                    msg="Registered successfully",
                    status_code=ErrorCode.OK,
                    status=StatusMessage.SUCCESSFULLY,
                     user=UserAuthResponse(
                    token=access_token,
                    user_id=new_user.user_id,
                    user_name=new_user.name,
                    user_email=new_user.email,
                    user_role=new_user.role),

                )
            )

            

    except ValueError as e:
        return JSONResponse(
                    status_code=HTTP_409_CONFLICT,
                    content=TokenResponse(error=True,msg=str(e),status_code=ErrorCode.BAD_REQUEST,status=StatusMessage.FAILED).model_dump()
                )
        
    except Exception as e:
        return JSONResponse(
                    status_code=400,
                    content=TokenResponse(error=True,msg=str(e),status_code=ErrorCode.INTERNAL_ERROR,status=StatusMessage.FAILED).model_dump()
                )
        