from fastapi import APIRouter,Request
from auth.auth import oauth
from uuid import uuid4

route=APIRouter(
    prefix="/login",
    tags=['login']
)


@route.get("/")
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