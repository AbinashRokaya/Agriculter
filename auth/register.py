from schemas.user_schema import UserRequest, UserResponse
from fastapi import APIRouter, HTTPException, status
from database.database import get_db
from model.user_model import UserModel
from auth.hasing import get_password_hashed
from sqlalchemy import and_,or_
route = APIRouter(
    prefix="/api/v1",
    tags=["Register"]
)

@route.post("/register", status_code=status.HTTP_201_CREATED)
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

            return {"register sussfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
