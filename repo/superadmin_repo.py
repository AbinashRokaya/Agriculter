from database.database import get_db
from uuid import UUID
from fastapi import HTTPException
from model.user_model import UserModel
from schemas.role_schema import AssignRoleRequest



def RollAssing(request:AssignRoleRequest):
    with get_db() as db:
        user=db.query(UserModel).filter(UserModel.user_id==request.user_id).first()

        if not user:
            raise HTTPException(status_code=404,detail=f"user id {request.user_id} not found")
        
        user.role=request.new_role
        db.commit()

        return {"message":f"user {user.name} is assigned new role {request.new_role}"}