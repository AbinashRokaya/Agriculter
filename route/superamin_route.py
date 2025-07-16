from fastapi import Depends,APIRouter,HTTPException
from model.user_model import UserModel
from auth.current_user import require_permission
from schemas.role_schema import AssignRoleRequest
from repo.superadmin_repo import RollAssing,AdminList
from schemas.superadmin_schema import AdminListRequest,AdminListResponse,Admin


route=APIRouter(
    prefix="/api/v1/SuperAdmin",
    tags=["SuperAdmin"]
)


@route.post("/rolleAssin")
def assing_role(request:AssignRoleRequest,current_user=Depends(require_permission('role_assign'))):
    try:
        return RollAssing(request=request)
    
    except Exception as e:
        return HTTPException(status_code=500,detail=f"{e}")
    
@route.post("/admin/list")
def admin_list(request:AdminListRequest,current_user=Depends(require_permission('role_assign'))):
    try:
        admin_list=AdminList(request=request)
        list=[Admin(
            user_id=admin.user_id,
            name=admin.name,
            email=admin.email,
            role=admin.role
        )for admin in admin_list]

        return AdminListResponse(admin=list)
    
    except Exception as e:
        return HTTPException(status_code=500,detail=f"{e}")
    
# @route.patch("/admin/update/{user_id}")
# def update_admin(user_id:str,current_user=Depends(require_permission('role_assign'))):
    
    



    



