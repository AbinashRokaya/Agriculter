from database.database import get_db
from model.cart_model import CartModel,CarItemModel
from model.order_model import OrderItemsModel,OrderModel
from model.product_model import ProductModel
from model.user_model import UserModel
from fastapi import HTTPException,status
from uuid import UUID
from sqlalchemy import and_,or_
from schemas.order_schema import OrderIteamRequest,OrderItemsListRequest,OrderStatus,OrderResponse,OrderPaganitionResponse,OrderProductResponse


def CreateOrderItems(order_items_req: OrderItemsListRequest, user_id: UUID):
    with get_db() as db:
        user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        total_amount = 0  # Initialize total amount
        products_map = {}  # To avoid querying product twice

        # Validate and calculate total
        for item in order_items_req.order_items:
            product = db.query(ProductModel).filter(ProductModel.product_id == item.product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail=f"Product with id {item.product_id} not found")

            if not check_quantay(act_quant=product.stock_quantity, user_quant=item.stock_quantaty):
                raise HTTPException(
                    status_code=409,
                    detail=f"Requested quantity ({item.stock_quantaty}) exceeds available stock ({product.stock_quantaty}) for product: {product.name}"
                )
            product.stock_quantity-=item.stock_quantaty
            db.commit()
            products_map[item.product_id] = product  # Cache for second loop
            total_amount += discount_price(discount=product.discount,price=product.price) * item.stock_quantaty  # Accumulate total

        # Create the order
        new_order = OrderModel(
            user_id=user_id,
            total_amount=total_amount,
            status=OrderStatus.Processing,
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        # Create order items
        for item in order_items_req.order_items:
            product = products_map[item.product_id]
            new_order_item = OrderItemsModel(
                order_id=new_order.order_id,
                product_it=item.product_id,
                stock_quantaty=item.stock_quantaty,
                price=discount_price(discount=product.discount,price=product.price)
            )
            db.add(new_order_item)

        db.commit()
        return {"message": "Order created successfully", "order_id": new_order.order_id}
    

def orderList(cursor:UUID,limit:int,user_id:UUID):
    with get_db() as db:
        query = (
            db.query(OrderItemsModel)
            .join(OrderItemsModel.order)  # Make sure this relationship exists
            .filter(OrderModel.user_id == user_id)
        )
        if cursor:
            query=query.filter(OrderItemsModel.product_it>cursor)

        query=query.order_by(OrderItemsModel.product_it).limit(limit+1)
        items=query.all()
        if not items:
            raise HTTPException(status_code=404,detail="order not found")
        next_cursor=None

        if len(items)>limit:
            next_cursor=items[-1].order_items_id
            items=items[:limit]

        list_data=[OrderResponse(
            order_items_id=c.order_items_id,
            user_id=c.order.user_id,
            order_id=c.order.order_id,
             total_amount=c.order.total_amount,
            product=OrderProductResponse(
                id=c.product.product_id,
                name=c.product.name,
                description=c.product.description,
                discount=c.product.discount,
                category_name=c.product.category.name,
                image=c.product.image,
                coverimage=c.product.coverimage


            ),
            status=c.order.status,
            price=c.price,
            stock_quantaty=c.stock_quantaty
            )for c in items]

        return OrderPaganitionResponse(order_list=list_data,next_cursor=next_cursor)

def orderListAdmin(cursor:UUID,limit:int,user_id:UUID):
    with get_db() as db:
        query=db.query(OrderItemsModel)
        if cursor:
            query=query.filter(OrderItemsModel.product_it>cursor).filter()

        query=query.order_by(OrderItemsModel.product_it).limit(limit+1)
        items=query.all()
        if not items:
            raise HTTPException(status_code=404,detail="order not found")
        next_cursor=None

        if len(items)>limit:
            next_cursor=items[-1].order_items_id
            items=items[:limit]

        list_data=[OrderResponse(
            order_items_id=c.order_items_id,
            user_id=c.order.user_id,
            order_id=c.order.order_id,
            total_amount=c.order.total_amount,
            product=OrderProductResponse(
                id=c.product.product_id,
                name=c.product.name,
              
                description=c.product.description,
                discount=c.product.discount,
                category_name=c.product.category.name,
                image=c.product.image,
                coverimage=c.product.coverimage


            ),
            status=c.order.status,
            price=c.price,
            stock_quantaty=c.stock_quantaty
            )for c in items]

        return OrderPaganitionResponse(order_list=list_data,next_cursor=next_cursor)

def updateOrder(order_id:UUID,order_status:OrderStatus):
    with get_db() as db:
        order=db.query(OrderModel).filter(OrderModel.order_id==order_id).first()
        if not order:
            raise HTTPException(status_code=404,detail=f"order id: {order_id} notfound")
        
        order.status=order_status
        db.commit()

        return {"message":f"order has updated in:-{order_status} "}

def search_from_status(cursor:UUID,limit:int,order_status:OrderStatus):
    with get_db() as db:
        query = (
            db.query(OrderModel)
            .join(OrderModel.order_item)  # assumes relationship `order_item` is defined in OrderModel
            .filter(OrderModel.status == order_status)
        )

        if cursor:
            query=query.filter(OrderItemsModel.product_it>cursor).filter()

        query=query.order_by(OrderItemsModel.product_it).limit(limit+1)
        items=query.all()
        if not items:
            raise HTTPException(status_code=404,detail="order not found")
        next_cursor=None

        if len(items)>limit:
            next_cursor=items[-1].order_id
            items=items[:limit]

        list_data = []
        for c in items:
            for item in c.order_item:  # <- iterate through the list of order items
                list_data.append(
                    OrderResponse(
                        order_items_id=item.order_items_id,
                        user_id=c.user_id,
                        order_id=c.order_id,
                        total_amount=c.total_amount,
                        product=OrderProductResponse(
                            id=item.product.product_id,
                            name=item.product.name,
                            description=item.product.description,
                            discount=item.product.discount,
                            category_name=item.product.category.name,
                            image=item.product.image,
                            coverimage=item.product.coverimage
                        ),
                        status=c.status,
                        price=item.price,
                        stock_quantaty=item.stock_quantaty
                    )
                )

        return OrderPaganitionResponse(order_list=list_data,next_cursor=next_cursor)
    
def check_quantay(act_quant,user_quant):
    if act_quant<user_quant:
        return False
    else:
        return True
    
def discount_price(discount,price):
    return round(float((price-((price*discount)/100))),2)