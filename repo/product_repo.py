from database.database import get_db
from schemas.product_schema import ProductCreate,ProductListRequest,ProductUpdate,ProductCreatewithImage,ProductResponse,ProductPaganationResponse
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
             price=round(request.price,2), 
            stock_quantity=request.stock_quantity,
            description=request.description,
            discount=request.discount,
            category_id=request.category_id,
            image=request.image,
            coverimage=request.coverimage if isinstance(request.coverimage, list) else []

        )
        # for r in request:
        #     print(r)

        # print({k: v for k, v in vars(new_product).items() if not k.startswith("_")})


        
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return new_product
    

def productList(cursor:UUID,limit:int):
    with get_db() as db:

        
        query = db.query(ProductModel)

        if cursor:
            query = query.filter(ProductModel.product_id > cursor)

        query = query.order_by(ProductModel.product_id).limit(limit + 1)
        items = query.all()
        print(items)

        next_cursor = None
        if len(items) > limit:
            next_cursor = items[-1].product_id
            items = items[:limit]

        

        list_data = [
            ProductResponse(
                id=prod.product_id,
                name=prod.name,
                price=prod.price,
                stock_quantity=prod.stock_quantity,
                description=prod.description,
                discount=prod.discount,
                category_id=prod.category_id,
                image=prod.image,
                coverimage=prod.coverimage
            )
            for prod in items
]
      
        


        return ProductPaganationResponse(product_list=list_data,next_cursor=next_cursor)


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
    