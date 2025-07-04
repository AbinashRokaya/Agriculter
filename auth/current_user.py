from fastapi import HTTPException,Cookie,status,Depends
from jose import jwt, ExpiredSignatureError, JWTError
from dotenv import load_dotenv
import os
import traceback
from database.database import get_db
from fastapi.security import OAuth2PasswordBearer
from uuid import uuid4
from schemas.role_schema import ROLE_PERMISSIONS,Action,Role
from datetime import datetime
from pydantic import ValidationError
from model.user_model import UserModel
import jwt
import json

load_dotenv(override=True)

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_MINUTES=os.getenv("ACCESS_TOKEN_MINUTES")




oauth2_schema=OAuth2PasswordBearer(tokenUrl='/manual/login')
def get_current_user(token: str = Depends(oauth2_schema)):
    with get_db() as db:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            token_data = payload.get("sub")

            try:
                token_data = json.loads(token_data)
            except Exception:
                raise HTTPException(status_code=403, detail="Invalid token data")

            user_email = token_data.get("email")
            user_role = token_data.get("role")
            user_id = token_data.get("user_id")

            if not user_email:
                raise HTTPException(status_code=403, detail="Email missing in token")

            authenticate_user = db.query(UserModel).filter(UserModel.email == user_email).first()
            if not authenticate_user:
                raise HTTPException(status_code=404, detail="User not found")

            return {
                "user_id": user_id,
                "user_email": user_email,
                "user_role": user_role
            }

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"}
            )
        except (jwt.PyJWTError, ValidationError):
            raise HTTPException(
                status_code=403,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )

def validate_user_request(token: str = Cookie(None)):
    session_details = get_current_user(token)

    return session_details


def require_permission(action:Action):
    def dependency(user=Depends(get_current_user)):
        role=user["user_role"]

        if action not in ROLE_PERMISSIONS.get(Role(role),set()):
             raise HTTPException(
                status_code=403,
                detail=f"{role} is not allowed to perform '{action}'"
            )
        return user
    return dependency