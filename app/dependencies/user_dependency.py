
from fastapi import Depends, HTTPException, Response,BackgroundTasks

from app.schemas.login_schema import Login,OTPVerification
# from app.schemas.user_schema import UserCreate, UserUpdate

# from app.database.collections import UserSchema


from app.auth_dependency import authenticate_user
from app.schemas import Users, CreateUser,Addresses,Carts,UpdateUser

from app.core import (
    create_access_token,
    hash_password,
    verify_password,
)

from app.config.settings import settings

from app.utils import get_current_timestamp

from app.utils import send_message_dependency
from app.utils import random_code_gen

async def create_user_dependency(user: CreateUser, background_tasks: BackgroundTasks):
    existing_user = await Users.find_one(Users.email == user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user.password = await hash_password(user.password)
    otp = random_code_gen.generate_random_otp()

    new_user = Users(**user.model_dump(by_alias=True), verificationCode=otp)
    await new_user.insert()

    address = Addresses(user=new_user, addresses=[])
    cart = Carts(user=new_user, products=[])

    await cart.insert()
    await address.insert()

    new_user.addressId = address.id
    new_user.cartId = cart.id
    await new_user.save()

    background_tasks.add_task(
        send_message_dependency,
        {"email": user.email, "name": user.firstName},
        otp
    )

    del new_user.password
    del new_user.verificationCode

    return {"message": "success", "user": new_user}


async def verify_user_dependency(otp_verification: OTPVerification, response: Response):
    user = await Users.find_one(Users.email == otp_verification.email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.isVerified:
        response.status_code = 200
        return {"message": "User already verified"}

    if user.verificationCode != otp_verification.otp:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    
    user.isVerified = True
    user.verificationCode = None
    await user.save()
    response.status_code = 200

    return {"message": "User verified successfully"}


async def get_current_user_dependency(payload=Depends(authenticate_user)):
    user_id = payload.get("id")

    user = await Users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # removing password before returning user
    del user.password

    return user


async def update_user_dependency(user_update: UpdateUser, payload:dict=Depends(authenticate_user)):
    
    user_id = payload.get("id")
    user = await Users.get(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_values = user_update.model_dump(exclude_unset=True, by_alias=True)

    if "email" in update_values and update_values["email"] != user.email:
        existing_user = await Users.find_one(Users.email == update_values["email"])
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        user.isVerified = False

    if "password" in update_values:
        update_values["password"] = await hash_password(update_values["password"])

    update_values["updatedAt"] = get_current_timestamp()
    await user.update({"$set": update_values})

    del user.password
    del user.verificationCode

    return user



async def delete_user_dependency(token: dict = Depends(authenticate_user)):
    user_id = token.get("id")
    role = token.get("role")

    if role == "admin":
        raise HTTPException(status_code=403, detail="Operation forbidden: Admins cannot delete their account using this endpoint")
    
    user = await Users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # associated data deletion
    address = await Addresses.find_one(Addresses.userId.id == user.id)
    if address:
        await address.delete()

    cart = await Carts.find_one(Carts.userId.id == user.id)
    if cart:
        await cart.delete() 
    
    # delete user
    await user.delete()

    return {"message": "success"}



async def login_user_dependency(user: Login, response: Response):
    
    existing_user = await Users.find_one(Users.email == user.email)

    if not existing_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not await verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = await create_access_token({"id": str(existing_user.id), "role": existing_user.role})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        expires=60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        path="/",
        secure=True,
        samesite="strict",
    )

    del existing_user.password

    return {"success": True, "message": existing_user}


async def get_user_logout_dependency(response: Response, token: dict = Depends(authenticate_user)):
    response.delete_cookie(
        key="access_token",
        path="/",
        secure=True,
        samesite="strict",
        httponly=True,
    )
    
    return {"success": True, "message": "User logged out successfully"}

