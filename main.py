from fastapi import FastAPI,Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from auth import auth, login,register
from starlette.config import Config
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from authlib.integrations.starlette_client import OAuth
import uvicorn
import os
from auth.current_user import get_current_user
from database.database import engine,Base
from auth.current_user import require_permission,Action
from route import (user_route,superamin_route,product_route,category_route,
                   cart_route)
from auth.superadmin import create_superadmin




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
app.include_router(login.route)
app.include_router(register.route)
app.include_router(user_route.route)
app.include_router(superamin_route.route)
app.include_router(product_route.route)
app.include_router(category_route.route)
app.include_router(cart_route.route)

@app.get("/")
async def homepage():
    return HTMLResponse('<a href="abi/login">Login with Google</a>')

@app.get("/chat")
async def get_response(current_user = Depends(require_permission("view"))):
    return {"message": f"{current_user['user_role']} can view"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, loop="asyncio", )


