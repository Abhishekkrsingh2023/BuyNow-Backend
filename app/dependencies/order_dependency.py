
from beanie import BeanieObjectId
from fastapi import Depends,HTTPException,status

from app.dependencies.user_dependency import get_current_user_dependency
from app.schemas import Orders


async def get_orders_dependency(user_from_db=Depends(get_current_user_dependency)) -> list[dict]:
    user_id = BeanieObjectId(user_from_db["user"]["id"])

    pipeline = [
        {"$match": {"userId": user_id}},
        {"$sort": {"createdAt": -1}},
        {
            "$addFields": {
                "id": {"$toString": "$_id"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "userId": 0,
                "razorpay_order_id": 0,
            }
        }
    ]

    orders = await Orders.get_pymongo_collection().aggregate(pipeline).to_list(length=None)
    return {
        "success": True,
        "orders": orders
    }


async def get_order_details_dependency(order_id: BeanieObjectId,user_from_db=Depends(get_current_user_dependency))->dict:
    """
    Docstring for get_order_details_dependency
    
    :param order_id: Description: The unique identifier of the order.
    :type order_id: BeanieObjectId
    """
    order = await Orders.find_one(Orders.id == order_id, Orders.userId == BeanieObjectId(user_from_db["user"]["id"]))

    EXCLUDE_FIELDS = ["_id", "userId", "razorpay_order_id"]
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    orders = order.model_dump(exclude=EXCLUDE_FIELDS)
    return {
        "success": True,
        "orders": orders
    }