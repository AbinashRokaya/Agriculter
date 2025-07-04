from schemas.user_schema import GetUserRequest,GetUserResponse,UpdateUserRequest,ListUserRequest,ListUserResponse,User
from auth.current_user import get_current_user,require_permission
from fastapi import Depends,APIRouter,HTTPException
from repo.user_repo import get_user_detail,update_user,userDelete,GetAllUser
from uuid import uuid4

route=APIRouter(
    prefix="/user",
    tags=["user details"]
)

@route.get("/detail",response_model=GetUserResponse)
def get_user_by_id(current_user=Depends(require_permission("view"))):
    try:
        print(current_user)
        req=get_user_detail(email=current_user["user_email"])
        req=GetUserResponse(
            name=req.name,
            email=req.email
        )
        return req

    except Exception as e:
        return HTTPException(status_code=500,detail=f"{e}")
    
@route.patch("/update/{user_id}")
def user_detail_update(user_id:str,update_user_value:UpdateUserRequest,current_user=Depends(require_permission("edit"))):
    try:
        return update_user(user_id=user_id,upate_user_value=update_user_value)
    except Exception as e:
        return HTTPException(status_code=500,detail=f"{e}")
    
@route.delete("/delete/{user_id}")
def user_delete(user_id:str,current_user=Depends(require_permission("delete"))):
    try:
        req=userDelete(user_id=user_id)
        return req
    except Exception as e:
        return HTTPException(status_code=500,detail=f"{e}")
    
@route.post("/user/all")
def get_user_all(request:ListUserRequest,current_user=Depends(require_permission("edit"))):
    try:
        list_user=GetAllUser(request=request)

        list_response=[User(
            user_id=user.user_id,
            name=user.name,
            email=user.email,
            role=user.role,

        ) for user in list_user]

        req=ListUserResponse(users=list_response)
        return req

    except Exception as e:
        return HTTPException(status_code=500,detail=f"{e}")
    


    

