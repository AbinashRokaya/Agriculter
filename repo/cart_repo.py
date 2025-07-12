from database.database import get_db
from model.cart_model import CartModel,CarItemModel
from model.product_model import ProductModel
from model.user_model import UserModel
from fastapi import HTTPException
from uuid import UUID
from schemas.cart_schema import CartIteamRequest,CartIteamResponse,CartReqest,CartResponse


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
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)

        return {"message":f"new product {cart_request.product_id} is added to card "}
