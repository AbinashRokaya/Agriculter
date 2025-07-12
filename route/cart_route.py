from fastapi import APIRouter,Depends,HTTPException,Path,Query,Form
from auth.current_user import require_permission
from uuid import UUID,uuid4
from model.cart_model import CartModel,CarItemModel
from schemas.cart_schema import CartIteamRequest,CartIteamResponse,CartReqest,CartResponse
from repo.cart_repo import CreateCart


route=APIRouter(
    prefix="/cart",
    tags=["cart"]
)

@route.post("/create")
def create_cart(cart_request:CartIteamRequest,current_user=Depends(require_permission("edit"))):
    try:
       return CreateCart(cart_request=cart_request,user_id=current_user["user_id"])
    except Exception as e:
        return HTTPException(status_code=500,detail=str(e))

