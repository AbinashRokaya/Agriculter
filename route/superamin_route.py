from fastapi import Depends,APIRouter,HTTPException
from model.user_model import UserModel
from auth.current_user import require_permission
from schemas.role_schema import AssignRoleRequest
from repo.superadmin_repo import RollAssing


route=APIRouter(
    prefix="/SuperAdmin",
    tags=["SuperAdmin"]
)


@route.post("/rolleAssin")
def assing_role(request:AssignRoleRequest,current_user=Depends(require_permission('role_assign'))):
    try:
        return RollAssing(request=request)
    
    except Exception as e:
        return HTTPException(status_code=500,detail=f"{e}")



