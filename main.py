from fastapi import FastAPI,Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from auth import auth, login
from starlette.config import Config
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from authlib.integrations.starlette_client import OAuth
import uvicorn
import os
from auth.current_user import get_current_user
from database.database import engine,Base



load_dotenv()

app = FastAPI()

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Correct place and syntax
app.include_router(auth.route)


@app.get("/")
async def homepage():
    return HTMLResponse('<a href="abi/login">Login with Google</a>')

@app.get("/chat")
async def get_response(current_user: dict = Depends(get_current_user)):
    return {"message": "Welcome!", "user": current_user}
