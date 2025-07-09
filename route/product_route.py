from fastapi import APIRouter,Depends,HTTPException,Path,Query,Form
from auth.current_user import require_permission
from uuid import UUID,uuid4
from model.product_model import ProductModel
from schemas.product_schema import ProductCreate,ProductResponse,ProductListRequest,ProductListResponse,ProductUpdate,ProductCreatewithImage,ProductPaganationResponse
from repo.product_repo import createProduct,productList,GetProductById,UpdateProduct,DeleteProduct,GetProductName
from pydantic import Field
from typing import List,Optional
import json
from fastapi import UploadFile,File
from fastapi.staticfiles import StaticFiles
import os,shutil

route=APIRouter(
    prefix="/product",
    tags=["Product"]
)
route.mount("/uploads",StaticFiles(directory="static/uploads"),name="uploads")

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@route.post("/create")
def product_create(
    name: str = Form(...),
    price: float = Form(...),
    stock_quantity: int = Form(...),
    description: str = Form(...),
    discount: int = Form(...),
    category_id: UUID = Form(...),
    image: UploadFile = File(...),
    coverimage: List[UploadFile] = File(...),
    current_user=Depends(require_permission("edit"))):
    try:
        if len(coverimage) < 3:
            raise HTTPException(status_code=400, detail="At least 3 cover images are required.")
        
        
        image_filename = f"{uuid4()}_{image.filename}"
        image_path = os.path.join(UPLOAD_DIR, image_filename)
        with open(image_path, "wb") as f:
            shutil.copyfileobj(image.file, f)

        # Save cover images
        cover_paths = []
        for cover in coverimage:
            cover_filename = f"{uuid4()}_{cover.filename}"
            cover_path = os.path.join(UPLOAD_DIR, cover_filename)
            with open(cover_path, "wb") as f:
                shutil.copyfileobj(cover.file, f)
            cover_paths.append(f"/static/uploads/{cover_filename}")

       

        product = ProductCreatewithImage( name=name,
                price=price,
                stock_quantity=stock_quantity,
                description=description,
                discount=discount,
                category_id=category_id,
                image=f"/static/uploads/{image_filename}",
                coverimage=cover_paths)

        new_product=createProduct(product)
       

        return {"message":f"new product: {new_product} is added"}
    
    except Exception as e:
        return HTTPException(status_code=500,detail=str(e))
    
@route.get("/list")
def product_list(cursor: Optional[UUID] = Query(None),limit: int = Query(1, gt=0, le=100),current_user=Depends(require_permission('view'))):
    try:
        return productList(cursor=cursor,limit=limit)
       
    except Exception as e:
        return HTTPException(status_code=500,detail=str(e))
    

@route.get("/{product_id}")
def get_product_by_id(product_id:UUID,current_user=Depends(require_permission("edit"))):
    try:
        list_product=GetProductById(request=product_id)
        if not list_product:
             raise HTTPException(status_code=404,detail="not found")
        return ProductResponse(
                id=list_product.product_id,
                name=list_product.name,
                price=list_product.price,
                stock_quantity=list_product.stock_quantity,
                description=list_product.description,
                discount=list_product.discount,
                category_id=list_product.category_id
            )
        
    except Exception as e:
        return HTTPException(status_code=500,detail=str(e))

@route.patch('/update/{product_id}')
def update_product(product_id:UUID,update_value:ProductUpdate,current_user=Depends(require_permission("edit"))):
    try:
        return UpdateProduct(product_id=product_id,value_update=update_value)
    
    except Exception as e:
        return HTTPException(status_code=500,detail=str(e))
    
@route.delete('/delete/{product_id}')
def delete_product(product_id:UUID,current_user=Depends(require_permission("edit"))):
    try:
        return DeleteProduct(product_id=product_id)
    
    except Exception as e:
        return HTTPException(status_code=500,detail=f"{e}")
    
@route.get("/product_by_name/{product_name}")
def get_product_by_name(product_name:str=Path(...,max_length=255),current_user=Depends(require_permission("view"))):
    try:
        list_product=GetProductName(product_name=product_name)
        if not list_product:
             raise HTTPException(status_code=404,detail="not found")
        list=[ProductResponse(
                id=prod.product_id,
                name=prod.name,
                price=prod.price,
                stock_quantity=prod.stock_quantity,
                description=prod.description,
                discount=prod.discount,
                category_id=prod.category_id
            ) for prod in list_product]
        return ProductListResponse(product_list=list)
    except Exception as e:
        return HTTPException(status_code=500,detail=str(e))


    

    