from database.database import get_db
from schemas.category_schema import CategoryResponse,CategoryRequest,CategoryListResponse,CategoryUpdate
from uuid import UUID
from model.category_model import CategoryModel
from fastapi import HTTPException


def CreateCategory(request:CategoryRequest):
    with get_db() as db:
        existing_category=db.query(CategoryModel).filter(CategoryModel.name==request.name).first()

        if  existing_category:
            raise HTTPException(status_code=409,detail="Category alredy exixts")
        
        new_category=CategoryModel(
            name=request.name,
            description=request.description
        )
        db.add(new_category)
        db.commit()
        db.refesh(new_category)

        return new_category
    

def CategoryList(skip:int,limit:int):
    with get_db() as db:
        list_category=db.query(CategoryModel).offset(skip).limit(limit).all()
        return list_category
    

def GetCategoryById(category_id:UUID):
    with get_db() as db:
        category=db.query(CategoryModel).filter(CategoryModel.category_id==category_id).first()
        return category
    
def UpdateCategory(Category_id:UUID,value_update:CategoryUpdate):
    with get_db() as db:
        category=db.query(CategoryModel).filter(CategoryModel.category_id==Category_id).first()

        if not category:
            raise HTTPException(status_code=404,detail="Category not found")
        
        update_data=value_update.dict(exclude_unset=True)

        for key,value in update_data.items():
            setattr(category,key,value)

        db.commit()
        db.refresh(category)

        return {"detail":f"{Category_id} is updated"}
    

def DeleteCategory(category_id:UUID):
    with get_db() as db:
        category=db.query(CategoryModel).filter(CategoryModel.category_id==category_id).first()
        if not category:
            raise HTTPException(status_code=404,detail="Category not found")
        
        db.delete(category)
        db.commit()

        return {'message':f"Category:{category.name} is deleted"}
    
def GetCategoryName(category_name:str):
    with get_db() as db:
        category=db.query(CategoryModel).filter(CategoryModel.name.like(f"%{category_name}%")).all()

        return category