from jose import jwt, ExpiredSignatureError, JWTError
from jwt.exceptions import InvalidTokenError
import os 
from datetime import datetime,timedelta
from typing import Union,Any
from dotenv import load_dotenv
import os
import json


load_dotenv(override=True)

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_MINUTES=int(os.getenv("ACCESS_TOKEN_MINUTES"))

def create_access_token(subject: dict, expires_delta: timedelta = None):
    if expires_delta:
            expires_delta=datetime.utcnow()+expires_delta
    else:
        expires_delta=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_MINUTES)

    to_encode={"exp":expires_delta,"sub":json.dumps(subject)}
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,ALGORITHM)

    return encoded_jwt





