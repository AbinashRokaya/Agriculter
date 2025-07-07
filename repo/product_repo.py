from database.database import get_db
from schemas.product_schema import ProductCreate,ProductListRequest,ProductUpdate
from uuid import UUID
from model.product_model import ProductModel
from model.category_model import CategoryModel
from fastapi import HTTPException


def create_product(request:ProductCreate):
    with get_db() as db:
        existing_product=db.query(ProductModel).filter(ProductModel.name==request.name).first()

        if  not existing_product:
            raise HTTPException(status_code=409,detail="Product alredy exists")
        
        exixting_category=db.query(CategoryModel.category_id==request.category_id).first()
        if not exixting_category:
            raise HTTPException(status_code=404,detail="Category is not found")
        
        new_product=ProductModel(
    
            name=request.name,
            stock_quantity=request.stock_quantity,
            description=request.description,
            discount=request.discount,
            category_id=exixting_category.category_id
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return new_product
    

def productList(request:ProductListRequest):
    with get_db() as db:
        list_p=db.query(ProductModel).offset(request.skip).limit(request.limit).all()

        
        return list_p


def GetProductById(request:UUID):
    with get_db() as db:
        product=db.query(ProductModel).filter(ProductModel.product_id==request).first()
        return product
    
def UpdateProduct(product_id:UUID,value_update:ProductUpdate):
    with get_db() as db:
        product=db.query(ProductModel).filter(ProductModel.product_id==product_id).first()

        if not product:
            raise HTTPException(status_code=404,detail="Product not found")
        
        update_data=value_update.dict(exclude_unset=True)
        
        for Key,value in update_data.items():
            setattr(product,Key,value)


        db.commit()
        db.refresh(product)

        return {"detail":f"{product_id} is updated"}
    
def DeleteProduct(product_id:UUID):
    with get_db() as db:
        product=db.query(ProductModel).filter(ProductModel.product_id==product_id).first()
        if not product:
            raise HTTPException(status_code=404,detail="Product not found")
        
        db.delete(product)
        db.commit()

        return {"message":f"Product:{product.name} is deleted"}
    
def GetProductName(product_name:str):
    with get_db() as db:
        product=db.query(ProductModel).filter(ProductModel.name.like(f"{product_name}")).first()

        return product
    