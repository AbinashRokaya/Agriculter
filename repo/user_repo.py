from database.database import get_db
from schemas.user_schema import GetUserResponse,UpdateUserRequest,UpdateUserResponse,ListUserRequest
from uuid import uuid4
from model.user_model import UserModel
from fastapi import HTTPException

def get_user_detail(email:str):

    with get_db() as db:
        user=db.query(UserModel).filter(UserModel.email==email).first()
        if user:
            print(user)
            return user
    return None


def update_user_me(user_id:uuid4,upate_user_value:UpdateUserRequest):
    with get_db() as db:
        user=db.query(UserModel).filter(UserModel.user_id==user_id).first()

        if not user:
            raise HTTPException(status_code=404,detail="user not found")
        
        update_data=upate_user_value.dict(exclude_unset=True)

        for Key,value in update_data.items():
            setattr(user,Key,value)

        db.commit()
        db.refresh(user)

        return {"detail":f"{user_id} is updated"}
    


def update_user(user_id:uuid4,upate_user_value:UpdateUserRequest):
    with get_db() as db:
        user=db.query(UserModel).filter(UserModel.user_id==user_id).first()

        
        update_data=upate_user_value.dict(exclude_unset=True)

        for Key,value in update_data.items():
            setattr(user,Key,value)

        db.commit()
        db.refresh(user)

        return {"detail":f"{user_id} is updated"}
    

    

def userDelete(user_id:uuid4):
    with get_db() as db:
        user=db.query(UserModel).filter(UserModel.user_id==user_id).first()
        if not user:
            raise HTTPException(status_code=404,detail="user not found")
        
        db.delete(user)
        db.commit()

        return {"message": f"User:{user_id} deleted successfully"}
    
def GetAllUser(request:ListUserRequest):
    with get_db() as db:
        users=db.query(UserModel).offset(request.skip).limit(request.limit).all()

        if not users:
            raise HTTPException(status_code=404,detail="not found")
        
        return users




