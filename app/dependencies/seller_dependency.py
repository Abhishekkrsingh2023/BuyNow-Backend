
from fastapi import HTTPException,status,BackgroundTasks

from app.utils import generate_random_otp,send_message_dependency
from app.schemas import CreateUser, Users
from app.core import hash_password

EXCLUDE_FIELDS_USER_SELLER = ["password", "verificationCode", "avatarId", "createdAt", "updatedAt", "isActive"]

async def create_seller_dependency(seller: CreateUser, background_tasks: BackgroundTasks):
    
    existing_user = await Users.find_one(Users.email == seller.email)

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    seller.password = await hash_password(seller.password)

    otp = generate_random_otp()
    
    background_tasks.add_task(
        send_message_dependency,
        receiver={"email": seller.email, "name": seller.firstName}, otp=otp
    )
    new_seller = Users(**seller.model_dump(by_alias=True), verificationCode=otp,role="seller")
    await new_seller.insert()
    
    seller_response = new_seller.model_dump(exclude=EXCLUDE_FIELDS_USER_SELLER)
    seller_response["id"] = str(new_seller.id)

    return {"success": True, "message": seller_response}
