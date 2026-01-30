
from fastapi import  HTTPException,BackgroundTasks
from app.utils import generate_random_otp,send_message_dependency
from app.schemas import Users

async def get_verification_code_dependency(email: str, background_tasks: BackgroundTasks):

    user = await Users.find_one(Users.email == email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.isVerified:
        raise HTTPException(status_code=400, detail="User is already verified")
    
    otp = generate_random_otp()
    user.verificationCode = otp
    await user.save()

    background_tasks.add_task(send_message_dependency,{"email": email,"name":user.firstName},otp)

    return {"message": f"Verification code sent to {email}"}