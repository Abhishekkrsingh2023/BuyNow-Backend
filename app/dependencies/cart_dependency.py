from fastapi import Depends, HTTPException

from beanie.operators import In
from beanie import BeanieObjectId

from app.schemas import Users, Products, Carts, CartItem

from app.auth_dependency.auth_user import authenticate_user
from app.utils.current_timestamp import get_current_timestamp


async def add_to_cart_dependency(cart: CartItem, token: dict = Depends(authenticate_user)):
    user_id = BeanieObjectId(token["id"])

    # Increment quantity if the product already exists
    update_existing = await Carts.find_one(
        Carts.user.id == user_id,
        {"items.productId": cart.productId}
    ).update(
        {
            "$inc": {"items.$.quantity": cart.quantity},
            "$set": {"updatedAt": get_current_timestamp()}
        }
    )

    # If matched, quantity was incremented — done
    if update_existing.matched_count > 0:
        return {"success": True, "message": "Product quantity updated"}

    item_to_push = cart.model_dump()
    # Else push a brand new cart item
    await Carts.find_one(Carts.user.id == user_id).update(
        {
            "$push": {"items": item_to_push},
            "$set": {"updatedAt": get_current_timestamp()}
        }
    )

    return {"success": True, "message": "Product added to cart"}



async def get_products_in_cart(token: dict = Depends(authenticate_user)):
    user_id = token.get("id")

    cart = await Carts.find_one(Carts.user.id == BeanieObjectId(user_id))
    if not cart or not cart.items:
        return {"success": True, "cart": []}

    product_ids = [item.productId for item in cart.items]

    products = await Products.find(
        In(Products.id, product_ids)
    ).to_list()

    if not products:
        return {"success": True, "cart": []}

    product_map = {product.id: product for product in products}

    cart_with_products = []
    for item in cart.items:
        product = product_map.get(item.productId)
        if product:
            pd = product.model_dump(
                exclude=["sellerID", "quantity", "_id", "description", "createdAt", "updatedAt"]
            )
            pd["id"] = str(product.id)

            cart_with_products.append({
                "product": pd,
                "quantity": item.quantity
            })

    return {"success": True, "cart": cart_with_products}


async def remove_from_cart_dependency(product_id: BeanieObjectId, token: dict = Depends(authenticate_user)):
    user_id = token.get("id")

    cart = Carts.get_pymongo_collection()

    await cart.find_one_and_update(
        {"user.$id": BeanieObjectId(user_id)},
        {
            "$pull": {
                "items": {"productId": product_id}
            },
            "$set": {
                "updatedAt": get_current_timestamp()
            }
        }
    )

    return {"success": True, "message": "Product removed from cart successfully"}