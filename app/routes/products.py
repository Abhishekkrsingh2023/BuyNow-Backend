from fastapi import APIRouter, Depends,status

from app.dependencies.product_dependency import (
    get_random_products_dependency,
    get_product_by_id_dependency,
)


router = APIRouter(
    prefix="/product",
    tags=["products"],
)


@router.get("", status_code=status.HTTP_200_OK)
async def get_random_product(products = Depends(get_random_products_dependency)):
    return products

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_product_by_id(product = Depends(get_product_by_id_dependency)):
    return product