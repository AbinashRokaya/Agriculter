from fastapi import APIRouter,Request,Depends,HTTPException,status
from auth.hasing import verify_password
from auth.jwt import create_access_token
from schemas.token_schema import Token,TokenResponse,UserAuthResponse
from fastapi.security import OAuth2PasswordRequestForm
from database.database import get_db
from model.user_model import UserModel
from sqlalchemy import and_,or_
from domain.common import ErrorCode,StatusMessage,BaseResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse


route=APIRouter(
    prefix=("/api/v1/auth"),
    tags=['login']
)


@route.post("/login",response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        with get_db() as db:
            get_user=db.query(UserModel).filter(or_(UserModel.email==form_data.username,UserModel.name==form_data.username)).first()
            if not get_user:
                 return JSONResponse(
                     status_code=404,
                     content=TokenResponse(error=True,
                                           msg="User name not found",
                                           status_code=ErrorCode.NOT_FOUND,
                                           status=StatusMessage.FAILED).model_dump()
                 )
                 
            
            if not verify_password(form_data.password,get_user.password):
                return JSONResponse(
                     status_code=401,
                     content=TokenResponse(error=True,
                                           msg="password is incorrect",
                                           status_code=ErrorCode.NOT_FOUND,
                                           status=StatusMessage.FAILED).model_dump()
                 )
                
            access_token=create_access_token(subject={"email":get_user.email,"role":get_user.role,"user_id":str(get_user.user_id)})

            return JSONResponse(
                status_code=200,
                content=TokenResponse(
                    msg="login successfully",
                    status_code=ErrorCode.OK,
                    status=StatusMessage.SUCCESSFULLY,
                     user=UserAuthResponse(
                    token=access_token,
                    user_id=get_user.user_id,
                    user_name=get_user.name,
                    user_email=get_user.email,
                    user_role=get_user.role),

                )
            )
            
    except ValueError as e:
         return JSONResponse(
                    status_code=400,
                    content=TokenResponse(error=True,msg=str(e),status_code=ErrorCode.BAD_REQUEST,status=StatusMessage.FAILED).model_dump()
                )
        
    except Exception as e:
        return JSONResponse(
                    status_code=500,
                    content=TokenResponse(error=True,msg=str(e),status_code=ErrorCode.INTERNAL_ERROR,status=StatusMessage.FAILED).model_dump()
                )
        

