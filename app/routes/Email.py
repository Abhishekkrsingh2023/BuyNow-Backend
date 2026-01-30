from fastapi import (
    APIRouter,
    Depends,
    status
)
from app.dependencies.email_dependency import (
    send_otp_dependency,
    verify_user_dependency
)

router = APIRouter(
    prefix="/email",
    tags=["Email"]
)

@router.post("/send-verification-code", status_code=status.HTTP_200_OK)
async def send_email(message = Depends(send_otp_dependency)):
    return message

@router.post("/verify", status_code=status.HTTP_200_OK)
async def verify_email(message = Depends(verify_user_dependency)):
    return message