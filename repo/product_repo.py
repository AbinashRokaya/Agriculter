from database.database import get_db
from schemas.product_schema import ProductCreate,ProductListRequest,ProductUpdate,ProductCreatewithImage
from uuid import UUID
from model.product_model import ProductModel
from model.category_model import CategoryModel
from fastapi import HTTPException
from fastapi import File,UploadFile,Depends


def createProduct(request:ProductCreatewithImage):
    with get_db() as db:
        existing_product=db.query(ProductModel).filter(ProductModel.name==request.name).first()

        if  existing_product:
            raise HTTPException(status_code=409,detail="Product alredy exists")
        
        exixting_category = db.query(CategoryModel).filter(CategoryModel.category_id == request.category_id).first()

        if not exixting_category:
            raise HTTPException(status_code=404,detail="Category is not found")
        
        new_product=ProductModel(
    
            name=request.name,
             price=request.price, 
            stock_quantity=request.stock_quantity,
            description=request.description,
            discount=request.discount,
            category_id=request.category_id,
            image=request.image,
            coverimage=request.coverimage if isinstance(request.coverimage, list) else []

        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return new_product
    

def productList(skip:int,limit:int):
    with get_db() as db:
        list_p=db.query(ProductModel).offset(skip).limit(limit).all()

        
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
        product=db.query(ProductModel).filter(ProductModel.name.like(f"%{product_name}%")).all()

        return product
    