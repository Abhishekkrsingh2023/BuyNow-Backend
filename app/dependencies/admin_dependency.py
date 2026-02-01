from unittest import result
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

    new_admin = Users(**admin.model_dump(by_alias=True,exclude_unset=True),role="admin")

    await new_admin.insert()

    admin_response = new_admin.model_dump(exclude=["_id","password","verificationCode","isVerified","createdAt","updatedAt"])
    admin_response["id"] = str(new_admin.id)

    return {"success": True, "user": admin_response}


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

    raw_motor = Users.get_pymongo_collection()
    pipeline = [
        {"$match": {"role": "user"}},
        {"$addFields": {"id": {"$toString": "$_id"}}},
        {"$limit": int(limit)},
        {"$project": {"_id": 0, "password": 0, "verificationCode": 0,"cartId":0,"addressId":0}},
    ]
    cursor = raw_motor.aggregate(pipeline)
    users = await cursor.to_list()

    return {"success": True, "users": users}


async def get_all_sellers_dependency(limit: int = 50, token: dict = Depends(authenticate_user)):

    role = token.get("role")

    if role != "admin":
        raise HTTPException(status_code=403, detail="Operation forbidden: Admins only")

    raw_motor = Users.get_pymongo_collection()
    pipeline = [
        {"$match": {"role": "seller"}},
        {"$addFields": {"id": {"$toString": "$_id"}}},
        {"$limit": int(limit)},
        {"$project": {"_id": 0, "password": 0, "verificationCode": 0,"cartId":0,"addressId":0}},
    ]
    cursor = raw_motor.aggregate(pipeline)
    sellers = await cursor.to_list()

    return {"success": True, "sellers": sellers}


async def get_all_admins_dependency(limit: int = 50, token: dict = Depends(authenticate_user)):

    role = token.get("role")

    if role != "admin":
        raise HTTPException(status_code=403, detail="Operation forbidden: Admins only")

    raw_motor = Users.get_pymongo_collection()
    pipeline = [
        {"$match": {"role": "admin"}},
        {"$addFields": {"id": {"$toString": "$_id"}}},
        {"$limit": int(limit)},
        {"$project": {"_id": 0, "password": 0, "verificationCode": 0,"cartId":0,"addressId":0}},
    ]
    cursor = raw_motor.aggregate(pipeline)
    admins = await cursor.to_list()

    return {"success": True, "admins": admins}

async def get_all_products_dependency(limit: int = 1000, token: dict = Depends(authenticate_user)):

    role = token.get("role")

    if role != "admin":
        raise HTTPException(status_code=403, detail="Operation forbidden: Admins only")

    products = Products.get_pymongo_collection()
    pipeline = [
        {"$limit": int(limit)},
        {"$addFields": {"id": {"$toString": "$_id"}}},
        {"$project": {"_id": 0, "sellerID": 0, "updatedAt": 0}},
    ]

    cursor = products.aggregate(pipeline)
    products_list = await cursor.to_list()

    return {"success": True, "products": products_list}


async def get_full_stats(token: dict = Depends(authenticate_user)):
    role = token.get("role")

    if role != "admin":
        raise HTTPException(status_code=403, detail="Operation forbidden: Admins only")

    pipeline = [
        {
            "$match": {
                "role": {"$in": ["user", "seller", "admin"]}
            }
        },
        {
            "$group": {
                "_id": "$role",
                "count": {"$sum": 1}
            }
        },
        {
            "$group": {
                "_id": None,
                "total_users": {
                    "$sum": {
                        "$cond": [{"$eq": ["$_id", "user"]}, "$count", 0]
                    }
                },
                "total_sellers": {
                    "$sum": {
                        "$cond": [{"$eq": ["$_id", "seller"]}, "$count", 0]
                    }
                },
                "total_admins": {
                    "$sum": {
                        "$cond": [{"$eq": ["$_id", "admin"]}, "$count", 0]
                    }
                }
            }
        },
        {
        "$project": {
            "_id": 0
        }
    }
    ]

    result = await Users.get_pymongo_collection().aggregate(pipeline).to_list(1)
    stats = result[0] if result else {}
    


    return {"success": True,"stats": stats }