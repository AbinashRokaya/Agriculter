from fastapi import APIRouter,Depends,HTTPException,Query,Path
from auth.current_user import require_permission,get_current_user
from uuid import UUID,uuid4
from model.order_model import OrderModel,OrderItemsModel
from schemas.order_schema import (OrderIteamRequest,OrderRequest,
                                  OrderItemsResponse,OrderResponse,
                                  OrderItemsListRequest)
from repo.order_repo import CreateOrderItems,orderList,updateOrder,search_from_status
from schemas.order_schema import OrderStatus
from typing import Optional


route=APIRouter(
    prefix="/api/v1/Order",
    tags=["order"]
)


@route.post("/create")
def create_cart(order_request:OrderItemsListRequest,current_user=Depends(get_current_user)):
    try:
       return CreateOrderItems(order_items_req=order_request,user_id=current_user["user_id"])
    except Exception as e:
        return HTTPException(status_code=500,detail=str(e))
    
@route.get("/list")
def order_list(cursor: Optional[UUID] = Query(None),limit: int = Query(1, gt=0, le=100),current_user=Depends(get_current_user)):
    try:
        return orderList(cursor=cursor,limit=limit,user_id=current_user["user_id"])
       
    except Exception as e:
        return HTTPException(status_code=500,detail=str(e))
    
@route.patch("/admin/update/{order_id}")
def update_order(order_id:UUID,status:OrderStatus,current_user=Depends(require_permission('edit'))):
    try:
        return updateOrder(order_id=order_id,order_status=status)

    except Exception as e:
        return HTTPException(status_code=500,detail=str(e))

@route.get("/admin/list")
def order_list(cursor: Optional[UUID] = Query(None),limit: int = Query(1, gt=0, le=100),current_user=Depends(require_permission('edit'))):
    try:
        return orderList(cursor=cursor,limit=limit,user_id=current_user["user_id"])
       
    except Exception as e:
        return HTTPException(status_code=500,detail=str(e))
        

@route.get("/admin/search_status")
def search_status(
    cursor: Optional[UUID]=Query(None) ,  # <- Fixed: use Path() for path parameters
    limit: int = Query(1, gt=0, le=100),
    status: OrderStatus = Query(OrderStatus.Pending),
    current_user=Depends(require_permission("edit"))
):
    try:
        return search_from_status(cursor=cursor, limit=limit, order_status=status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))