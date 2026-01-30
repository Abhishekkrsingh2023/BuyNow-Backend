
from fastapi import BackgroundTasks,HTTPException,Response
from app.schemas.login_schema import OTPVerification
from app.schemas.user_schema import Users
from app.utils import (
    generate_random_otp,
    send_message_dependency
)

async def send_otp_dependency(email: str,background_tasks: BackgroundTasks):
    """
    send_message_dependency
    
    :param email: email address to send OTP for verification
    :type email: str
    """
    user = await Users.find_one(Users.email == email)
    if not user:
        return {"success": False, "message": "User with this email does not exist."}
    
    if user.isVerified:
        return {"success": False, "message": "User is already verified."}
    
    name = user.firstName
    otp = generate_random_otp()
    background_tasks.add_task(send_message_dependency, {"email": email, "name": name}, otp)

    return {"success": True, "message": "OTP sent to your email address."}

async def verify_user_dependency(otp_verification: OTPVerification, response: Response):
    user = await Users.find_one(Users.email == otp_verification.email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.isVerified:
        raise HTTPException(status_code=400, detail="User is already verified")

    if user.verificationCode != otp_verification.otp:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    
    user.isVerified = True
    user.verificationCode = None
    await user.save()
    response.status_code = 200

    return {"success": True, "message": "User verified successfully"}