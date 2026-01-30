
import os,uuid

from fastapi import (
    Depends, 
    File,
    UploadFile,
    HTTPException, 
    Response,
    BackgroundTasks,
    status
)

from app.schemas.login_schema import Login

from app.auth_dependency import authenticate_user
from app.schemas import (
    Users, 
    CreateUser,
    Addresses,
    Carts,
    UpdateUser
)

from app.core import (
    create_access_token,
    hash_password,
    verify_password,
)

from app.config.settings import settings

from app.utils import (
    send_message_dependency,
    random_code_gen,
    get_current_timestamp,
    upload_file_to_cloudinary,
    delete_file_from_cloudinary
)


EXCLUDE_FIELDS = ["password", "verificationCode", "_id","cartId","addressId","avatarId"]


async def create_user_dependency(user: CreateUser, background_tasks: BackgroundTasks):

    existing_user = await Users.find_one(Users.email == user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

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

    user_response = new_user.model_dump(exclude=EXCLUDE_FIELDS)
    user_response["id"] = str(new_user.id)

    return {"success": True, "user": user_response}



async def get_current_user_dependency(payload=Depends(authenticate_user)):
    user_id = payload.get("id")

    user = await Users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_response:dict = user.model_dump(exclude=EXCLUDE_FIELDS)
    user_response["id"] = str(user.id)

    return {"success": True, "user": user_response}


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

    user_response:dict = user.model_dump(exclude=EXCLUDE_FIELDS)
    user_response["id"] = str(user.id)

    return {"success": True, "user": user_response}


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

    return {"success": True, "message": "User deleted successfully"}



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
        samesite="none",
    )

    user_response:dict = existing_user.model_dump(exclude=EXCLUDE_FIELDS)
    user_response["id"] = str(existing_user.id)

    return {"success": True, "message": user_response}


async def get_user_logout_dependency(response: Response, token: dict = Depends(authenticate_user)):
    response.delete_cookie(
        key="access_token",
        path="/",
        secure=True,
        samesite="none",
        httponly=True,
    )
    
    return {"success": True, "message": "User logged out successfully"}

async def update_user_avatar(image:UploadFile=File(...), payload:dict=Depends(authenticate_user)):
    user_id = payload.get("id")
    user = await Users.get(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    avatar_id = user.avatarId
    # extracting the extension
    if image.filename:
        _, ext = os.path.splitext(image.filename)
        suffix = ext or ""

    temp_path = None

    try:
        os.makedirs("temp", exist_ok=True)
        temp_id = str(uuid.uuid4())
        temp_filename = f"{temp_id}{suffix}"
        temp_path = os.path.join("temp", temp_filename)

        with open(temp_path, "wb") as tmp:
            tmp.write(await image.read())

        upload_result = upload_file_to_cloudinary(file_path=temp_path, public_id=temp_id, folder="user_avatars")

        if upload_result:
            user.avatarUrl = upload_result.get("secure_url")
            user.avatarId = upload_result.get("public_id")
        else:
            raise Exception("Unable to upload image")
        
    except Exception:
        raise HTTPException(status_code=500, detail="Unable to upload avatar")
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove("temp")
            except Exception as e:
                pass

    if avatar_id:
        try:
            data = await delete_file_from_cloudinary(public_id=avatar_id, resource_type="image")
        except Exception as e:
            pass  


    user.updatedAt = get_current_timestamp()
    await user.save()

    user_response:dict = user.model_dump(exclude=["password", "verificationCode", "_id","cartId","addressId","avatarId"])
    user_response["id"] = str(user.id)

    return {"success": True, "user": user_response}

async def remove_user_avatar(payload:dict=Depends(authenticate_user)):
    user_id = payload.get("id")
    user = await Users.get(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    avatar_id = user.avatarId

    if not avatar_id:
        raise HTTPException(status_code=400, detail="No avatar to remove")

    try:
        data = await delete_file_from_cloudinary(public_id=avatar_id, resource_type="image")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unable to delete avatar from cloud storage")  

    user.avatarUrl = None
    user.avatarId = None
    user.updatedAt = get_current_timestamp()
    await user.save()

    user_response:dict = user.model_dump(exclude=EXCLUDE_FIELDS)
    user_response["id"] = str(user.id)

    return {"success": True, "user": user_response}