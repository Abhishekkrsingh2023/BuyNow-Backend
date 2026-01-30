from fastapi import Depends, HTTPException, Response

from app.auth_dependency.auth_user import authenticate_user
from app.schemas import CreateUser, Users, Products

from app.core import (
    hash_password,
)

from beanie import BeanieObjectId




async def create_admin_dependency(admin: CreateUser):
    existing_user = await Users.find_one(Users.email == admin.email)

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    admin.password = await hash_password(admin.password)

    new_admin = Users(**admin.model_dump(by_alias=True))
    new_admin.role = "admin"

    await new_admin.insert()

    del new_admin.password
    return {"success": True, "user": new_admin}


async def delete_admin_dependency(admin_id:BeanieObjectId, token: dict = Depends(authenticate_user)):

    role = token.get("role")

    if role != "admin":
        raise HTTPException(status_code=403, detail="Operation forbidden: Admins only")

    user = await Users.get(admin_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await user.delete()
    return {"success": True, "message": "Admin deleted successfully"}


async def get_all_users_dependency(limit: int = 50, token: dict = Depends(authenticate_user)):

    role = token.get("role")

    if role != "admin":
        raise HTTPException(status_code=403, detail="Operation forbidden: Admins only")

    users = await Users.find(Users.role == "user",limit=limit).to_list()

    return {"success": True, "users": users}


async def get_all_sellers_dependency(limit: int = 50, token: dict = Depends(authenticate_user)):

    role = token.get("role")

    if role != "admin":
        raise HTTPException(status_code=403, detail="Operation forbidden: Admins only")

    sellers = await Users.find(Users.role == "seller",limit=limit).to_list()
    for seller in sellers:
        del seller.password

    return {"success": True, "sellers": sellers}

async def get_all_admins_dependency(limit: int = 50, token: dict = Depends(authenticate_user)):

    role = token.get("role")

    if role != "admin":
        raise HTTPException(status_code=403, detail="Operation forbidden: Admins only")

    admins = await Users.find(Users.role == "admin",limit=limit).to_list()
    for admin in admins:
        del admin.password

    return {"success": True, "admins": admins}

async def get_all_products_dependency(limit:int = 1000, token: dict = Depends(authenticate_user)):

    role = token.get("role")

    if role != "admin":
        raise HTTPException(status_code=403, detail="Operation forbidden: Admins only")


    products = await Products.find_all(limit=limit).to_list()
    return {"success": True, "products": products}

async def get_full_stats(token: dict = Depends(authenticate_user)):
    role = token.get("role")

    if role != "admin":
        raise HTTPException(status_code=403, detail="Operation forbidden: Admins only")

    total_users = await Users.find(Users.role == "user").count()
    total_sellers = await Users.find(Users.role == "seller").count()
    total_admins = await Users.find(Users.role == "admin").count()


    return {"success": True, "total_users": total_users, "total_sellers": total_sellers, "total_admins": total_admins}