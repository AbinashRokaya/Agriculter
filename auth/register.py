from schemas.user_schema import UserRequest, UserResponse
from fastapi import APIRouter, HTTPException, status
from database.database import get_db
from model.user_model import UserModel
from auth.hasing import get_password_hashed
from sqlalchemy import and_,or_
from auth.jwt import create_access_token
from schemas.token_schema import Token,TokenResponse,UserAuthResponse
route = APIRouter(
    prefix="/api/v1",
    tags=["Register"]
)

@route.post("/register", status_code=status.HTTP_201_CREATED,response_model=TokenResponse)
def register(user: UserRequest):
    try:
        with get_db() as db:

            existing_user = db.query(UserModel).filter(and_(UserModel.email == user.email,UserModel.name==user.name)).first()

            if existing_user:
                raise HTTPException(status_code=409, detail="User already exists")
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

            return TokenResponse(
                token=Token(
                    access_token=access_token,token_type="bear",
                         
                ),
                user=UserAuthResponse(
                        user_id=new_user.user_id,
                        user_name=new_user.name,
                        user_email=new_user.email,
                        user_role=new_user.role),
                message="register successfully"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
