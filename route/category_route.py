from fastapi import APIRouter,Depends,HTTPException,Query,Path
from auth.current_user import require_permission
from uuid import UUID
from model.category_model import CategoryModel
from schemas.category_schema import CategoryListResponse,CategoryRequest,CategoryResponse,CategoryUpdate
from repo.category_repo import CreateCategory,CategoryList,GetCategoryById,GetCategoryName,UpdateCategory,DeleteCategory
from pydantic import Field



route=APIRouter(
    prefix="/api/v1/category",
    tags=["Category"]

)

@route.post("/create")
def category_create(request:CategoryRequest,current_user=Depends(require_permission('edit'))):
    try:
        new_category=CreateCategory(request=request)

        return {"message":f"new category: {new_category.name} is added"}
    
    except Exception as e:
        return HTTPException(status_code=500,detail=f"{e}")
    

@route.get("/list",response_model=CategoryListResponse)
def category_list(skip: int = Query(0), limit: int = Query(10),current_user=Depends(require_permission("view"))):
    try:
        categoryall=CategoryList(skip=skip,limit=limit)

        if not categoryall:
            raise HTTPException(status_code=404,detail="Category not found")
        
        list=[CategoryResponse(
            id=list_category.category_id,
            name=list_category.name,
            description=list_category.description
        )for list_category in categoryall]

        return CategoryListResponse(Category_list=list)
    
    except Exception as e:
        return HTTPException(status_code=500,detail=f"{e}")
    

@route.get("/{category_id}",response_model=CategoryResponse)
def get_category_by_id(category_id:UUID,current_user=Depends(require_permission("edit"))):
    try:
        category=GetCategoryById(category_id=category_id)

        if not category:
            raise HTTPException(status_code=404,detail="category not found")
        
        return CategoryResponse(
            id=category.category_id,
            name=category.name,
            description=category.description
        )
    except Exception as e:
        return HTTPException(status_code=500,detail=f"{e}")
    

@route.patch("/update/{category_id}")
def update_category(category_id:UUID,update_value:CategoryUpdate,current_user=Depends(require_permission("edit"))):
    try:
        return UpdateCategory(category_id=category_id,value_update=update_value)
    
    except Exception as e:
        return HTTPException(status_code=500,detail=f"{e}")
    
@route.delete("/delete/{category_id}")
def delete_category(category_id:UUID,current_user=Depends(require_permission("edit"))):
    try:
        return DeleteCategory(category_id=category_id)
    except Exception as e:
        return HTTPException(status_code=500,detail=f"{e}")
    

@route.get("/category_by_name/{category_name}")
def get_category_by_name(category_name:str=Path(...,max_length=255),current_user=Depends(require_permission("view"))):
    try:
        categoryall=GetCategoryName(category_name=category_name)

        list=[CategoryResponse(
            id=list_category.category_id,
            name=list_category.name,
            description=list_category.description
        )for list_category in categoryall]

        return CategoryListResponse(Category_list=list)
    
    except Exception as e:
        return HTTPException(status_code=500,detail=f"{e}")