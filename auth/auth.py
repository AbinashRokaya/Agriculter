from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from database.database import get_db
from model.user_model import UserModel
from auth.jwt import create_access_token
import os
from schemas.token_schema import IdTokenPayload,TokenResponse

route = APIRouter(prefix="/api/v1/google")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


"""
This is the method of google authenticate. Where  frontend send {id token} and here the {id token} is verify by the google tokens verifaction.
when the veryfaction is True it fetch user data from the token and add all the data in database. In database if it is authenticate from the google is write True in is_google_auth 
other wise fase. This function give the response of token,token_type and user details
"""

@route.post("/auth",response_model=TokenResponse)
async def google_auth_via_post(payload: IdTokenPayload):
    token = payload.id_token
    if not token:
        raise HTTPException(status_code=400, detail="No ID token provided")

    try:
        id_info = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_email = id_info["email"]
    user_name = id_info.get("name")
    user_id = id_info["sub"]

    with get_db() as db:
        user = db.query(UserModel).filter(UserModel.email == user_email).first()
        if not user:
            user = UserModel(
                name=user_name,
                email=user_email,
                password=None,
                is_google_auth=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)

    access_token = create_access_token({
        "email": user.email,
        "role": user.role,
        "user_id": str(user.user_id)
    })

    return TokenResponse(access_token=access_token,token_type="bear",
                         user_id=user.user_id,
                         user_name=user.name,
                         user_email=user.email,
                         user_role=user.role)
