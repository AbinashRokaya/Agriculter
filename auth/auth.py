from fastapi import APIRouter,Request,HTTPException
from fastapi.responses import RedirectResponse
from datetime import datetime, timedelta
from jose import jwt, ExpiredSignatureError, JWTError
from dotenv import load_dotenv
import os
import uuid
import traceback
from uuid import uuid4
import os
from dotenv import load_dotenv
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from auth.jwt import create_access_token
from database.database import get_db
from model.user_model import UserModel
from schemas.token_schema import Token

load_dotenv(override=True)

route=APIRouter(
    prefix="/abi",

)
config = Config(".env")
oauth = OAuth(config)
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    },
)

@route.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    # Generate a nonce (required for security)
    request.session['nonce'] = str(uuid4())

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri,
        response_type='code',
        nonce=request.session['nonce']  # Pass nonce for ID token
    )
@route.get("/auth",response_model=Token)
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    
    userinfo = None
    try:
        # Try to parse the ID token first
        resp = await oauth.google.get("https://www.googleapis.com/oauth2/v2/userinfo", token=token)
        userinfo=resp.json()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Google authentication failed.")

        # Fallback if id_token is not present or fails
    
    user = token.get("userinfo")
    expires_in = token.get("expires_in")
    user_id = user.get("sub")
    iss = user.get("iss")
    user_name=user.get("name")
    user_email = user.get("email")

    print(userinfo["email"])
    print(userinfo["name"])
  
    if iss not in ["https://accounts.google.com", "accounts.google.com"]:
        raise HTTPException(status_code=401, detail="Google authentication failed.")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Google authentication failed.")
    
    with get_db() as db:
        # The 'name' field is used to store the user's display name from Google in your database.
        # This allows you to show the user's real name in your application UI and associate it with their account.
        # If you don't store the name, you won't be able to display or use it later.
        old_user = db.query(UserModel).filter(UserModel.email == user_email).first()
    
        if not old_user:
            new_user = UserModel(
                name=userinfo["name"],
                email=userinfo["email"],
                password=None,
                is_google_auth=True,
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            user_in_db = new_user
        else:
            user_in_db = old_user

    # Create JWT token
    access_token_expires = timedelta(seconds=expires_in)
    access_token = create_access_token(data={"email":user_in_db.email,"role":user_in_db.role,"user_id":str(user_in_db.user_id)}, expires_delta=access_token_expires)
    
    
    return {"access_token":access_token,"token_type":"bearer"}


    