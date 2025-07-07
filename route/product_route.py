from fastapi import APIRouter,Depends,HTTPException,Path
from auth.current_user import require_permission
from uuid import UUID
from model.product_model import ProductModel
from schemas.product_schema import ProductCreate,ProductResponse,ProductListRequest,ProductListResponse,ProductUpdate
from repo.product_repo import create_product,productList,GetProductById,UpdateProduct,DeleteProduct,GetProductName
from pydantic import Field

route=APIRouter(
    prefix="/product",
    tags=["Product"]
)

@route.post("/create")
def product_create(request:ProductCreate,current_user=Depends(require_permission("edit"))):
    try:
        new_product=product_create(request=request)
        return {"message":f"new product: {new_product} is added"}
    
    except Exception as e:
        return HTTPException(status_code=500,detail=f"{e}")
    
@route.post("/list",response_model=ProductResponse)
def product_list(request:ProductListRequest,current_user=Depends(require_permission('view'))):
    try:
        list_product=productList(request=request)
        if not list_product:
             raise HTTPException(status_code=404,detail="not found")
        list=ProductResponse(
                id=list_product.product_id,
                name=list_product.name,
                price=list_product.price,
                stock_quantity=list_product.stock_quantity,
                description=list_product.description,
                discount=list_product.discount,
                category_id=list_product.category_id
            )
        return ProductListResponse(product_list=list)
    except Exception as e:
        return HTTPException(status_code=500,detail=f"{e}")
    

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
        return HTTPException(status_code=500,detail=f"{e}")

@route.patch('/update/{product_id}')
def update_product(product_id:UUID,update_value:ProductUpdate,current_user=Depends(require_permission("edit"))):
    try:
        return UpdateProduct(product_id=product_id,value_update=update_value)
    
    except Exception as e:
        return HTTPException(status_code=500,detail=f"{e}")
    
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
        list=ProductResponse(
                id=list_product.product_id,
                name=list_product.name,
                price=list_product.price,
                stock_quantity=list_product.stock_quantity,
                description=list_product.description,
                discount=list_product.discount,
                category_id=list_product.category_id
            )
        return ProductListResponse(product_list=list)
    except Exception as e:
        return HTTPException(status_code=500,detail=f"{e}")


    

    