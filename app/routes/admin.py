from fastapi import APIRouter, Depends,status

from app.dependencies.admin_dependency import (
    create_admin_dependency,
    delete_admin_dependency,
    get_all_admins_dependency,
    get_all_sellers_dependency,
    get_all_users_dependency,
    get_all_products_dependency,
    get_full_stats,
)

router = APIRouter(
    prefix="/admins",
    tags=["admins"],
)


@router.post("/create-admin",status_code=status.HTTP_201_CREATED)
async def create_admin(admin = Depends(create_admin_dependency)):
    return admin

@router.delete("/delete/{admin_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_admin(message= Depends(delete_admin_dependency)):
    return message

@router.get("/users", status_code=status.HTTP_200_OK)
async def get_all_users(users = Depends(get_all_users_dependency)):
    return users

@router.get("/sellers", status_code=status.HTTP_200_OK)
async def get_all_sellers(sellers = Depends(get_all_sellers_dependency)):
    return sellers

@router.get("/admins", status_code=status.HTTP_200_OK)
async def get_all_admins(admins = Depends(get_all_admins_dependency)):
    return admins

@router.get("/products", status_code=status.HTTP_200_OK)
async def get_all_products(products = Depends(get_all_products_dependency)):
    return products

@router.get("/stats", status_code=status.HTTP_200_OK)
async def get_full_stats(stats = Depends(get_full_stats)):
    return stats