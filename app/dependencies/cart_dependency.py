from fastapi import Depends, HTTPException

from beanie.operators import In
from beanie import BeanieObjectId

from app.schemas import Users, Products, Carts,CartItem

from app.auth_dependency.auth_user import authenticate_user
from app.utils.current_timestamp import get_current_timestamp



async def add_to_cart_dependency(cart:CartItem, token: dict = Depends(authenticate_user)):
    
    user_id = token.get("id")
    user = await Users.get(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_cart = await Carts.find_one(Carts.user.id == user.id)
    
    # Check if the product already exists in the cart
    for item in user_cart.items:
        if item.productId == cart.productId:
            item.quantity += cart.quantity
            break
    else:
        user_cart.items.append(cart)

    user_cart.updatedAt = get_current_timestamp()
    await user_cart.save()

    return {"success": True, "message": "Product added to cart successfully"}

async def get_products_in_cart(token: dict = Depends(authenticate_user)):
    user_id = token.get("id")

    cart = await Carts.find_one(Carts.user.id == BeanieObjectId(user_id))
    if not cart or not cart.items:
        return {"success": True, "cart": []}

    # work entirely with ObjectIds
    product_ids = [item.productId for item in cart.items]

    # fetch all products with one query
    products = await Products.find(
        In(Products.id, product_ids)
    ).to_list()

    if not products:
        return {"success": True, "cart": []}

    # map using ObjectId keys (no string conversion)
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