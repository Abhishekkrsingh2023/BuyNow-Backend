from fastapi import APIRouter, Depends,status

from app.dependencies.user_dependency import (
    create_user_dependency,
    remove_user_avatar,
    delete_user_dependency,
    update_user_avatar,
    remove_user_avatar
)

from app.dependencies.cart_dependency import (
    add_to_cart_dependency,
    get_products_in_cart,
    remove_from_cart_dependency
)

router = APIRouter(
    prefix="/user",
    tags=["users"],
)

@router.post("/register",status_code=status.HTTP_201_CREATED)
async def create_user(message = Depends(create_user_dependency)):
    return message

@router.post("/add-to-cart",status_code=status.HTTP_201_CREATED)
async def add_to_cart(message = Depends(add_to_cart_dependency)):
    return message

@router.get("/cart",status_code=status.HTTP_200_OK)
async def get_cart(products = Depends(get_products_in_cart)):
    return products


@router.delete("/cart/remove/{product_id}", status_code=status.HTTP_200_OK)
async def remove_from_cart(message: dict = Depends(remove_from_cart_dependency)):
    return message

@router.delete("/delete",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(message = Depends(delete_user_dependency)):
    return message

@router.put("/avatar", status_code=status.HTTP_200_OK)
async def update_avatar(message = Depends(update_user_avatar)):
    return message

@router.delete("/remove-avatar", status_code=status.HTTP_200_OK)
async def remove_avatar(message = Depends(remove_user_avatar)):
    return message