from schemas.user_schema import UserRequest, UserResponse
from fastapi import APIRouter, HTTPException, status
from database.database import get_db
from model.user_model import UserModel
from auth.hasing import get_password_hashed

route = APIRouter(
    prefix="/manual",
    tags=["Manual Register"]
)

@route.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserRequest):
    try:
        with get_db() as db:

            existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()

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

            return UserResponse(
                name=new_user.name,
                email=new_user.email
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
