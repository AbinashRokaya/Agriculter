from database.database import get_db
from model.cart_model import CartModel,CarItemModel
from model.product_model import ProductModel
from model.user_model import UserModel
from fastapi import HTTPException,status
from uuid import UUID
from schemas.cart_schema import CartIteamRequest,CartIteamResponse,CartReqest,CartResponse,CartPaganitionResponse,CartProductResponse
from sqlalchemy import and_,or_

def CreateCart(cart_request:CartIteamRequest,user_id:UUID):
    with get_db() as db:
        user=db.query(UserModel).filter(UserModel.user_id==user_id).first()
        if not user:
            raise HTTPException(status_code=404,detail="user not found")
        exist_cart=db.query(CartModel).filter(CartModel.user_id==user_id).first()
        product=db.query(ProductModel).filter(ProductModel.product_id==cart_request.product_id).first()
        if not product:
            raise HTTPException(status_code=404,detail="product not found")
        
       
        if not exist_cart:
            cart=CartModel(
                user_id=user_id
            )
            db.add(cart)
            db.commit()
            db.refresh(cart)
            exist_cart=db.query(CartModel).filter(CartModel.user_id==user_id).first()

        
        cart_item=CarItemModel(
            cart_id=exist_cart.cart_id,
            product_id=cart_request.product_id,
            stock_quantaty=cart_request.stock_quantaty
        )
        if check_quantay(cart_item.product.stock_quantity,cart_request.stock_quantaty):
            db.add(cart_item)
            db.commit()
            db.refresh(cart_item)

            return {"message":f"new product {cart_request.product_id} is added to card "}
        else:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f"your stock quantaty {quantaty} is greater than actual stock quantaty")
        


def ListOrder(cursor:UUID,limit:int,user_id:UUID):
    with get_db() as db:
     

        query=db.query(CarItemModel).filter(CartModel.user_id == user_id)

        if cursor:
            query=query.filter(CarItemModel.product_id>cursor)

        query=query.order_by(CarItemModel.product_id).limit(limit+1)
        items=query.all()
        if not items:
            raise HTTPException(status_code=404,detail="cart not found")
        next_cursor=None

        if len(items)>limit:
            next_cursor=items[-1].order_items_id
            items=items[:limit]

        list_data=[CartResponse(
            cart_items_id=c.cart_items_id,
            user_id=c.cart.user.user_id,
            cart_id=c.cart.cart_id,
            product=CartProductResponse(
                id=c.product.product_id,
                name=c.product.name,
                price=c.product.price,
                description=c.product.description,
                discount=c.product.discount,
                category_name=c.product.category.name,
                image=c.product.image,
                coverimage=c.product.coverimage


            ),
            stock_quantaty=c.stock_quantaty
        )for c in items]

        return CartPaganitionResponse(cart_list=list_data,next_cursor=next_cursor)


def UpdateCart(cart_items_id:UUID,quantaty:int):
    with get_db() as db:
        cart_items=db.query(CarItemModel).filter(CarItemModel.order_items_id==cart_items_id).first()
        if not cart_items:
            raise HTTPException(status_code=404,detail="cart not found")
        if check_quantay(cart_items.product.stock_quantity,quantaty):
            cart_items.stock_quantaty=quantaty
            db.commit()

            return {"message":f"quantaty {quantaty} update"}
        else:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f"your stock quantaty {quantaty} is greater than actual stock quantaty")
        


def check_quantay(act_quant,user_quant):
    if act_quant<user_quant:
        return False
    else:
        return True
    
def deleteCart(cart_items_id:UUID):
    with get_db() as db:
        cart_items=db.query(CarItemModel).filter(CarItemModel.order_items_id==cart_items_id).first()
        if not cart_items:
            raise HTTPException(status_code=404,detail="cart not found")
        db.delete(cart_items)
        db.commit()
        return {"message":f"cart items {cart_items.product.name} is deleted"}