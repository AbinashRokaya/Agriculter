from fastapi import APIRouter,Depends,HTTPException,Path,Query,Form
from auth.current_user import require_permission,get_current_user
from uuid import UUID,uuid4
from model.cart_model import CartModel,CarItemModel
from schemas.cart_schema import CartIteamRequest,CartIteamResponse,CartReqest,CartResponse
from repo.cart_repo import CreateCart,ListOrder,UpdateCart,deleteCart
from typing import Optional
from pydantic import Field

route=APIRouter(
    prefix="/cart",
    tags=["cart"]
)

@route.post("/create")
def create_cart(cart_request:CartIteamRequest,current_user=Depends(get_current_user)):
    try:
       return CreateCart(cart_request=cart_request,user_id=current_user["user_id"])
    except Exception as e:
        return HTTPException(status_code=500,detail=str(e))

@route.post("/list")
def cart_list(cursor:Optional[UUID]= Query(None),limit: int = Query(1, gt=0, le=100),current_user=Depends(get_current_user)):
    try:
        return ListOrder(cursor=cursor,limit=limit,user_id=current_user["user_id"])
    except Exception as e:
        return HTTPException(status_code=500,detail=str(e))
    


    
@route.patch("/update/{cart_item_id}")
def update_cart(cart_item_id:UUID,stock_quantaty:int,current_user=Depends(require_permission('view'))):
    try:
        return UpdateCart(cart_items_id=cart_item_id,quantaty=stock_quantaty)
    except Exception as e:
        return HTTPException(status_code=500,detail=str(e))
    
@route.delete("/delete/{cart_items_id}")
def delete_cart(cart_items_id:UUID,current_user=Depends(get_current_user)):
    try:
        return deleteCart(cart_items_id=cart_items_id)
    except Exception as e:
        return HTTPException(status_code=500,detail=str(e))