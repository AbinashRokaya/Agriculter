from fastapi import APIRouter,Request,Depends,HTTPException
from auth.hasing import verify_password
from auth.jwt import create_access_token
from schemas.token_schema import Token
from fastapi.security import OAuth2PasswordRequestForm
from database.database import get_db
from model.user_model import UserModel

from fastapi.security import OAuth2PasswordBearer
route=APIRouter(
    prefix="/manual",
    tags=['manual login']
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@route.post("/login",response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with get_db() as db:
        get_user=db.query(UserModel).filter(UserModel.email==form_data.username).first()
        if not get_user:
            raise HTTPException(status_code=404,detail=f"User is not foud or email is Incorrect")
        
        if not verify_password(form_data.password,get_user.password):

            raise HTTPException(status_code=400,detail="Incorrect password")
        
        access_token=create_access_token({"email":get_user.email,"role":get_user.role,"user_id":str(get_user.user_id)})

        return {"access_token":access_token,"token_type":"bearer"}
