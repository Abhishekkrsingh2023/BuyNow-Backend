from fastapi import APIRouter, Depends, status

from app.dependencies.seller_dependency import (
    create_seller_dependency,
)

from app.dependencies.product_dependency import (
    create_product_dependency,
    get_product_dependency
)

router = APIRouter(
    prefix="/seller",
    tags=["sellers"],
)

@router.post("/register",status_code=status.HTTP_201_CREATED)
async def create_seller(message = Depends(create_seller_dependency)):
    return message

@router.post("/create-product", status_code=status.HTTP_200_OK)
async def create_product(result = Depends(create_product_dependency)):
    return result

@router.get("/dashboard", status_code=status.HTTP_200_OK)
async def seller_dashboard(products = Depends(get_product_dependency)):
    return products
    