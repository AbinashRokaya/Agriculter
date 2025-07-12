from fastapi import APIRouter,Depends,HTTPException
from auth.current_user import require_permission
from uuid import UUID,uuid4
from model.order_model import OrderModel,OrderItemsModel
from schemas.order_schema import OrderIteamRequest,OrderRequest,OrderIteamResponse,OrderResponse





route=APIRouter(
    prefix="/Order",
    tags=["order"]
)


