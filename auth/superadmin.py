from database.database import get_db
from model.user_model import UserModel
from fastapi import HTTPException,status
from auth.hasing import get_password_hashed
from schemas.role_schema import Role


def create_superadmin():
    with get_db() as db:
        existing=db.query(UserModel).filter(UserModel.email=="superadmin@gmail.com").first()

        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="superadmin alredy exixts")
        
        superadmin=UserModel(
            name="super admin",
            email="superadmin@gmail.com",
            password=get_password_hashed("Super@123"),
            role=Role.SuperAdmin

        )

        db.add(superadmin)
        db.commit()
        db.refresh(superadmin)

        return {"super admin is created"}